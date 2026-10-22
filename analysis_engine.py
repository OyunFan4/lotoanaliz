"""Deterministic, non-predictive statistics and leakage-free chronological evaluation."""
from collections import Counter
from itertools import combinations
from math import comb
import random

MAXIMUM = {'sayisal': 90, 'super': 60}

def validate(game, numbers):
    if game not in MAXIMUM: raise ValueError('Geçersiz oyun')
    if len(numbers)!=6 or any(type(x) is not int or not 1<=x<=MAXIMUM[game] for x in numbers) or len(set(numbers))!=6:
        raise ValueError('Altı farklı ve kurala uygun tam sayı gerekli')
    return sorted(numbers)

def frequency(game, draws):
    m=MAXIMUM[game]; hits=Counter(n for d in draws for n in d['numbers']); total=len(draws)
    last={n:None for n in range(1,m+1)}; gaps={n:total for n in range(1,m+1)}
    for i,d in enumerate(draws):
        for n in d['numbers']:last[n]=d['date'];gaps[n]=total-1-i
    return [{'number':n,'hits':hits[n],'rate':hits[n]/total if total else 0,
             'expected_rate':6/m,'last_seen':last[n],'draws_since':gaps[n],
             **{f'last_{period}':sum(n in d['numbers'] for d in draws[-period:]) for period in (10,25,50,100,250)}} for n in range(1,m+1)]

def distribution(game, draws, low_boundary=None):
    mid=low_boundary or MAXIMUM[game]//2
    odds=Counter(); lows=Counter(); sums=Counter(); consecutive=0
    for d in draws:
        a=d['numbers'];odds[sum(n%2 for n in a)]+=1;lows[sum(n<=mid for n in a)]+=1
        sums[sum(a)]+=1;consecutive+=int(any(b-a==1 for a,b in zip(a,a[1:])))
    return {'sample_size':len(draws),'low_boundary':mid,'odd_counts':dict(odds), 'low_counts':dict(lows),
            'sum_counts':dict(sums),'draws_with_consecutive':consecutive}

def cooccurrence(draws, size=2, limit=30):
    if size not in (2,3):raise ValueError('Yalnızca ikili ve üçlü')
    c=Counter(combo for d in draws for combo in combinations(d['numbers'],size))
    return [{'numbers':list(k),'hits':v} for k,v in sorted(c.items(), key=lambda x:(-x[1],x[0]))[:limit]]

def generated(game, strategy, training, rng):
    m=MAXIMUM[game]; weights=[1]*m
    if strategy in ('hot','recent','hybrid','pairs'):
        used=training[-25:] if strategy=='recent' else training
        for d in used:
            for n in d['numbers']:weights[n-1]+=1
        if strategy=='hybrid':
            for d in training[-25:]:
                for n in d['numbers']:weights[n-1]+=2
    for _ in range(500):
        available=list(range(1,m+1)); result=[]
        for __ in range(6):
            values=[weights[n-1] for n in available]; chosen=rng.choices(available,weights=values,k=1)[0]
            result.append(chosen);available.remove(chosen)
        result.sort();odd=sum(x%2 for x in result);low=sum(x<=m//2 for x in result)
        if strategy=='odd' and odd!=3:continue
        if strategy=='low' and low!=3:continue
        if strategy=='hybrid' and (not 2<=odd<=4 or not 2<=low<=4):continue
        if strategy=='sum' and len(training)>=10:
            totals=sorted(sum(d['numbers']) for d in training)
            if not totals[len(totals)//10]<=sum(result)<=totals[-len(totals)//10-1]:continue
        return result
    return sorted(rng.sample(range(1,m+1),6))

def backtest(game, draws, strategy='random', count=1, warmup=25, seed=42):
    if strategy not in ('random','hot','recent','odd','low','sum','pairs','hybrid'):raise ValueError('Strateji geçersiz')
    if not 1<=count<=100 or warmup<1:raise ValueError('Parametreler geçersiz')
    history=sorted(draws,key=lambda d:(d['date'],d.get('draw_number',0)))
    if len(history)<=warmup:return {'status':'insufficient_data','sample_size':0,'required':warmup+1}
    rng=random.Random(seed);baseline=random.Random(seed+1);results=[];baseline_results=[]
    for i in range(warmup,len(history)):
        previous=[d for d in history[:i] if d['date']<history[i]['date']]
        if len(previous)<warmup:continue
        target=set(history[i]['numbers'])
        predicted=[generated(game,strategy,previous,rng) for _ in range(count)]
        randoms=[generated(game,'random',previous,baseline) for _ in range(count)]
        results.extend(len(target.intersection(p)) for p in predicted)
        baseline_results.extend(len(target.intersection(p)) for p in randoms)
    if not results:return {'status':'insufficient_data','sample_size':0}
    return {'status':'ok','sample_size':len(results),'tested_draws':len(results)//count,
            'match_distribution':{str(i):results.count(i) for i in range(7)},
            'baseline_distribution':{str(i):baseline_results.count(i) for i in range(7)},
            'mean_matches':sum(results)/len(results),'baseline_mean_matches':sum(baseline_results)/len(baseline_results),
            'seed':seed,'strategy':strategy,'columns_per_draw':count,
            'note':'Geçmiş performans gelecekte kazanma olasılığını kanıtlamaz.'}


def significance(game, draws, simulations=1500, seed=42):
    """Monte Carlo null comparison of marginal frequencies; no predictive claims."""
    from math import sqrt
    if game not in MAXIMUM: raise ValueError('Geçersiz oyun')
    if not 200 <= simulations <= 10000: raise ValueError('Geçersiz simülasyon sayısı')
    m=MAXIMUM[game]; n=len(draws)
    if n<20:return {'status':'insufficient_data','sample_size':n,'minimum':20}
    freq=Counter(x for d in draws for x in validate(game,d['numbers']))
    expected=n*6/m
    obs=sum((freq[k]-expected)**2/expected for k in range(1,m+1))
    rng=random.Random(seed);exceed=0; stats=[]
    for _ in range(simulations):
        c=Counter(v for __ in range(n) for v in rng.sample(range(1,m+1),6))
        z=sum((c[k]-expected)**2/expected for k in range(1,m+1))
        stats.append(z);exceed+=(z>=obs)
    p=(exceed+1)/(simulations+1)
    return {'status':'ok','sample_size':n,'test':'monte_carlo_frequency_deviation',
        'observed_statistic':round(obs,5),'simulations':simulations,'seed':seed,
        'p_value':p,'expected_per_number':expected,'effect_size':round(sqrt(obs/(n*6)),5),
        'note':'Çoklu karşılaştırma ve seçilim yanlılığına dikkat edin. Bu test sonraki çekilişi öngörmez.'}

def draw_details(game, draws):
    """Aggregated descriptive metrics for verified draws."""
    m=MAXIMUM[game]
    if not draws:return {'sample_size':0,'ranges':{},'gaps':{},'min_numbers':{},'max_numbers':{}}
    gaps=Counter();minimum=Counter();maximum=Counter();ranges=Counter()
    for d in draws:
        ns=validate(game,d['numbers']);minimum[ns[0]]+=1;maximum[ns[-1]]+=1
        for a,b in zip(ns,ns[1:]):gaps[b-a]+=1
        ranges[len({(x-1)//10 for x in ns})]+=1
    return {'sample_size':len(draws),'number_limit':m,'gaps':dict(gaps),
            'min_numbers':dict(minimum),'max_numbers':dict(maximum),
            'tens_bands_covered':dict(ranges)}
