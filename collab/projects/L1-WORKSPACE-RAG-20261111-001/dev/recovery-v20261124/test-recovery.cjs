'use strict';
const assert=require('node:assert/strict'),view=require('../assets/recovery-view.js');
assert.equal(view.normalizeIndex(view.synthetic).length,1);
assert.equal(view.normalizeIndex({schema_version:1,derived:true,category:'Recovery',items:[{work_id:'../bad',id:'E-123456abcdef',provider:'l1-channel-recovery'}]}).length,0);
assert.throws(()=>view.normalizeIndex({schema_version:1,derived:false,category:'Recovery',items:[]}));
const good={work_id:'W-123',evidence_id:'E-123456abcdef',format:'html',sha256:'a'.repeat(64)};
assert.equal(view.safeArtifact(good,'W-123'),true);
for(const bad of [{...good,format:'javascript'},{...good,work_id:'DIFFERENT'},{...good,sha256:'bad'}])assert.equal(view.safeArtifact(bad,'W-123'),false);
console.log('PASS 6 Recovery normalization/integrity checks');
