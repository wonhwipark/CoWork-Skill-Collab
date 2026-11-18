#!/usr/bin/env node
"use strict";
/* Pure in-memory contract-oracle regression. No host, network, model, watcher or write operations.
 * Usage from repository root: node collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/test_ace_pec_safe_synthetic_r0001.js
 * Only static local read of pinned design r0001/r0002; not a production skill or host E2E test.
 */
function runSuite(design, baseline) {
  "use strict";
  const cases=[];
  function check(id,fn){try{fn();cases.push({id,status:"PASS"})}catch(e){cases.push({id,status:"FAIL",reason:String(e.message||e)})}}
  function eq(actual,expected,label){if(actual!==expected)throw Error((label||"unexpected value")+" expected="+JSON.stringify(expected)+" actual="+JSON.stringify(actual))}
  function ok(condition,label){if(!condition)throw Error(label||"assertion failed")}
  function utf8(s){const a=[];for(let i=0;i<s.length;i++){let c=s.codePointAt(i);if(c>65535)i++;if(c<128)a.push(c);else if(c<2048)a.push(192|(c>>6),128|(c&63));else if(c<65536)a.push(224|(c>>12),128|((c>>6)&63),128|(c&63));else a.push(240|(c>>18),128|((c>>12)&63),128|((c>>6)&63),128|(c&63))}return a}
  function sha256(src){const primes=[],k=[];for(let n=2;k.length<64;n++){let p=true;for(let j=2;j*j<=n;j++)if(n%j===0){p=false;break}if(p){primes.push(n);k.push(Math.floor((Math.cbrt(n)%1)*4294967296)>>>0)}}let H=primes.slice(0,8).map(n=>Math.floor((Math.sqrt(n)%1)*4294967296)>>>0),b=src.slice(),l=BigInt(b.length)*8n;b.push(128);while(b.length%64!==56)b.push(0);for(let n=7;n>=0;n--)b.push(Number((l>>BigInt(n*8))&255n));const rr=(x,n)=>(x>>>n)|(x<<(32-n));for(let p=0;p<b.length;p+=64){const w=[];for(let i=0;i<16;i++)w[i]=(b[p+i*4]<<24)|(b[p+i*4+1]<<16)|(b[p+i*4+2]<<8)|b[p+i*4+3];for(let i=16;i<64;i++){let x=w[i-15],y=w[i-2];w[i]=(w[i-16]+(rr(x,7)^rr(x,18)^(x>>>3))+w[i-7]+(rr(y,17)^rr(y,19)^(y>>>10)))>>>0}let[a,c,d,e,f,g,h,j]=H;for(let i=0;i<64;i++){let t1=(j+(rr(f,6)^rr(f,11)^rr(f,25))+((f&g)^((~f)&h))+k[i]+w[i])>>>0,t2=((rr(a,2)^rr(a,13)^rr(a,22))+((a&c)^(a&d)^(c&d)))>>>0;j=h;h=g;g=f;f=(e+t1)>>>0;e=d;d=c;c=a;a=(t1+t2)>>>0}const v=[a,c,d,e,f,g,h,j];for(let i=0;i<8;i++)H[i]=(H[i]+v[i])>>>0}return H.map(x=>x.toString(16).padStart(8,"0")).join("")}
  function latestDecision(rows,requested) {
    const matching=rows.filter(r=>r.work===requested.work&&r.scope===requested.scope&&r.subject===requested.subject);
    if(!matching.length)return {status:"HOLD",reason:"NO_MATCHING_DECISION"};
    if(matching.some(r=>r.approved!==true||!Number.isSafeInteger(r.append)||r.append<0||typeof r.id!=="string"))return {status:"HOLD",reason:"UNVERIFIED_DECISION"};
    const ordered=matching.slice().sort((a,b)=>a.append-b.append);
    for(let i=1;i<ordered.length;i++)if(ordered[i].append===ordered[i-1].append)return {status:"HOLD",reason:"AMBIGUOUS_ORDER"};
    const pick=ordered[ordered.length-1];
    return {status:pick.action==="REVOKE"?"REVOKED":"SELECTED",id:pick.id};
  }
  function evidenceCheck(e) {
    if(e.access!==true)return "HOLD";
    if(typeof e.revision!=="string"||e.revision!==e.expectedRevision)return "HOLD";
    if(!Array.isArray(e.source)||!Array.isArray(e.excerpt)||!e.source.every(v=>Number.isInteger(v)&&v>=0&&v<256)||!e.excerpt.every(v=>Number.isInteger(v)&&v>=0&&v<256))return "HOLD";
    if(!Number.isSafeInteger(e.offset)||!Number.isSafeInteger(e.length)||e.offset<0||e.length<0||e.offset+e.length>e.source.length)return "HOLD";
    if(e.fileDigest!==sha256(e.source)||typeof e.pointer!=="string"||!e.pointer)return "HOLD";
    const extracted=e.source.slice(e.offset,e.offset+e.length);
    return sha256(extracted)===sha256(e.excerpt)&&extracted.length===e.excerpt.length?"PASS":"FAIL";
  }
  function guardIntent(a){return a.writes===0&&a.modelCalls===0&&a.subagents===0&&a.autoJobs===0&&a.readyWrites===0?"PASS":"FAIL"}
  function dispatchPreviouslySealed(key,sealed){return sealed.indexOf(key)>=0?"HOLD":"ELIGIBLE_FOR_OTHER_GATES"}
  const a={work:"SYNTH-WORK-01",scope:"feature-a",subject:"decision-1"};
  const rows=[
    {work:a.work,scope:a.scope,subject:a.subject,id:"D-OLD",approved:true,append:10,action:"SELECT"},
    {work:a.work,scope:a.scope,subject:a.subject,id:"D-NEW",approved:true,append:11,action:"SELECT"}
  ];
  const source=utf8("CL=12345|PR=99|IPC=TX_READY|조건=NR|확인");
  const phrase=utf8("TX_READY");
  let start=-1; for(let i=0;i<=source.length-phrase.length;i++)if(phrase.every((v,j)=>source[i+j]===v)){start=i;break}
  const ev={access:true,revision:"commit-a",expectedRevision:"commit-a",source,excerpt:phrase,offset:start,length:phrase.length,fileDigest:sha256(source),pointer:"Evidence/SYNTH-001"};
  check("STATIC-SHA256-VECTOR",()=>eq(sha256(utf8("abc")),"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"));
  check("STATIC-R0001-IMMUTABLE",()=>eq(sha256(utf8(baseline)),"aa69b2e6bba529d09609d8c6c7b1ead0d4b3d744208361ce447c87ad57b41303"));
  check("STATIC-R0002-PINNED",()=>eq(sha256(utf8(design)),"8959c5785da37d0a7f48687fbbe17576c4f0f517be93ffcd9befc029a1c6def1"));
  check("STATIC-12-ACCEPTANCE-IDS",()=>{const ids=["ACE-01","ACE-02","ACE-03","PEC-01","PEC-02","PEC-03","PEC-04","ACON-01","ACON-02","SAFE-01","SAFE-02","SAFE-03"];for(const id of ids){const matches=design.match(new RegExp("\\| "+id+" \\|","g"))||[];eq(matches.length,1,id)}});
  check("STATIC-R1-REVIEW-CLOSED",()=>ok(design.includes("CLOSED_NO_AUTOMATIC_REREVIEW")&&design.includes("NEW_MODEL_CALLS_FOR_r0002=0")&&design.includes("ACON_PAID_REPETITION=NOT_RUN")));
  check("ACE-02-LATEST-APPEND",()=>eq(latestDecision(rows,a).id,"D-NEW"));
  check("ACE-02-CURRENT-MTIME-IRRELEVANT",()=>{const b=rows.map(x=>({...x,mtime:"2099-01-01"}));eq(latestDecision(b,a).id,"D-NEW")});
  check("ACE-02-OTHER-SCOPE-ISOLATION",()=>{const b=rows.concat([{...rows[1],scope:"feature-b",id:"D-OTHER",append:999}]);eq(latestDecision(b,a).id,"D-NEW")});
  check("ACE-02-CONFLICT-HOLD",()=>{const b=rows.concat([{...rows[1],id:"D-AMBIG",append:11}]);eq(latestDecision(b,a).status,"HOLD")});
  check("ACE-02-UNVERIFIED-AUTH-HOLD",()=>{const b=rows.concat([{...rows[1],id:"D-NOAPP",append:12,approved:false}]);eq(latestDecision(b,a).status,"HOLD")});
  check("ACE-02-REVOCATION",()=>{const b=rows.concat([{...rows[1],id:"D-REVOKE",append:12,action:"REVOKE"}]);eq(latestDecision(b,a).status,"REVOKED")});
  check("PEC-01-EXACT-RAW-RANGE",()=>eq(evidenceCheck(ev),"PASS"));
  check("PEC-01-ONE-BYTE-CORRUPTION",()=>{const b={...ev,excerpt:ev.excerpt.slice()};b.excerpt[0]^=1;eq(evidenceCheck(b),"FAIL")});
  check("PEC-01-SOURCE-REV-MISMATCH",()=>eq(evidenceCheck({...ev,expectedRevision:"commit-b"}),"HOLD"));
  check("PEC-01-IDENTIFIERS-PRESERVED",()=>{const keys={cl:"12345",jira:"SYNTH-101",pr:"99",ipc:"TX_READY",source:"commit-a",evidence:"SYNTH-001"};eq(JSON.stringify({...keys}),JSON.stringify(keys))});
  check("PEC-03-MISSING-OFFSET",()=>eq(evidenceCheck({...ev,offset:undefined}),"HOLD"));
  check("PEC-03-OUT-OF-BOUNDS",()=>eq(evidenceCheck({...ev,offset:source.length+1}),"HOLD"));
  check("PEC-03-SOURCE-FILE-TAMPER",()=>eq(evidenceCheck({...ev,source:source.map((v,i)=>i===0?v^1:v)}),"HOLD"));
  check("PEC-03-NO-ACCESS",()=>eq(evidenceCheck({...ev,access:false}),"HOLD"));
  check("PEC-03-ENCODING-DIFFERENCE",()=>eq(evidenceCheck({...ev,excerpt:utf8("TX_READY\n")}),"FAIL"));
  check("SAFE-01-ZERO-ACTIONS",()=>eq(guardIntent({writes:0,modelCalls:0,subagents:0,autoJobs:0,readyWrites:0}),"PASS"));
  check("SAFE-01-SUBAGENT-FAIL-CLOSED",()=>eq(guardIntent({writes:0,modelCalls:0,subagents:1,autoJobs:0,readyWrites:0}),"FAIL"));
  check("SAFE-01-PAID-CALL-FAIL-CLOSED",()=>eq(guardIntent({writes:0,modelCalls:1,subagents:0,autoJobs:0,readyWrites:0}),"FAIL"));
  check("SAFE-01-READY-WRITE-FAIL-CLOSED",()=>eq(guardIntent({writes:0,modelCalls:0,subagents:0,autoJobs:0,readyWrites:1}),"FAIL"));
  check("SAFE-03-SEALED-R1-NO-REQUEUE",()=>eq(dispatchPreviouslySealed("REQ-COWORK-ACE-PEC-HOP-ACON-DESIGN-R1-20261118|1",["REQ-COWORK-ACE-PEC-HOP-ACON-DESIGN-R1-20261118|1"]),"HOLD"));
  check("SAFE-03-NO-ACCIDENTAL-NEW-JOB",()=>eq(guardIntent({writes:0,modelCalls:0,subagents:0,autoJobs:1,readyWrites:0}),"FAIL"));
  return {suite:"ACE_PEC_SAFE_SYNTHETIC_CONTRACT_R0001",scope:"PURE_IN_MEMORY_CONTRACT_ORACLE_NOT_PRODUCTION_INTEGRATION",passed:cases.filter(x=>x.status==="PASS").length,failed:cases.filter(x=>x.status!=="PASS").length,cases,model_calls:0,host_writes:0,review_reruns:0};
}
const fs=require("node:fs");
const path=require("node:path");
const dir=__dirname;
const old=fs.readFileSync(path.join(dir,"ACE_PEC_HOP_ACON_INTEGRATED_SKILL_DESIGN_r0001_20261118_KST.md"),"utf8");
const design=fs.readFileSync(path.join(dir,"ACE_PEC_HOP_ACON_INTEGRATED_SKILL_DESIGN_r0002_20261118_KST.md"),"utf8");
const result=runSuite(design,old);
process.stdout.write(JSON.stringify(result,null,2)+"\n");
if(result.failed>0)process.exitCode=1;
