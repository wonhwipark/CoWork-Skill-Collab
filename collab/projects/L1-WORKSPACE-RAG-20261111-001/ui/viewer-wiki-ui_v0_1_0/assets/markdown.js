/* Deliberately restricted Markdown, built only with DOM APIs. Raw HTML stays text. */
window.WikiMarkdown = (() => {
  'use strict';
  function inline(parent,text,onDoc){
    const pattern=/(`[^`]+`|\*\*[^*]+\*\*|\[[^\]]+\]\([^)]+\))/g;
    let start=0;
    for(const match of text.matchAll(pattern)){
      parent.append(document.createTextNode(text.slice(start,match.index)));
      const token=match[0];let e;
      if(token.startsWith('`')){e=document.createElement('code');e.textContent=token.slice(1,-1);}
      else if(token.startsWith('**')){e=document.createElement('strong');e.textContent=token.slice(2,-2);}
      else {const m=token.match(/^\[([^\]]+)\]\(([^)]+)\)$/); const target=m[2];
        if(/^doc:[a-z0-9-]+$/.test(target)){e=document.createElement('a');e.href=onDoc(target.slice(4));}
        else {e=document.createElement('span');e.className='blocked-link';e.title='이 데모에서 허용하지 않는 링크';}
        e.textContent=m[1];
      }
      parent.append(e);start=match.index+token.length;
    }
    parent.append(document.createTextNode(text.slice(start)));
  }
  function render(container,source,onDoc){
    container.replaceChildren();const headings=[];const lines=String(source).slice(0,500000).split(/\r?\n/);let i=0;
    while(i<lines.length){const line=lines[i];if(!line.trim()){i++;continue;}
      if(line.startsWith('```')){const wrap=document.createElement('div');wrap.className='code-block';const label=document.createElement('div');label.className='code-label';label.textContent=line.slice(3)||'text';const pre=document.createElement('pre');pre.tabIndex=0;pre.setAttribute('aria-label','코드 예시, 가로 스크롤 가능');const code=document.createElement('code');const buf=[];i++;while(i<lines.length&&!lines[i].startsWith('```'))buf.push(lines[i++]);code.textContent=buf.join('\n');pre.append(code);wrap.append(label,pre);container.append(wrap);i++;continue;}
      const heading=line.match(/^(#{1,3})\s+(.+)$/);if(heading){const level=heading[1].length;const h=document.createElement('h'+level);h.id='section-'+(headings.length+1);inline(h,heading[2],onDoc);container.append(h);headings.push({id:h.id,title:heading[2],level});i++;continue;}
      if(line.startsWith('>')){const block=document.createElement('blockquote');while(i<lines.length&&lines[i].startsWith('>')){const p=document.createElement('p');inline(p,lines[i++].replace(/^>\s?/,''),onDoc);block.append(p);}container.append(block);continue;}
      if(line.startsWith('|')&&i+1<lines.length&&/^\|[\s:|\-]+\|\s*$/.test(lines[i+1])){const wrap=document.createElement('div');wrap.className='table-scroll';wrap.tabIndex=0;wrap.setAttribute('role','region');wrap.setAttribute('aria-label','문서 표, 가로 스크롤 가능');const table=document.createElement('table');let row=0;while(i<lines.length&&lines[i].startsWith('|')){if(row===1){i++;row++;continue;}const section=document.createElement(row===0?'thead':'tbody');const tr=document.createElement('tr');const cells=lines[i++].trim().replace(/^\||\|$/g,'').split('|');for(const cell of cells){const td=document.createElement(row===0?'th':'td');if(row===0)td.scope='col';inline(td,cell.trim(),onDoc);tr.append(td);}section.append(tr);table.append(section);row++;}wrap.append(table);container.append(wrap);continue;}
      if(/^(- |\d+\. )/.test(line)){const ordered=/^\d+\./.test(line);const list=document.createElement(ordered?'ol':'ul');while(i<lines.length&&(ordered?/^\d+\. /:/^- /).test(lines[i])){const li=document.createElement('li');inline(li,lines[i++].replace(/^(- |\d+\. )/,''),onDoc);list.append(li);}container.append(list);continue;}
      const p=document.createElement('p');inline(p,line,onDoc);container.append(p);i++;
    }
    return headings;
  }
  return Object.freeze({render});
})();
