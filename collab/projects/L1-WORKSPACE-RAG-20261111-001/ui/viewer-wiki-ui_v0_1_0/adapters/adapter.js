/* Presentation DTO only; not a host API or persistent metadata schema. */
window.WikiAdapter = (() => {
  'use strict';
  const source = window.WikiFixtures;
  const clone = value => JSON.parse(JSON.stringify(value));
  const find = id => {const doc=source.docs.find(d=>d.id===id);if(!doc)throw new Error('DOCUMENT_NOT_FOUND');return doc;};
  const nodes = new Map();
  function index(items){items.forEach(n=>{nodes.set(n.id,n);if(n.children)index(n.children);});}
  Object.values(source.trees).forEach(index);
  const summary = d => ({id:d.id,title:d.title,description:d.description,module:d.module,kind:d.kind,state:d.state});
  return Object.freeze({
    capabilities:Object.freeze({mode:'fixture',readOnly:true,searchScope:'SYNTHETIC_FIXTURE_ONLY',mscIsolationVerified:false}),
    async listRoots(view){if(!Object.hasOwn(source.trees,view))throw new Error('VIEW_NOT_FOUND');return clone(source.trees[view].map(({children,...n})=>({...n,hasChildren:!!children})));},
    async listChildren(nodeId){const n=nodes.get(nodeId);if(!n)throw new Error('NODE_NOT_FOUND');return clone((n.children||[]).map(({children,...child})=>({...child,hasChildren:!!children})));},
    async getDocument(docId){const d=find(docId);return clone({id:d.id,title:d.title,description:d.description,kind:d.kind,markdown:d.markdown||'',raw:d.raw||'',related:d.related||[]});},
    async getDocumentMeta(docId){const d=find(docId);return clone({module:d.module,state:d.state,path:d.path,workId:d.workId||null,owner:d.owner||null,updated:d.updated||null,sourceRevision:d.sourceRevision||null,publishedRevision:d.publishedRevision||null,validation:d.validation||null});},
    async getMscTarget(docId){const d=find(docId);return d.participants?{mode:'synthetic-placeholder',participants:d.participants,url:null,isolationVerified:false}:null;},
    async search(query){const q=String(query).trim().toLocaleLowerCase();return clone(source.docs.filter(d=>!q||[d.title,d.module,d.description,d.kind,d.markdown||''].join(' ').toLocaleLowerCase().includes(q)).map(summary));},
    async getSummary(docId){return clone(summary(find(docId)));}
  });
})();
