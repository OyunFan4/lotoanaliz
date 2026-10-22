"""LotoAnaliz AI: same-origin PWA plus cautious official-results checker.
No access controls are bypassed; requests which fail remain unverified.
"""
from __future__ import annotations
import json, logging, os, re, sqlite3, time, hmac, threading
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, Query, Header, Request
from extended_api import router as extended_router
import extended_api
from fastapi.staticfiles import StaticFiles

ROOT=Path(__file__).resolve().parent
DB=Path(os.environ.get('LOTO_DB_PATH',str(ROOT/'official_results.sqlite3')))
extended_api.DB_PATH=str(DB)
HOST='https://www.millipiyangoonline.com'
GAMES={'sayisal':('sayisal-loto',90), 'super':('super-loto',60)}
MONTHS={'ocak':1,'şubat':2,'mart':3,'nisan':4,'mayıs':5,'haziran':6,'temmuz':7,'ağustos':8,'eylül':9,'ekim':10,'kasım':11,'aralık':12}
app=FastAPI(title='LotoAnaliz AI — Resmî sonuç kontrol servisi',version='2.0')
logging.basicConfig(level=logging.INFO)

def connect():
    db=sqlite3.connect(DB,timeout=10)
    db.execute('CREATE TABLE IF NOT EXISTS results (game TEXT NOT NULL, year INTEGER NOT NULL, draw_number INTEGER NOT NULL, draw_date TEXT NOT NULL, numbers TEXT NOT NULL, source_url TEXT NOT NULL, fetched_at TEXT NOT NULL, PRIMARY KEY(game,year,draw_number))')
    db.execute('CREATE TABLE IF NOT EXISTS checks (game TEXT PRIMARY KEY, checked_at REAL NOT NULL, status TEXT NOT NULL, message TEXT NOT NULL)')
    db.execute('CREATE TABLE IF NOT EXISTS sync_jobs (id INTEGER PRIMARY KEY AUTOINCREMENT, game TEXT NOT NULL, year INTEGER, started_at TEXT NOT NULL, finished_at TEXT, checked INTEGER DEFAULT 0, inserted INTEGER DEFAULT 0, rejected INTEGER DEFAULT 0, status TEXT NOT NULL, cursor INTEGER DEFAULT 1, message TEXT DEFAULT "")')
    db.execute('CREATE TABLE IF NOT EXISTS backtest_runs (id INTEGER PRIMARY KEY AUTOINCREMENT, game TEXT NOT NULL, strategy TEXT NOT NULL, created_at TEXT NOT NULL, parameters TEXT NOT NULL, report TEXT NOT NULL)')
    db.execute('CREATE TABLE IF NOT EXISTS imports (id INTEGER PRIMARY KEY AUTOINCREMENT, game TEXT NOT NULL, imported_at TEXT NOT NULL, count INTEGER NOT NULL, original_name TEXT NOT NULL, source_type TEXT NOT NULL)')
    db.execute('CREATE TABLE IF NOT EXISTS rejects (id INTEGER PRIMARY KEY AUTOINCREMENT, game TEXT NOT NULL, year INTEGER, draw_number INTEGER, reason TEXT NOT NULL, checked_at TEXT NOT NULL, UNIQUE(game,year,draw_number))')
    db.execute('PRAGMA journal_mode=WAL')
    return db

def parse_result(html,game,year,number,url):
    soup=BeautifulSoup(html,'html.parser')
    if '{{#each' in html or '{{this}}' in html:
        raise ValueError('Resmî HTML sonuç sayıları yerine işlenmemiş şablon içeriyor')
    # Require an actual results heading and explicit draw number to avoid parsing adverts.
    heading=next((h.get_text(' ',strip=True) for h in soup.find_all(['h1','h2']) if 'Sonuçları' in h.get_text(' ',strip=True) and ('Süper Loto' if game=='super' else 'Sayısal Loto') in h.get_text(' ',strip=True)),None)
    if not heading: raise ValueError('Beklenen çekiliş başlığı yok')
    pat=re.search(r'(\d{1,2})\s+([A-Za-zÇĞİÖŞÜçğıöşü]+)\s+(\d{4})',heading)
    if not pat: raise ValueError('Başlıktan tarih okunamadı')
    mon=MONTHS.get(pat.group(2).casefold())
    if not mon: raise ValueError('Bilinmeyen ay')
    when=date(int(pat.group(3)),mon,int(pat.group(1)))
    if when.year!=year or when>date.today(): raise ValueError('Çekiliş tarihi uyuşmuyor')
    text=soup.get_text('\n',strip=True)
    no=re.search(r'Çekiliş\s*no\s*:\s*(\d+)',text,re.I)
    if not no or int(no.group(1))!=number: raise ValueError('Çekiliş numarası uyuşmuyor')
    label=next((tag for tag in soup.find_all(['h2','h3','h4']) if 'Kazanan Numaralar' in tag.get_text(' ',strip=True)),None)
    if label:
        chunks=[]
        for node in label.next_elements:
            if getattr(node,'name',None) in ('h1','h2','h3','h4') and node is not label:break
            if isinstance(node,str):
                s=node.strip()
                if s:chunks.append(s)
            if len(chunks)>70:break
        number_text=' '.join(chunks)
    else:
        split=re.split(r'Kazanan Numaralar',text,maxsplit=1)
        number_text=split[1].split('Kazanan Kategoriler')[0] if len(split)>1 else ''
    number_text=number_text.split('Kazanan Kategoriler')[0]
    # Only isolated number elements count.  Additional Joker/SuperStar numbers are excluded.
    pieces=re.findall(r'(?<!\d)\b\d{1,2}\b(?!\d)',number_text)
    expected=8 if game=='sayisal' else 6
    if len(pieces)!=expected: raise ValueError(f'Ana ve ek sayılar kesin olarak ayrılamadı ({len(pieces)} aday; beklenen {expected})')
    nums=sorted(map(int,pieces[:6]))
    if any(x<1 or x>GAMES[game][1] for x in nums) or len(set(nums))!=6:raise ValueError('Sayılar oyun kuralına uymuyor')
    return {'game':game,'date':when.isoformat(),'drawNumber':str(number),'numbers':nums,'status':'official_verified','sourceUrl':url,'fetchedAt':datetime.now(timezone.utc).isoformat()}

def expected_latest(game,now):
    # Approximate draw number only for choosing probe candidates; never interpret missing numbers as actual draws.
    # Scan within a conservative range, do not infer verified results from numbering.
    start=date(now.year,1,1)
    days=(now-start).days
    return min(160,max(1,int(days*3/7)+3))

def fetch_one(game,year,n):
    slug,_=GAMES[game]
    url=f'{HOST}/{slug}/cekilis-sonuclari.{n}.{year}'
    r=requests.get(url,headers={'User-Agent':'LotoAnalizAI/2.0 (public results verification)'},timeout=9,allow_redirects=False)
    if r.status_code!=200:raise ValueError(f'HTTP {r.status_code}')
    if len(r.content)>3_000_000:raise ValueError('Beklenmeyen büyüklük')
    return parse_result(r.text,game,year,n,url)

def rows(db,game,limit):
    return [{'game':g,'date':d,'drawNumber':str(n),'numbers':json.loads(nums),'status':'official_verified','sourceUrl':url,'fetchedAt':fetched} for g,d,n,nums,url,fetched in db.execute('SELECT game,draw_date,draw_number,numbers,source_url,fetched_at FROM results WHERE game=? ORDER BY draw_date DESC LIMIT ?', (game,limit))]

@app.middleware('http')
async def secure_headers(request:Request,call_next):
    response=await call_next(request)
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Referrer-Policy']='strict-origin-when-cross-origin'
    response.headers['X-Frame-Options']='DENY'
    response.headers['Permissions-Policy']='geolocation=(), microphone=(), camera=()'
    if request.url.scheme=='https':
        response.headers['Strict-Transport-Security']='max-age=31536000; includeSubDomains'
    if request.url.path.startswith('/api/'):
        response.headers['Cache-Control']='no-store'
    return response

@app.get('/api/health')
def health():return {'ok':True,'service':'LotoAnaliz AI online results checker'}

@app.get('/api/sync')
def sync(game:str=Query('super')):
    if game not in GAMES:raise HTTPException(400,'Bilinmeyen oyun')
    with connect() as db:
        old=db.execute('SELECT checked_at,status,message FROM checks WHERE game=?',(game,)).fetchone()
        if old and time.time()-old[0]<1200:
            return {'status':old[1],'message':old[2],'checkedAt':datetime.fromtimestamp(old[0],timezone.utc).isoformat(),'results':rows(db,game,500),'cached':True}
        # At most 8 requests per game/check. Never probe a restricted site aggressively.
        today=date.today();estimate=expected_latest(game,today)
        existing={r[0] for r in db.execute('SELECT draw_number FROM results WHERE game=? AND year=?',(game,today.year))}
        candidates=[n for n in range(max(1,estimate-5),estimate+3) if n not in existing][:8]
        accepted=0;errors=[]
        for n in candidates:
            try:
                res=fetch_one(game,today.year,n)
                db.execute('INSERT OR IGNORE INTO results VALUES(?,?,?,?,?,?,?)',(game,today.year,n,res['date'],json.dumps(res['numbers']),res['sourceUrl'],res['fetchedAt']))
                accepted+=1
            except requests.RequestException as e:
                errors.append('Resmî siteye ağ erişimi başarısız')
                break
            except ValueError as e:
                errors.append(f'Çekiliş {n}: {str(e)}')
                if '403' in str(e) or '429' in str(e):break
        status='ok' if accepted else ('limited' if errors else 'no_new')
        message=(f'{accepted} yeni resmî kayıt doğrulandı.' if accepted else 'Yeni doğrulanmış sonuç alınamadı.')
        if errors:message+=' '+errors[0]
        checked=time.time()
        db.execute('INSERT INTO checks VALUES(?,?,?,?) ON CONFLICT(game) DO UPDATE SET checked_at=excluded.checked_at,status=excluded.status,message=excluded.message',(game,checked,status,message))
        return {'status':status,'message':message,'checkedAt':datetime.fromtimestamp(checked,timezone.utc).isoformat(),'results':rows(db,game,500),'cached':False}

@app.get('/api/admin/history/scan')
def history_scan(game:str=Query('super'),year:int=Query(2026,ge=2020,le=2100),start:int=Query(1,ge=1,le=200),batch:int=Query(3,ge=1,le=10),x_admin_key:str|None=Header(None)):
    """Operator-driven bounded historical scan; NOT proof of archive completeness."""
    required=os.environ.get('LOTO_ADMIN_KEY')
    if not required or not x_admin_key or not hmac.compare_digest(x_admin_key, required):raise HTTPException(403,'Yetkisiz işlem')
    if game not in GAMES:raise HTTPException(400,'Geçersiz oyun')
    checked=inserted=rejected=0;reason=''
    with connect() as db:
        job=db.execute('INSERT INTO sync_jobs (game,year,started_at,status,cursor) VALUES(?,?,?,?,?)',
                       (game,year,datetime.now(timezone.utc).isoformat(),'running',start)).lastrowid
        for n in range(start,min(start+batch,201)):
            checked+=1
            try:
                item=fetch_one(game,year,n)
                row=db.execute('INSERT OR IGNORE INTO results VALUES(?,?,?,?,?,?,?)',
                               (game,year,n,item['date'],json.dumps(item['numbers']),item['sourceUrl'],item['fetchedAt']))
                inserted+=row.rowcount
            except (requests.RequestException, ValueError) as exc:
                rejected+=1;reason=str(exc)[:250]
                db.execute('INSERT INTO rejects(game,year,draw_number,reason,checked_at) VALUES(?,?,?,?,?) ON CONFLICT(game,year,draw_number) DO UPDATE SET reason=excluded.reason,checked_at=excluded.checked_at',
                           (game,year,n,reason,datetime.now(timezone.utc).isoformat()))
                if '403' in reason or '429' in reason or isinstance(exc,requests.RequestException):break
            time.sleep(0.5)
        db.execute('UPDATE sync_jobs SET finished_at=?,checked=?,inserted=?,rejected=?,status=?,cursor=?,message=? WHERE id=?',
                   (datetime.now(timezone.utc).isoformat(),checked,inserted,rejected,'limited' if rejected else 'completed',start+checked,reason,job))
    return {'game':game,'year':year,'checked':checked,'inserted':inserted,'rejected':rejected,'next_cursor':start+checked,'complete':False,'error':reason}

@app.get('/api/admin/history/progress')
def history_progress(game:str=Query('super'), year:int=Query(2026,ge=2020,le=2100),x_admin_key:str|None=Header(None)):
    required=os.environ.get('LOTO_ADMIN_KEY')
    if not required or not x_admin_key or not hmac.compare_digest(required,x_admin_key):
        raise HTTPException(403,'Yetkisiz işlem')
    if game not in GAMES:raise HTTPException(400,'Geçersiz oyun')
    with connect() as db:
        cur=db.execute('SELECT MAX(cursor) FROM sync_jobs WHERE game=? AND year=?',(game,year)).fetchone()[0]
        n=db.execute('SELECT COUNT(*) FROM results WHERE game=? AND year=?',(game,year)).fetchone()[0]
        rejects=db.execute('SELECT COUNT(*) FROM rejects WHERE game=? AND year=?',(game,year)).fetchone()[0]
    return {'game':game,'year':year,'next_cursor':cur or 1,'verified_count':n,
            'failed_candidates':rejects,'fully_verified':False}

@app.get('/api/admin/history/resume')
def history_resume(game:str=Query('super'),year:int=Query(2026,ge=2020,le=2100),batch:int=Query(3,ge=1,le=10),x_admin_key:str|None=Header(None)):
    progress=history_progress(game,year,x_admin_key)
    return history_scan(game,year,progress['next_cursor'],batch,x_admin_key)

@app.get('/api/official')
def official(game:str=Query('super'),limit:int=Query(500,ge=1,le=5000)):
    if game not in GAMES:raise HTTPException(400,'Bilinmeyen oyun')
    with connect() as db:return {'results':rows(db,game,limit)}

app.include_router(extended_router)
app.mount('/',StaticFiles(directory=str(ROOT),html=True),name='pwa')


# Optional scheduled synchronization: enable only on dedicated single-worker deployment.
# Public source is probed cautiously, with cooldown and no bypass of restrictions.
def _scheduled_checks():
    while True:
        time.sleep(max(3600, int(os.environ.get('LOTO_SYNC_INTERVAL_SECONDS', '21600'))))
        for name in ('sayisal', 'super'):
            try:
                sync(name)
            except Exception as exc:
                logging.warning('Scheduled sync failed for %s: %s', name, type(exc).__name__)

@app.on_event('startup')
def start_optional_scheduler():
    if os.environ.get('LOTO_ENABLE_SCHEDULER')=='1':
        threading.Thread(target=_scheduled_checks, daemon=True, name='loto-sync').start()
