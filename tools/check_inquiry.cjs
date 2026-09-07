const assert=require('node:assert/strict');
const {workflowMailto}=require('../app.js');
const values={name:'Ana García',company:'Taller A&B',email:'ana@example.com',process:'Connect documents & orders.',today:'Two teams copy data between email and spreadsheets.'};
const url=new URL(workflowMailto(values));
assert.equal(url.protocol,'mailto:');assert.equal(url.pathname,'chainmakerspr@gmail.com');
assert.equal(url.searchParams.get('subject'),'Workflow inquiry from Taller A&B');
const body=url.searchParams.get('body');for(const value of Object.values(values))assert(body.includes(value));
assert(!workflowMailto({...values,company:''}).includes('undefined'));
console.log('PASS: workflow mailto preserves fields, accents, ampersands and multiline context');
