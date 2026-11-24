import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {predict} from '../ml.js';
const model=JSON.parse(readFileSync(new URL('../model/model.json', import.meta.url),'utf8'));
const holdout=readFileSync(new URL('../model/evaluation.json', import.meta.url),'utf8');
const cases=JSON.parse(holdout).test_cases;
test('ML score is bounded and deterministic',()=>{
 for(const input of ['', 'Scholarship now!','恭喜獲獎，先匯款']){
  const score=predict(input,model).score;
  assert.ok(score>=0 && score<=1);
  assert.equal(predict(input,model).score,score);
 }
});
test('Browser-side inference reproduces Python sklearn held-out scores',()=>{
 for(const row of cases){
  const p=predict(row.text,model).score;
  assert.ok(Math.abs(p-row.score)<.00015,`score mismatch (${p} vs ${row.score}) for ${row.text}`);
 }
});
test('Model learns a difference between two clear examples',()=>{
 const bad=predict('Your scholarship is approved. Pay the verification deposit immediately and send your OTP code.',model).score;
 const okay=predict('Applications for the university scholarship are open through the official campus portal. No payments required.',model).score;
 assert.ok(bad>okay,`Expected risky (${bad}) > ordinary (${okay})`);
});
