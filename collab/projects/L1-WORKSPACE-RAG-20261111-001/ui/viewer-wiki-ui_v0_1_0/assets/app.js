(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const adapter=window.WikiAdapter;
  document.querySelector('.skip-link').onclick=e=>{e.preventDefault();$('main').focus();$('main').scrollIntoView();};
  const icons={
    menu:'M4 6h16M4 12h16M4 18h16', close:'m6 6 12 12M6 18 18 6',search:'M21 21l-5-5M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0',
    layers:'m12 3 10 5-10 5L2 8l10-5ZM2 12l10 5 10-5M2 16l10 5 10-5', 'chevron-down':'m6 9 6 6 6-6','chevron-right':'m9 5 7 7-7 7',
    briefcase:'M8 6V4h8v2M3 7h18v14H3V7Zm0 6c6 3 12 3 18 0M10 13h4',
    'book-open':'M12 5C8 3 4 3 2 4v15c3-1 6-1 10 1 4-2 7-2 10-1V4c-3-1-6-1-10 1Zm0 0v15',
    folder:'M3 5h6l2 3h10v13H3V5',lock:'M6 10h12v11H6V10Zm3 0V6a3 3 0 0 1 6 0v4',
    shield:'m12 3 9 4v6c0 4-5 8-9 9-4-1-9-5-9-9V7l9-4Zm-4 9 3 3 5-6',
    link:'m9 15 6-6M8 16l-2 2a4 4 0 0 1-6-6l5-5a4 4 0 0 1 6 0M16 8l2-2a4 4 0 0 1 6 6l-5 5a4 4 0 0 1-6 0',
    'panel-right':'M3 3h18v18H3V3Zm12 0v18M18 8h.1M18 12h.1M18 16h.1',
    file:'M5 3h9l5 5v13H5V3Zm9 0v6h5M8 13h8M8 17h6',
    diagram:'M9 3h6v5H9V3ZM2 16h6v5H2v-5Zm14 0h6v5h-6v-5ZM12 8v4M5 16v-4h14v4',
    'check-circle':'m8 12 3 3 5-6M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0',
    'arrow-right':'M4 12h16m-6-6 6 6-6 6','arrow-left':'M20 12H4m6-6-6 6 6 6',code:'m8 7-5 5 5 5m8-10 5 5-5 5m-3-13-2 16',
    plus:'M12 5v14M5 12h14',minus:'M5 12h14',maximize:'M3 9V3h6m6 0h6v6m0 6v6h-6M9 21H3v-6',calendar:'M3 5h18v16H3V5Zm4-3v6m10-6v6M3 11h18'
  };
  function icon(name){const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox','0 0 24 24');svg.classList.add('icon');svg.setAttribute('aria-hidden','true');const p=document.createElementNS(svg.namespaceURI,'path');p.setAttribute('d',icons[name]||icons.file);svg.append(p);return svg;}
  document.querySelectorAll('[data-icon]').forEach(e=>e.append(icon(e.dataset.icon)));
  function el(tag,cls,text){const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e;}
  const states={PREVIEW:['PREVIEW','preview'],DRAFT:['DRAFT','draft'],PUBLISHED:['PUBLISHED · 예시','published'],NOT_VERIFIED:['미확인','unknown']};
  function badge(state){const s=states[state]||['미확인','unknown'];return el('span','badge badge-'+s[1],s[0]);}
  let currentView='work',currentDoc='rach-overview',renderVersion=0,treeVersion=0,searchVersion=0,mode='rendered',lastReturn='rach-overview',lastTrigger=null,observer=null;
  let activeNodeAncestors=new Set();
  const defaultDocs={work:'rach-overview',knowledge:'knowledge-rach',files:'rach-overview'};
  const viewLabels={work:'Work',knowledge:'Knowledge',files:'전체 파일'};
  const expandedByView={work:new Map(),knowledge:new Map(),files:new Map()};
  function href(id,view=currentView,section){return '#/'+view+'/'+encodeURIComponent(id)+(section?'?section='+encodeURIComponent(section):'');}
  function route(){try{const m=location.hash.match(/^#\/(work|knowledge|files)\/([^?]+)(?:\?(.*))?$/);return m?{view:m[1],id:decodeURIComponent(m[2]),section:new URLSearchParams(m[3]||'').get('section')}:{view:'work',id:'rach-overview'};}catch{return {view:'work',id:'invalid-route'};}}
  function navigate(id,view=currentView){location.hash=href(id,view);closePanels();}
  function makeLink(id,label,cls){const a=el('a',cls,label);a.href=href(id);return a;}
  function toast(message){$('toast').textContent=message;$('toast').hidden=false;clearTimeout(toast.timer);toast.timer=setTimeout(()=>$('toast').hidden=true,2400);}
  function closePanels(restore=true){document.querySelectorAll('.panel-open').forEach(e=>e.classList.remove('panel-open'));document.body.classList.remove('panel-active');$('panel-backdrop').hidden=true;$('tree-toggle').setAttribute('aria-expanded','false');$('meta-toggle').setAttribute('aria-expanded','false');if(restore&&lastTrigger)lastTrigger.focus();lastTrigger=null;}
  function openPanel(id,trigger){closePanels(false);lastTrigger=trigger;$(id).classList.add('panel-open');document.body.classList.add('panel-active');$('panel-backdrop').hidden=false;trigger.setAttribute('aria-expanded','true');$(id).querySelector('button,a')?.focus();}
  $('tree-toggle').onclick=()=>openPanel('sidebar',$('tree-toggle'));
  $('meta-toggle').onclick=()=>openPanel('right-panel',$('meta-toggle'));
  document.querySelectorAll('[data-close-panel]').forEach(b=>b.onclick=()=>closePanels());$('panel-backdrop').onclick=()=>closePanels();
  document.addEventListener('keydown',e=>{if(e.key==='Escape'){closePanels();}if(document.body.classList.contains('panel-active')&&e.key==='Tab'){const panel=document.querySelector('.panel-open');const focusable=[...panel.querySelectorAll('button,a[href],input,[tabindex="0"]')].filter(x=>!x.closest('[hidden]'));const first=focusable[0],last=focusable.at(-1);if(e.shiftKey&&document.activeElement===first){last.focus();e.preventDefault();}else if(!e.shiftKey&&document.activeElement===last){first.focus();e.preventDefault();}}if(e.key==='/'&&!e.ctrlKey&&!e.metaKey&&!/INPUT|TEXTAREA/.test(e.target.tagName)&&!document.querySelector('dialog[open]')){e.preventDefault();openSearch();}});
  const wideMedia=matchMedia('(min-width:1041px)');wideMedia.addEventListener('change',()=>closePanels());
  document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>navigate(defaultDocs[b.dataset.view],b.dataset.view));
  async function buildTree(){
    const token=++treeVersion;const view=currentView;const roots=await adapter.listRoots(view);
    async function build(items){const ul=el('ul','tree-level');for(const n of items){const li=el('li');const row=el('div','tree-row');li.append(row);
      if(n.hasChildren){const btn=el('button','tree-expander');btn.append(icon('chevron-right'));btn.setAttribute('aria-label',n.title+' 펼치기/접기');const label=el('span','tree-group-label',n.title);row.append(btn,label);const children=await build(await adapter.listChildren(n.id));li.append(children);const contains=!!children.querySelector('[data-selected="true"]');if(contains)activeNodeAncestors.add(n.id);const expanded=expandedByView[view].get(n.id)??(contains||view==='knowledge');children.hidden=!expanded;btn.setAttribute('aria-expanded',String(expanded));btn.onclick=()=>{const next=btn.getAttribute('aria-expanded')!=='true';btn.setAttribute('aria-expanded',String(next));children.hidden=!next;expandedByView[view].set(n.id,next);};
      }else{row.append(el('span','tree-leaf-space'));const a=el('a');a.href=href(n.docId,view);a.append(icon(n.docId.startsWith('msc-')?'diagram':'file'),el('span',null,n.title));if(n.docId===currentDoc){a.setAttribute('aria-current','page');a.dataset.selected='true';}a.onclick=()=>closePanels(false);row.append(a);}ul.append(li);}return ul;}
    const tree=await build(roots);if(token===treeVersion)$('page-tree').replaceChildren(tree);
  }
  function metadata(meta){const box=$('metadata');box.replaceChildren(el('h2',null,'문서 정보'));const dl=el('dl');const fields=[['Work ID',meta.workId],['모듈',meta.module],['검증 상태',meta.validation==='SYNTHETIC_ONLY'?'합성 예시만 확인':'미확인'],['원본 revision',meta.sourceRevision],['그룹 게시 revision',meta.publishedRevision],['원본 경로',meta.path]];
    fields.forEach(([k,v])=>{dl.append(el('dt',null,k),el('dd',k.includes('revision')||k.includes('경로')?'mono':null,v||'미확인'));});box.append(dl,el('p','meta-note','이 패널의 값은 합성 예시입니다. 실제 필드와 연결은 현장 계약을 확인해 매핑해요.'));
  }
  function buildToc(headings){const toc=$('toc');toc.replaceChildren();for(const h of headings){const a=el('a',h.level>2?'toc-sub':null,h.title);a.href=href(currentDoc,currentView,h.id);a.onclick=e=>{e.preventDefault();history.replaceState(null,'',a.href);$(h.id)?.scrollIntoView({block:'start',behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth'});closePanels(false);$(h.id)?.setAttribute('tabindex','-1');$(h.id)?.focus({preventScroll:true});};a.dataset.heading=h.id;toc.append(a);}if(observer)observer.disconnect();if(headings.length){toc.firstChild.classList.add('active');observer=new IntersectionObserver(entries=>{for(const entry of entries){if(entry.isIntersecting){toc.querySelectorAll('a').forEach(a=>a.classList.toggle('active',a.dataset.heading===entry.target.id));}}},{rootMargin:'-100px 0px -65% 0px'});headings.forEach(h=>observer.observe($(h.id)));}}
  function button(label,ic,fn,primary=false){const b=el('button',primary?'primary-button':'soft-button');b.append(icon(ic),el('span',null,label));b.onclick=fn;return b;}
  function showError(){document.body.classList.remove('msc-mode');$('document-layout').hidden=false;$('doc-eyebrow').replaceChildren(el('span',null,'DOCUMENT'));$('doc-title').textContent='문서를 불러오지 못했어요';$('doc-description').textContent='주소나 조회 권한을 확인한 뒤 다시 시도해 주세요.';$('doc-byline').replaceChildren();$('doc-actions').replaceChildren(button('다시 시도','arrow-right',()=>render()),button('시작 문서로','arrow-left',()=>navigate('rach-overview','work')));$('article').replaceChildren(el('div','state-card','문서가 없거나 현재 연결에서 읽을 수 없습니다.'));$('related').replaceChildren();$('toc').replaceChildren();$('metadata').replaceChildren(el('p','meta-note','문서 메타정보 미확인'));$('breadcrumbs').replaceChildren(el('span',null,'문서 조회 오류'));document.title='문서 조회 오류 · L1 Workspace';}
  async function render(){
    const r=route();const old=currentDoc;currentView=r.view;currentDoc=r.id;mode='rendered';if(!old.startsWith('msc-')&&currentDoc.startsWith('msc-'))lastReturn=old;
    const token=++renderVersion;$('loading').hidden=false;$('document-layout').hidden=true;document.querySelectorAll('[data-view]').forEach(b=>b.dataset.view===currentView?b.setAttribute('aria-current','page'):b.removeAttribute('aria-current'));$('tree-title').textContent=({work:'WORK 페이지',knowledge:'MODULE / FEATURE / SCENARIO',files:'전체 콘텐츠'})[currentView];
    buildTree().catch(()=>{$('page-tree').replaceChildren(el('p','meta-note','탐색 목록을 불러오지 못했어요.'));});
    try{const [doc,meta,msc]=await Promise.all([adapter.getDocument(currentDoc),adapter.getDocumentMeta(currentDoc),adapter.getMscTarget(currentDoc)]);if(token!==renderVersion)return;
      $('doc-title').textContent=doc.title;$('doc-description').textContent=doc.description||'';$('doc-eyebrow').replaceChildren(el('span',null,(meta.module||'문서')+' / '+doc.kind),badge(meta.state));
      $('doc-byline').replaceChildren(el('span','mini-avatar','예시'),el('span',null,meta.owner||'담당 미확인'),el('span','byline-dot','·'),el('span',null,meta.updated?meta.updated+' · 합성 예시':'업데이트 미확인'),el('span','byline-dot','·'),el('span',null,'읽기 전용'));
      $('breadcrumbs').replaceChildren();const root=el('a',null,viewLabels[currentView]);root.href=href(defaultDocs[currentView]);$('breadcrumbs').append(root,icon('chevron-right'),el('span',null,meta.module||'미확인'),icon('chevron-right'),el('span',null,doc.title));
      metadata(meta);document.title=doc.title+' · L1 Workspace';$('doc-actions').replaceChildren();document.body.classList.toggle('msc-mode',doc.kind==='MSC');let headings=[];
      if(doc.kind==='MSC') {renderMsc(msc);$('doc-actions').append(button('문서로 돌아가기','arrow-left',()=>navigate(lastReturn)),button('링크 복사','link',copyLink));}
      else{const rawButton=button('원문 보기','code',()=>{mode=mode==='raw'?'rendered':'raw';rawButton.querySelector('span').textContent=mode==='raw'?'본문 보기':'원문 보기';if(mode==='raw'){const wrap=el('div','code-block');const pre=el('pre');pre.tabIndex=0;pre.textContent=doc.markdown||doc.raw||'텍스트 미리보기를 지원하지 않는 형식입니다.';wrap.append(pre);$('article').replaceChildren(wrap);buildToc([]);}else{renderContent();} });$('doc-actions').append(rawButton,button('링크 복사','link',copyLink));
        if(doc.related?.some(id=>id.startsWith('msc-')))$('doc-actions').append(makeLink('msc-six','MSC 시나리오','soft-button'));
        function renderContent(){if(doc.kind==='JSON'){const wrap=el('div','code-block');const pre=el('pre');pre.tabIndex=0;pre.textContent=doc.raw;wrap.append(pre);$('article').replaceChildren(wrap);headings=[];}
          else if(doc.kind==='BINARY'){$('article').replaceChildren(el('div','state-card','이 파일 형식은 미리보기를 지원하지 않아요. 실제 서비스의 허용된 파일 핸들러를 연결해 주세요.'));headings=[];}
          else headings=window.WikiMarkdown.render($('article'),doc.markdown,id=>href(id));buildToc(headings);}
        renderContent();
      }
      const summaries=await Promise.all(doc.related.map(id=>adapter.getSummary(id).catch(()=>null)));if(token!==renderVersion)return;const rel=$('related');rel.replaceChildren();if(summaries.filter(Boolean).length){const h=el('h2',null);h.append(icon('link'),el('span',null,'이어서 읽기'));const grid=el('div','related-grid');summaries.filter(Boolean).forEach(s=>{const a=makeLink(s.id,'','related-card');const label=el('span',null,s.title);label.append(el('small',null,s.module+' · '+s.kind));a.append(icon(s.kind==='MSC'?'diagram':'file'),label);const arrow=icon('arrow-right');arrow.classList.add('arrow');a.append(arrow);grid.append(a);});rel.append(h,grid);}
      $('document-layout').hidden=false;if(r.section){requestAnimationFrame(()=>$(r.section)?.scrollIntoView({block:'start'}));}else window.scrollTo(0,0);
    }catch{if(token===renderVersion)showError();}finally{if(token===renderVersion)$('loading').hidden=true;}
  }
  async function copyLink(){try{await navigator.clipboard.writeText(location.href);toast('문서 링크를 복사했어요.');}catch{toast('링크 복사가 지원되지 않아요. 주소창의 URL을 복사해 주세요.');}}
  $('copy-link').onclick=copyLink;
  function renderMsc(target){
    const article=$('article');article.replaceChildren();buildToc([]);const notice=el('div','msc-notice','합성 MSC 레이아웃 · doc-converter 원본 아님. 실제 MSC HTML은 별도 origin·sandbox·CSP 검증 후 기존 핸들러에 연결해요.');article.append(notice);
    if(!target||target.mode!=='synthetic-placeholder'){article.append(el('div','state-card','MSC 연결이 검증되지 않아 열 수 없어요.'));return;}
    const n=target.participants===12?12:6;const baseWidth=n*142+70;let scale=1;
    const controls=el('div','msc-controls');const percent=el('span','zoom-value','100%');const scroll=el('div','msc-scroll');scroll.tabIndex=0;scroll.setAttribute('role','region');scroll.setAttribute('aria-label',n+'명 참가자 합성 MSC, 가로·세로 스크롤 가능');
    const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.classList.add('msc-canvas');svg.setAttribute('viewBox',`0 0 ${baseWidth} 590`);svg.setAttribute('role','img');svg.setAttribute('aria-label',n+'명 합성 참가자의 요청·확인·응답 흐름');
    function shape(tag,attrs,text){const e=document.createElementNS(svg.namespaceURI,tag);Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,String(v)));if(text)e.textContent=text;svg.append(e);return e;}
    const names=['요청 주체','상태 관리','설정 관리','전달 계층','응답 처리','확인 주체','확장 A','확장 B','확장 C','확장 D','확장 E','확장 F'];
    for(let j=0;j<n;j++){const x=45+j*142;shape('rect',{x,y:24,width:120,height:39,rx:7,fill:j%2?'#f2effb':'#edf3fc',stroke:'#dedfea'});shape('text',{x:x+60,y:49,'text-anchor':'middle','font-size':11,fill:'#665e80','font-family':'sans-serif'},names[j]);shape('line',{x1:x+60,y1:65,x2:x+60,y2:550,stroke:'#dedfea','stroke-dasharray':'4 5'});}
    const messages=['1. 요청 조건 확인 (합성)','2. 상태 조회 (합성)','3. 설정 전달 (합성)','4. 적용 확인 (합성)','5. 응답 확인 (합성)','6. 검토 결과 연결 (합성)'];
    messages.forEach((message,j)=>{const from=j%(n-1),to=(j+1)%(n-1)+1;const x1=105+from*142,x2=105+to*142,y=124+j*68;shape('text',{x:(x1+x2)/2,y:y-12,'text-anchor':'middle','font-size':10,fill:'#7c719b','font-family':'sans-serif'},message);shape('line',{x1,y1:y,x2,y2:y,stroke:'#9382bf','stroke-width':1.5});shape('path',{d:`M${x2-6} ${y-4} L${x2} ${y} L${x2-6} ${y+4}`,fill:'none',stroke:'#9382bf','stroke-width':1.5});});
    function applyScale(value){scale=Math.min(2,Math.max(.2,value));svg.style.width=Math.round(baseWidth*scale)+'px';svg.style.height=Math.round(590*scale)+'px';percent.textContent=Math.round(scale*100)+'%';}
    controls.append(button('축소','minus',()=>applyScale(scale-.15)),percent,button('확대','plus',()=>applyScale(scale+.15)),button('폭 맞춤','maximize',()=>applyScale(scroll.clientWidth/baseWidth)),button('100%','maximize',()=>applyScale(1)));
    const details=el('details','msc-phase');details.open=true;details.append(el('summary',null,'Phase 1 · 재진입 조건 확인부터 상태 대조 및 설정 전달·응답 검토까지의 긴 단계명 예시'),el('p',null,'이 영역의 접기는 설명만 제어합니다. 실제 MSC의 단계·메시지·participant 의미는 변경하지 않아요.'));
    scroll.append(svg);article.append(controls,details,scroll);applyScale(1);
  }
  async function runSearch(){const token=++searchVersion;try{const docs=await adapter.search($('search-input').value);if(token!==searchVersion)return;$('search-count').textContent=docs.length+'개 문서';const box=$('search-results');box.replaceChildren();if(!docs.length)box.append(el('p','search-empty','일치하는 예시 문서가 없어요. 다른 검색어를 입력해 주세요.'));for(const d of docs){const b=el('button','search-result');const text=el('span');text.append(el('strong',null,d.title),el('small',null,d.module+' · '+d.kind));b.append(icon(d.kind==='MSC'?'diagram':'file'),text,badge(d.state));b.onclick=()=>{$('search-dialog').close();navigate(d.id);};box.append(b);}}catch{$('search-results').replaceChildren(el('p','search-empty','검색을 불러오지 못했어요. 다시 시도해 주세요.'));}}
  function openSearch(){$('search-dialog').showModal();$('search-input').value='';$('search-input').focus();runSearch();}
  $('search-dialog').addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();e.stopPropagation();$('search-dialog').close();}});
  $('search-open').onclick=openSearch;$('search-close').onclick=()=>$('search-dialog').close();$('search-input').oninput=runSearch;
  $('about-open').onclick=()=>$('about-dialog').showModal();$('about-close').onclick=()=>$('about-dialog').close();
  window.addEventListener('hashchange',()=>{closePanels(false);render();});
  if(!location.hash)history.replaceState(null,'',href('rach-overview','work'));render();
})();
