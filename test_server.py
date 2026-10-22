from server import parse_result

def mk(label,number,year,nums):
    return f'<h1>22 Eylül {year} 18:30 {label} Sonuçları</h1><div>Çekiliş no: {number}</div><h2>Kazanan Numaralar</h2>'+''.join(f'<span>{n}</span>' for n in nums)+'<h2>Kazanan Kategoriler</h2>'

def test_super():
    p=parse_result(mk('Süper Loto',114,2026,[3,15,43,48,50,52]),'super',2026,114,'https://www.millipiyangoonline.com/x')
    assert p['numbers']==[3,15,43,48,50,52]

def test_sayisal_extra_excluded():
    p=parse_result(mk('Sayısal Loto',101,2026,[1,5,22,30,40,81,67,73]),'sayisal',2026,101,'https://www.millipiyangoonline.com/x')
    assert p['numbers']==[1,5,22,30,40,81]

def test_reject_unexpected():
    try:parse_result(mk('Süper Loto',114,2026,[3,15,43]),'super',2026,114,'https://www.millipiyangoonline.com/x')
    except ValueError:pass
    else:raise AssertionError('malformed draw accepted')
