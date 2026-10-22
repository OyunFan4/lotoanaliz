import json
import pytest
from fastapi.testclient import TestClient
import server, extended_api

@pytest.fixture
def client(tmp_path,monkeypatch):
    db=tmp_path/'test.sqlite'
    monkeypatch.setattr(server,'DB',db)
    monkeypatch.setattr(extended_api,'DB_PATH',str(db))
    monkeypatch.setenv('LOTO_ADMIN_KEY','test_key_dont_use_in_production')
    with server.connect() as conn:
        conn.execute('INSERT INTO results VALUES(?,?,?,?,?,?,?)',('super',2026,1,'2026-01-01',json.dumps([1,2,3,4,5,6]),'https://www.millipiyangoonline.com/super-loto/test','2026-01-02T00:00:00+00:00'))
    return TestClient(server.app)

def test_health_and_draws(client):
    assert client.get('/api/health').json()['ok']
    r=client.get('/api/draws?game=super'); assert r.status_code==200 and r.json()['total']==1
    assert client.get('/api/draws/latest?game=super').json()['result']['numbers']==[1,2,3,4,5,6]
    assert client.get('/api/analytics/frequency?game=super').json()['numbers'][0]['hits']==1

def test_export_and_backtests(client):
    r=client.get('/api/draws/export.csv?game=super'); assert r.status_code==200 and 'drawNumber' in r.text
    r=client.post('/api/backtests/run',json={'game':'super','strategy':'random','warmup':1,'count':1,'seed':14}); assert r.status_code==200
    assert len(client.get('/api/backtests').json()['results'])==1

def test_csv_import_is_unverified_and_admin_only(client):
    csv=b'game,date,drawNumber,n1,n2,n3,n4,n5,n6\nsuper,2026-01-03,2,1,2,3,4,5,6\n'
    unauth=client.post('/api/import/csv',files={'file':('sample.csv',csv,'text/csv')}); assert unauth.status_code==403
    imported=client.post('/api/import/csv',files={'file':('sample.csv',csv,'text/csv')},headers={'x-admin-key':'test_key_dont_use_in_production'})
    assert imported.status_code==200 and imported.json()['inserted']==1 and imported.json()['status']=='unverified'
    assert client.get('/api/draws?game=super').json()['total']==1
    assert len(client.get('/api/imports/unverified',headers={'x-admin-key':'test_key_dont_use_in_production'}).json()['results'])==1

def test_admin_scan_protected(client):
    assert client.get('/api/admin/history/scan?game=super&year=2026').status_code==403

def test_invalid_game(client):
    assert client.get('/api/draws?game=other').status_code==400
    assert client.post('/api/predictions/generate',json={'game':'other'}).status_code==400
