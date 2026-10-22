import os, json, tempfile
from fastapi.testclient import TestClient
import extended_api, server
from analysis_engine import significance,draw_details


def samples(game='super', size=40):
    mx=60 if game=='super' else 90
    return [{'date':f'2026-02-{i%28+1:02}', 'numbers': sorted({((i*7+j*9)%mx)+1 for j in range(6)})} for i in range(size)]

def test_significance_deterministic():
    a=significance('super',samples(),200,42)
    assert a==significance('super',samples(),200,42)
    assert 0<a['p_value']<=1 and a['sample_size']==40

def test_significance_not_enough_data():
    assert significance('super',samples(size=4))['status']=='insufficient_data'

def test_detail_counts():
    r=draw_details('super',samples(size=6))
    assert r['sample_size']==6
    assert sum(r['gaps'].values())==30

def test_protected_history_and_headers(monkeypatch,tmp_path):
    monkeypatch.setenv('LOTO_ADMIN_KEY','long-test-admin-secret')
    path=tmp_path/'v8.db'
    monkeypatch.setattr(server,'DB',path)
    monkeypatch.setattr(extended_api,'DB_PATH',str(path))
    client=TestClient(server.app)
    assert client.get('/api/admin/history/progress').status_code==403
    r=client.get('/api/admin/history/progress',headers={'x-admin-key':'long-test-admin-secret'})
    assert r.status_code==200 and r.json()['next_cursor']==1
    assert r.headers['x-content-type-options']=='nosniff'
    assert r.headers['cache-control']=='no-store'
    assert client.get('/api/analytics/significance?game=super').json()['status']=='insufficient_data'
    assert client.get('/api/analytics/details?game=super').json()['sample_size']==0


def test_refuse_placeholder_template():
    from server import parse_result
    html='<h1>22 Eylül 2026 Süper Loto Sonuçları</h1><div>Çekiliş no: 114</div>{{#each balls}}'
    try:
        parse_result(html,'super',2026,114,'https://www.millipiyangoonline.com/xyz')
        assert False
    except ValueError:
        pass
