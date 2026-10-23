const ROOT='https://api.collectapi.com';
const PATHS={sayisal:'/chancegame/sayisalLoto',super:'/chancegame/superLoto'};
const MAX={sayisal:90,super:60};
function reply(code,obj){return {statusCode:code,headers:{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'},body:JSON.stringify(obj)}}
function normalize(entry,game){
  const raw=String(entry?.tarih||'').trim();
  const m=/^(\d{2})\.(\d{2})\.(\d{4})$/.exec(raw);
  if(!m)return null;
  const date=`${m[3]}-${m[2]}-${m[1]}`;
  const dt=new Date(date+'T00:00:00Z');
  if(!Number.isFinite(dt.getTime())||dt.toISOString().slice(0,10)!==date)return null;
  const chunks=typeof entry.rakamlar==='string'?entry.rakamlar.trim().split(/\s*[-,;]\s*/):entry.rakamlar;
  if(!Array.isArray(chunks)||chunks.length!==6)return null;
  const numbers=chunks.map(x=>Number(String(x).trim()));
  if(numbers.some(x=>!Number.isInteger(x)||x<1||x>MAX[game])||new Set(numbers).size!==6)return null;
  // 2020 öncesi Sayısal Loto farklı oyun kurallarıyla oynanıyordu.
  // Sonuç aktarılabilir; ancak döneme uygun analiz ve resmî teyit ayrı konulardır.
  return {game,date,drawNumber:'',numbers:numbers.sort((a,b)=>a-b),source:'collectapi',sourceUrl:ROOT+PATHS[game],status:'third_party_unverified',historicalRulesMayDiffer:game==='sayisal'&&date<'2020-08-01'};
}
export const handler=async(event)=>{
  const game=event.queryStringParameters?.game;
  if(!Object.hasOwn(PATHS,game||''))return reply(400,{status:'error',results:[],message:'game=sayisal veya game=super kullanın.'});
  const checkedAt=new Date().toISOString();const sourceUrl=ROOT+PATHS[game];
  const common={game,checkedAt,sourceUrl,results:[],historyComplete:false,verification:'third_party_unverified'};
  const secret=process.env.COLLECTAPI_KEY;
  if(!secret)return reply(200,{...common,status:'configuration_required',message:'Netlify ortam değişkeni COLLECTAPI_KEY tanımlanmamış.'});
  const apikey=secret.trim().replace(/^apikey\s+/i,'');
  try{
    const ctrl=new AbortController();const timer=setTimeout(()=>ctrl.abort(),9500);
    let response;
    try{response=await fetch(sourceUrl,{headers:{'Content-Type':'application/json',authorization:'apikey '+apikey,accept:'application/json'},signal:ctrl.signal,redirect:'error'})}finally{clearTimeout(timer)}
    if(!response.ok)return reply(200,{...common,status:'unavailable',httpStatus:response.status,message:response.status===401||response.status===403?'CollectAPI yetkilendirmesi başarısız; API anahtarını ve aboneliği kontrol edin.':`CollectAPI HTTP ${response.status} yanıtı verdi.`});
    const raw=await response.text();if(raw.length>1000000)return reply(200,{...common,status:'unavailable',message:'Yanıt boyutu beklenen sınırı aştı.'});
    let parsed;try{parsed=JSON.parse(raw)}catch{return reply(200,{...common,status:'unavailable',message:'CollectAPI geçerli JSON döndürmedi.'})}
    if(parsed?.success!==true||!Array.isArray(parsed.result))return reply(200,{...common,status:'unavailable',message:'CollectAPI sonuç biçimi beklenenden farklı veya başarılı değil.'});
    const results=parsed.result.map(x=>normalize(x,game)).filter(Boolean);
    if(!results.length)return reply(200,{...common,status:'unavailable',message:'Yanıtta geçerli altı sayılı çekiliş bulunamadı.'});
    return reply(200,{...common,status:'ok',results,message:`CollectAPI üzerinden ${results.length} kayıt okundu. Üçüncü taraf veri; resmî doğrulanmış değildir.`,historyComplete:false});
  }catch(e){const timeout=e.name==='AbortError'||e.name==='TimeoutError';return reply(200,{...common,status:'unavailable',message:timeout?'CollectAPI bağlantısı zaman aşımına uğradı.':'CollectAPI bağlantı hatası: '+String(e.message||e).slice(0,150)})}
};
export const _test={normalize};
