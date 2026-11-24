/* L1 Recovery read view. Host adapters authorize all reads and MSC artifact openings. */
(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports)module.exports=api;
  if(root&&root.document){
    root.L1RecoveryViewer=api;
    root.document.addEventListener('DOMContentLoaded',()=>{
      const button=root.document.getElementById('recovery-open');
      if(button)button.addEventListener('click',()=>{root.location.hash='#/recovery';});
    },{once:true});
  }
})(typeof window==='undefined'?null:window,function(){
'use strict';
const ID=/^[A-Za-z0-9][A-Za-z0-9_.-]{0,99}$/;
const SHA=/^[0-9a-f]{64}$/;
const ACCEPTED=['html','svg','puml'];
const synthetic={schema_version:1,derived:true,category:'Recovery',items:[
  {work_id:'DEMO-REC-001',id:'E-123456abcdef',provider:'l1-channel-recovery',summary:'합성 예시 · 수정 CL에서 찾은 보호 조건 검토',code_rev:'fixture-only',integrity:'SYNTHETIC_ONLY',module:'NR L1 Tx',status:'검증 전',sha256:null,published_path:null}
]};
function normalizeIndex(payload){
  if(!payload||payload.schema_version!==1||payload.derived!==true||payload.category!=='Recovery'||!Array.isArray(payload.items)||payload.items.length>10000)throw Error('RECOVERY_INDEX_INVALID');
  const items=[];
  for(const raw of payload.items){
    if(!raw||typeof raw!=='object'||!ID.test(raw.work_id||'')||!/^E-[a-f0-9]{12}$/i.test(raw.id||'')||raw.provider!=='l1-channel-recovery')continue;
    items.push({workId:raw.work_id,evidenceId:raw.id,summary:String(raw.summary||'근거 요약 없음').slice(0,500),module:String(raw.module||'미분류').slice(0,80),status:String(raw.status||raw.confidence_state||'미확인').slice(0,100),sourceRev:String(raw.code_rev||'UNKNOWN').slice(0,140),integrity:String(raw.integrity||'UNKNOWN').slice(0,50),sha256:SHA.test(raw.sha256||'')?raw.sha256:null});
  }
  return items;
}
function safeArtifact(info,workId){
  return !!(info&&ID.test(workId)&&info.work_id===workId&&ID.test(info.evidence_id||'')&&ACCEPTED.includes(info.format)&&SHA.test(info.sha256||''));
}
function el(doc,tag,cls,text){const n=doc.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=String(text);return n;}
function render(hostContainer, host, options={}){
  const doc=hostContainer.ownerDocument;
  const isHost=!!(host&&host.capabilities&&host.capabilities.readOnly===true&&typeof host.getRecoveryIndex==='function');
  hostContainer.replaceChildren();
  const heading=el(doc,'h1',null,'Recovery 분석');
  const note=el(doc,'p','recovery-subtitle',isHost?'기존 Work/Evidence 기반 읽기 전용 분석 보기':'합성 화면 예시 · 업무 Viewer의 실제 조회 연결은 아직 확인되지 않았습니다.');
  const input=el(doc,'input','recovery-search');input.type='search';input.placeholder='Work ID · 모듈 · CL/PR · 상태 · 요약 검색';input.setAttribute('aria-label','Recovery 목록 검색');
  const status=el(doc,'p','recovery-status');status.setAttribute('role','status');
  const list=el(doc,'div','recovery-list');const detail=el(doc,'section','recovery-detail');detail.setAttribute('aria-label','Recovery 사례 상세');
  hostContainer.append(heading,note,input,status,list,detail);
  let items=[],sequence=0;
  function line(parent,title,value){const row=el(doc,'div','recovery-field');row.append(el(doc,'strong',null,title),el(doc,'span',null,value==null?'미확인':String(value)));parent.append(row);}
  async function openCase(item){
    const current=++sequence;detail.replaceChildren(el(doc,'h2',null,'사례 상세'),el(doc,'p',null,'근거를 확인하는 중…'));
    let data=null;
    if(isHost&&typeof host.getRecoveryCase==='function'){
      try{data=await host.getRecoveryCase(item.workId,item.evidenceId);}catch{data=null;}
    }
    if(current!==sequence)return;
    detail.replaceChildren(el(doc,'h2',null,'사례 상세'));
    line(detail,'Work ID',item.workId);line(detail,'Evidence ID',item.evidenceId);
    line(detail,'현재 대상 revision',item.sourceRev);line(detail,'원본 무결성',item.integrity);
    if(!data||data.work_id!==item.workId||data.evidence_id!==item.evidenceId){
      detail.append(el(doc,'p','recovery-warning','상세 분석 데이터가 없거나 Work/Evidence 식별이 불일치합니다. 원본을 추측해 표시하지 않습니다.'));
      return;
    }
    for(const [key,label] of [['seed','Seed · 수정 전후 원인'],['cause_rule','원인 규칙'],['coverage','기존 보호와 미커버 후보'],['decision','검사·Recovery 필요성 판정'],['limitations','미확인·시험 범위']]){
      if(data[key]!=null)line(detail,label,typeof data[key]==='string'?data[key]:JSON.stringify(data[key]));
    }
    if(data.edge&&data.edge.definition&&data.edge.evidence_id){
      line(detail,'Edge · 업무 GPT 정의',data.edge.definition);line(detail,'Edge 근거',data.edge.evidence_id);
    }else line(detail,'Edge','의미·Evidence 계약 미확정 — 임의 그래프 생성하지 않음');
    const links=el(doc,'section','recovery-msc');links.append(el(doc,'h3',null,'MSC · Seed 전후 / AS-IS / TO-BE'));
    const artifacts=Array.isArray(data.msc_artifacts)?data.msc_artifacts:[];
    let available=0;
    for(const artifact of artifacts.slice(0,50)){
      if(!safeArtifact(artifact,item.workId))continue;
      const row=el(doc,'div','recovery-artifact');row.append(el(doc,'span',null,(artifact.label||artifact.format).slice(0,100)));
      const btn=el(doc,'button',null,artifact.format.toUpperCase()+' 열기');btn.type='button';
      btn.disabled=!isHost||typeof host.openRecoveryArtifact!=='function';
      btn.title=btn.disabled?'업무 호스트의 승인된 MSC Artifact 열기 연결 필요':'서버 ACL과 검증된 Artifact 위치 확인 후 열기';
      btn.onclick=async()=>{btn.disabled=true;try{await host.openRecoveryArtifact({workId:item.workId,evidenceId:artifact.evidence_id,format:artifact.format,sha256:artifact.sha256});}catch{status.textContent='MSC 열기에 실패했습니다. 권한·원본 SHA·변환 결과를 확인하세요.';}finally{btn.disabled=false;}};
      row.append(btn);links.append(row);available++;
    }
    if(!available)links.append(el(doc,'p',null,'등록·검증된 MSC HTML/SVG/PUML 연결이 없습니다.'));
    detail.append(links);
    if(isHost&&typeof host.openWork==='function'){
      const btn=el(doc,'button','recovery-open-work','원본 Work/Evidence 열기');btn.type='button';btn.onclick=()=>host.openWork(item.workId,item.evidenceId);detail.append(btn);
    }
  }
  function draw(){list.replaceChildren();const q=input.value.trim().toLocaleLowerCase();let shown=0;for(const item of items){
    if(![item.workId,item.evidenceId,item.summary,item.module,item.status,item.sourceRev].join(' ').toLocaleLowerCase().includes(q))continue;
    const b=el(doc,'button','recovery-case');b.type='button';b.append(el(doc,'strong',null,item.summary),el(doc,'small',null,item.module+' · '+item.workId+' · '+item.status+' · '+item.sourceRev));b.onclick=()=>openCase(item);list.append(b);shown++;
  }status.textContent=shown+'건 / '+items.length+'건 · '+(isHost?'호스트 조회':'합성 데이터');if(!shown)list.append(el(doc,'p',null,'일치하는 사례가 없습니다.'));}
  input.oninput=draw;
  const done=(payload)=>{items=normalizeIndex(payload);draw();if(items.length)openCase(items[0]);};
  if(!isHost){done(synthetic);return Promise.resolve({mode:'synthetic',count:items.length});}
  status.textContent='Recovery 인덱스를 확인하는 중…';
  return Promise.resolve().then(()=>host.getRecoveryIndex()).then(payload=>{done(payload);return {mode:'host',count:items.length};},()=>{items=[];draw();detail.replaceChildren(el(doc,'p','recovery-warning','호스트 Recovery 인덱스를 읽지 못했습니다. 권한 또는 파생 인덱스를 확인하세요.'));return {mode:'blocked',count:0};});
}
return Object.freeze({render,normalizeIndex,safeArtifact,synthetic});
});