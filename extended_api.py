"""Backwards-compatible API router for server.py."""
import json, os, sqlite3, time, hmac, csv, io
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Query, Header, UploadFile, File
from pydantic import BaseModel, Field
from fastapi.responses import Response
from analysis_engine import frequency, distribution, cooccurrence, backtest, validate

router=APIRouter(prefix='/api')
DB_PATH=None

def connect_db():
    db=sqlite3.connect(DB_PATH, timeout=10)
    db.row_factory=sqlite3.Row
    db.execute('PRAGMA busy_timeout=10000')
    db.execute('CREATE TABLE IF NOT EXISTS results (game TEXT NOT NULL,year INTEGER NOT NULL,draw_number INTEGER NOT NULL,draw_date TEXT NOT NULL,numbers TEXT NOT NULL,source_url TEXT NOT NULL,fetched_at TEXT NOT NULL,PRIMARY KEY(game,year,draw_number))')
    db.execute('CREATE TABLE IF NOT EXISTS checks (game TEXT PRIMARY KEY,checked_at REAL NOT NULL,status TEXT NOT NULL,message TEXT NOT NULL)')
    db.execute('CREATE TABLE IF NOT EXISTS sync_jobs (id INTEGER PRIMARY KEY AUTOINCREMENT, game TEXT NOT NULL, year INTEGER, started_at TEXT NOT NULL, finished_at TEXT, checked INTEGER DEFAULT 0, inserted INTEGER DEFAULT 0, rejected INTEGER DEFAULT 0, status TEXT NOT NULL, cursor INTEGER DEFAULT 1, message TEXT DEFAULT "")')
    db.execute('CREATE TABLE IF NOT EXISTS backtest_runs (id INTEGER PRIMARY KEY AUTOINCREMENT, game TEXT NOT NULL, strategy TEXT NOT NULL, created_at TEXT NOT NULL, parameters TEXT NOT NULL, report TEXT NOT NULL)')
    db.execute('CREATE TABLE IF NOT EXISTS imports (id INTEGER PRIMARY KEY AUTOINCREMENT, game TEXT NOT NULL, imported_at TEXT NOT NULL, count INTEGER NOT NULL, original_name TEXT NOT NULL, source_type TEXT NOT NULL)')
    db.execute('CREATE TABLE IF NOT EXISTS rejects (id INTEGER PRIMARY KEY AUTOINCREMENT, game TEXT NOT NULL, year INTEGER, draw_number INTEGER, reason TEXT NOT NULL, checked_at TEXT NOT NULL, UNIQUE(game,year,draw_number))')
    return db

def database_draws(game, from_date=None,to_date=None):
    if game not in ('sayisal','super'):raise HTTPException(400,'Geçersiz oyun')
    with connect_db() as db:
        records=db.execute('SELECT year,draw_date,draw_number,numbers,source_url,fetched_at FROM results WHERE game=? ORDER BY draw_date,draw_number',(game,)).fetchall()
    return [{'game':game,'year':r['year'],'date':r['draw_date'],'drawNumber':str(r['draw_number']), 'draw_number':r['draw_number'],
             'numbers':json.loads(r['numbers']), 'status':'official_verified','sourceUrl':r['source_url'],'fetchedAt':r['fetched_at']}
             for r in records if (not from_date or r['draw_date']>=from_date) and (not to_date or r['draw_date']<=to_date)]

@router.get('/games')
def games():return [{'code':'sayisal','name':'Çılgın Sayısal Loto','max_number':90,'numbers_per_draw':6}, {'code':'super','name':'Süper Loto','max_number':60,'numbers_per_draw':6}]

@router.get('/draws')
def draws(game:str='sayisal',limit:int=Query(50,ge=1,le=500),offset:int=Query(0,ge=0),from_date:str|None=None,to_date:str|None=None):
    all_rows=database_draws(game,from_date,to_date)
    return {'total':len(all_rows),'results':list(reversed(all_rows))[offset:offset+limit]}

@router.get('/draws/latest')
def latest(game:str='sayisal'):
    r=database_draws(game)
    return {'result':r[-1] if r else None}

@router.get('/analytics/frequency')
def analytics_frequency(game:str='sayisal',limit_draws:int=Query(0,ge=0,le=100000),from_date:str|None=None,to_date:str|None=None):
    ds=database_draws(game,from_date,to_date)
    if limit_draws:ds=ds[-limit_draws:]
    return {'game':game,'sample_size':len(ds),'verified_only':True,'numbers':frequency(game,ds)}

@router.get('/analytics/distribution')
def analytics_distribution(game:str='sayisal',low_boundary:int|None=None,from_date:str|None=None,to_date:str|None=None):
    ds=database_draws(game,from_date,to_date)
    return distribution(game,ds,low_boundary)

@router.get('/analytics/significance')
def analytics_significance(game:str='sayisal', simulations:int=Query(1500,ge=200,le=10000),seed:int=42):
    from analysis_engine import significance
    return significance(game,database_draws(game),simulations,seed)

@router.get('/analytics/details')
def analytics_details(game:str='sayisal',from_date:str|None=None,to_date:str|None=None):
    from analysis_engine import draw_details
    return draw_details(game,database_draws(game,from_date,to_date))

@router.get('/analytics/cooccurrence')
def analytics_cooccurrence(game:str='sayisal',size:int=Query(2,ge=2,le=3),limit:int=Query(30,ge=1,le=1000)):
    ds=database_draws(game)
    return {'sample_size':len(ds),'size':size,'results':cooccurrence(ds,size,limit)}

class BacktestRequest(BaseModel):
    game:str='sayisal'
    strategy:str='random'
    count:int=Field(default=1,ge=1,le=100)
    warmup:int=Field(default=25,ge=1)
    seed:int=42

@router.post('/backtests/run')
def run_backtest(req:BacktestRequest):
    if req.game not in ('sayisal','super'):raise HTTPException(400,'Geçersiz oyun')
    report=backtest(req.game,database_draws(req.game),req.strategy,req.count,req.warmup,req.seed)
    with connect_db() as db:
        db.execute('INSERT INTO backtest_runs(game,strategy,created_at,parameters,report) VALUES(?,?,?,?,?)',
          (req.game,req.strategy,datetime.now(timezone.utc).isoformat(),req.model_dump_json(),json.dumps(report,ensure_ascii=False)))
    return report

@router.get('/backtests')
def backtests(limit:int=Query(25,ge=1,le=200)):
    with connect_db() as db:
        entries=db.execute('SELECT id,game,strategy,created_at,parameters,report FROM backtest_runs ORDER BY id DESC LIMIT ?',(limit,)).fetchall()
    return {'results':[dict(id=x['id'],game=x['game'],strategy=x['strategy'],created_at=x['created_at'],parameters=json.loads(x['parameters']),report=json.loads(x['report'])) for x in entries]}

@router.get('/sync/status')
def sync_status():
    with connect_db() as db:
        rows=db.execute('SELECT game,checked_at,status,message FROM checks').fetchall()
        jobs=db.execute('SELECT * FROM sync_jobs ORDER BY id DESC LIMIT 10').fetchall()
        rejects=db.execute('SELECT game,count(*) AS count FROM rejects GROUP BY game').fetchall()
    return {'checks':[dict(x) for x in rows],'recent_jobs':[dict(x) for x in jobs], 'rejected_by_game':[dict(x) for x in rejects],
            'complete_history_verified':False}

@router.get('/coverage')
def coverage(game:str='sayisal'):
    ds=database_draws(game)
    with connect_db() as db:
        years=[dict(r) for r in db.execute('SELECT year,count(*) as verified FROM results WHERE game=? GROUP BY year ORDER BY year',(game,))]
        rejected=db.execute('SELECT count(*) FROM rejects WHERE game=?',(game,)).fetchone()[0]
    return {'game':game,'verified':len(ds),'by_year':years,'rejected':rejected,'all_history_complete':False,'note':'Bağımsız resmî arşiv kapsam doğrulaması yapılmadı.'}

class PredictionsRequest(BaseModel):
    game:str='sayisal';strategy:str='random';count:int=Field(5,ge=1,le=100);seed:int=42

@router.post('/predictions/generate')
def prediction_generate(req:PredictionsRequest):
    import random
    from analysis_engine import generated
    if req.game not in ('sayisal','super'):raise HTTPException(400,'Geçersiz oyun')
    if req.strategy not in ('random','hot','recent','odd','low','sum','pairs','hybrid'):raise HTTPException(400,'Geçersiz strateji')
    rng=random.Random(req.seed); ds=database_draws(req.game);out=[];seen=set()
    for _ in range(req.count*100):
        x=generated(req.game,req.strategy,ds,rng);k=tuple(x)
        if k not in seen:seen.add(k);out.append(x)
        if len(out)==req.count:break
    return {'game':req.game,'strategy':req.strategy,'seed':req.seed,'verified_sample':len(ds),'combinations':out,'disclaimer':'Kazanma olasılığında kanıtlanmış bir artış yoktur.'}

@router.get('/predictions')
def predictions():return {'results':[],'note':'Tahminler bu cihazdaki PWA üzerinde tutulur; API sunucusuna aktarılmaz.'}


def check_admin(header_value):
    required=os.environ.get('LOTO_ADMIN_KEY','')
    if not required or not header_value or not hmac.compare_digest(required,header_value):
        raise HTTPException(403,'Yönetici yetkisi gerekli')

@router.get('/draws/export.csv')
def export_draws(game:str='sayisal'):
    items=database_draws(game)
    output=io.StringIO(); writer=csv.writer(output)
    writer.writerow(['game','date','drawNumber','n1','n2','n3','n4','n5','n6','sourceUrl'])
    for d in items:writer.writerow([d['game'],d['date'],d['drawNumber'],*d['numbers'],d['sourceUrl'] if d['sourceUrl'].startswith('https://www.millipiyangoonline.com/') else ''])
    return Response(output.getvalue(),media_type='text/csv; charset=utf-8',headers={'Content-Disposition':f'attachment; filename={game}-verified.csv'})

@router.post('/import/csv')
async def import_csv(file:UploadFile=File(...),x_admin_key:str|None=Header(None)):
    """Operator-reviewed official CSV only; does not promote arbitrary CSV to verified."""
    check_admin(x_admin_key)
    raw=await file.read(2_000_001)
    if len(raw)>2_000_000:raise HTTPException(413,'Dosya çok büyük')
    try:
        text=raw.decode('utf-8-sig'); items=list(csv.DictReader(io.StringIO(text)))
    except (UnicodeError,csv.Error):raise HTTPException(422,'CSV okunamadı')
    if len(items)>10000:raise HTTPException(413,'Çok fazla kayıt')
    # Never allow a user-provided CSV to become officially verified without checking official source.
    inserted=0; invalid=0
    with connect_db() as db:
        db.execute('CREATE TABLE IF NOT EXISTS unverified_imports (id INTEGER PRIMARY KEY AUTOINCREMENT, game TEXT NOT NULL, draw_date TEXT NOT NULL, draw_number TEXT, numbers TEXT NOT NULL, imported_at TEXT NOT NULL, UNIQUE(game,draw_date,draw_number))')
        for row in items:
            try:
                game=row.get('game','').strip();number_text=row.get('drawNumber','').strip()
                if game not in ('sayisal','super'):raise ValueError('invalid game')
                draw_date=datetime.strptime(row.get('date',''),'%Y-%m-%d').date().isoformat()
                numbers=validate(game,[int(row[f'n{i}']) for i in range(1,7)])
                result=db.execute('INSERT OR IGNORE INTO unverified_imports(game,draw_date,draw_number,numbers,imported_at) VALUES(?,?,?,?,?)',
                   (game,draw_date,number_text,json.dumps(numbers),datetime.now(timezone.utc).isoformat()))
                inserted+=result.rowcount
            except (ValueError,TypeError,KeyError):invalid+=1
        db.execute('INSERT INTO imports(game,imported_at,count,original_name,source_type) VALUES(?,?,?,?,?)',
                   ('mixed',datetime.now(timezone.utc).isoformat(),inserted,(file.filename or 'upload')[:100],'unverified_csv'))
    return {'status':'unverified','inserted':inserted,'invalid':invalid,'note':'İçe aktarılan CSV kayıtları resmî doğrulanmış arşive eklenmedi.'}

@router.get('/imports/unverified')
def unverified_imports(x_admin_key:str|None=Header(None),limit:int=Query(100,ge=1,le=1000)):
    check_admin(x_admin_key)
    with connect_db() as db:
        db.execute('CREATE TABLE IF NOT EXISTS unverified_imports (id INTEGER PRIMARY KEY AUTOINCREMENT, game TEXT NOT NULL, draw_date TEXT NOT NULL, draw_number TEXT, numbers TEXT NOT NULL, imported_at TEXT NOT NULL, UNIQUE(game,draw_date,draw_number))')
        return {'results':[dict(r) for r in db.execute('SELECT * FROM unverified_imports ORDER BY id DESC LIMIT ?',(limit,))]}
