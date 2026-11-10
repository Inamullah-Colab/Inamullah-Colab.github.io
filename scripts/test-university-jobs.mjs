import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const source=fs.readFileSync('assets/js/university-jobs.js','utf8');
function run(now,deadline,status='open'){
 const label={textContent:'Checked open'},classes=[];
 const card={dataset:{jobDeadline:deadline,jobStatus:status},querySelector:()=>label,classList:{add:x=>classes.push(x)}};
 const FixedDate=class extends Date{constructor(...args){super(...(args.length?args:[now]));}};
 vm.runInNewContext(source,{Date:FixedDate,Intl,document:{querySelectorAll:()=>[card]}});
 return {label:label.textContent,classes};
}
assert.deepEqual(run('2026-11-10T12:00:00Z','2026-11-11'),{label:'Closes tomorrow',classes:['is-urgent']});
assert.equal(run('2026-11-10T12:00:00Z','2026-11-17').label,'Closes in 7 days');
assert.equal(run('2026-11-10T12:00:00Z','2026-11-18').label,'Checked open');
assert.equal(run('2027-07-01T23:30:00Z','2027-07-01').label,'Deadline passed');
assert.equal(run('2027-07-01T23:30:00Z','2027-07-02').label,'Closes today');
assert.equal(run('2026-11-10T12:00:00Z','2026-11-11','closed').label,'Closed');
assert.equal(run('2026-11-10T12:00:00Z','2026-11-11','unverified').label,'Needs recheck');
console.log('Deadline checks passed, including UK summer time, expired, closed and unverified states.');
