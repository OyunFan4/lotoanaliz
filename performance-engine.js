(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;root.LotoPerformance=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const valid=(a,max)=>Array.isArray(a)&&a.length===6&&new Set(a).size===6&&a.every(n=>Number.isInteger(n)&&n>=1&&n<=max);
const drawMatch=(p,d)=>p.game===d.game&&String(p.drawNumber)===String(d.drawNumber)&&p.drawDate===d.date;
function evaluate(predictions,draws,opts={}){
 const accepted=draws.filter(d=>d.status==='official_verified'&&valid(d.numbers,d.game==='super'?60:90)&&d.drawNumber&&d.date&&!d.conflict);
 const seen=new Set();const items=[];
 for(const p of predictions){if(!p||!p.id||seen.has(p.id))continue;seen.add(p.id);
  if(!['sayisal','super'].includes(p.game)||!valid(p.numbers,p.game==='super'?60:90))continue;
  // Legacy predictions without a target are displayed but cannot be evaluated.
  const targetReady=typeof p.drawNumber==='string'&&p.drawNumber.trim()&&/^\d{4}-\d\d-\d\d$/.test(p.drawDate||'')&&Number.isFinite(Date.parse(p.createdAt||''));
  const eligible=targetReady&&Date.parse(p.createdAt)<Date.parse(p.drawDate+'T00:00:00+03:00');
  const matches=eligible?accepted.filter(d=>drawMatch(p,d)):[];
  const draw=matches.length===1?matches[0]:null;
  const matchCount=draw?p.numbers.filter(n=>draw.numbers.includes(n)).length:null;
  items.push({...p,draw:draw||null,matchCount,status:draw?'evaluated':'pending',reason:!targetReady?'Hedef çekiliş belirtilmemiş':!eligible?'Çekiliş günü öncesinde kaydedilmemiş':matches.length>1?'Çelişkili çekiliş kayıtları':null});
 }
 const filtered=items.filter(p=>(!opts.game||opts.game==='all'||p.game===opts.game)&&(!opts.method||opts.method==='all'||p.strategy===opts.method)&&(!opts.from||String(p.createdAt).slice(0,10)>=opts.from)&&(!opts.to||String(p.createdAt).slice(0,10)<=opts.to)&&(!opts.status||opts.status==='all'||p.status===opts.status));
 const evaluated=filtered.filter(p=>p.status==='evaluated'),pending=filtered.filter(p=>p.status==='pending');
 const distribution=Array.from({length:7},(_,i)=>evaluated.filter(p=>p.matchCount===i).length);
 return {items:filtered,total:evaluated.length,pending:pending.length,correct:evaluated.filter(p=>p.matchCount>=1).length,best:evaluated.length?Math.max(...evaluated.map(p=>p.matchCount)):null,rate:evaluated.length?100*evaluated.filter(p=>p.matchCount>=1).length/evaluated.length:null,distribution,hasData:evaluated.length>0};
}
return {evaluate,valid};});
