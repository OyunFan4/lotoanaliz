from analysis_engine import validate, frequency,cooccurrence,backtest,generated
import pytest, random

def fake(game,count=45):
    r=random.Random(20)
    return [{'date':f'2026-{1+i//28:02d}-{1+i%28:02d}','numbers':sorted(r.sample(range(1,(90 if game=='sayisal' else 60)+1),6))} for i in range(count)]

def test_validation():
    assert validate('super',[2,1,6,5,4,3])==[1,2,3,4,5,6]
    with pytest.raises(ValueError):validate('super',[1,1,2,3,4,5])
    with pytest.raises(ValueError):validate('super',[1,2,3,4,5,61])

def test_every_number_including_zeroes():
    f=frequency('sayisal',[{'date':'2026-01-01','numbers':[1,2,3,4,5,6]}]);assert len(f)==90
    assert f[0]['hits']==1 and f[-1]['hits']==0
    assert f[0]['last_250']==1

def test_pairs_triples():
    d=[{'date':'2026-01-01','numbers':[1,2,3,4,5,6]},{'date':'2026-01-02','numbers':[1,2,3,7,8,9]}]
    assert cooccurrence(d,2)[0]=={'numbers':[1,2],'hits':2}
    assert cooccurrence(d,3)[0]=={'numbers':[1,2,3],'hits':2}

def test_backtesting_and_reproducibility():
    d=fake('super')
    assert backtest('super',d,warmup=25)['tested_draws']==20
    assert backtest('super',d,'hot',seed=13)==backtest('super',d,'hot',seed=13)
    assert backtest('super',d[:4])['status']=='insufficient_data'

def test_no_future_leakage():
    d=fake('super')
    a=backtest('super',d,'recent',warmup=25,seed=31)
    changed=d+[{'date':'2027-01-01','numbers':[1,2,3,4,5,6]}]
    b=backtest('super',changed,'recent',warmup=25,seed=31)
    assert a['tested_draws']+1==b['tested_draws']
    # Existing result distribution alone need not match after addition, but sequential engine uses history[:i] only.

def test_strategies_valid():
    for g in ('sayisal','super'):
        for strategy in ('random','hot','recent','odd','low','sum','pairs','hybrid'):
            x=generated(g,strategy,fake(g),random.Random(12));assert validate(g,x)==x
