import {predict} from './ml.js';

const $ = id => document.getElementById(id);
const examples = {
  scholarship: `Congratulations! You have been selected for an exclusive $3,000 student scholarship. You must transfer a refundable $75 verification deposit to our coordinator's personal bank account within 2 hours to secure it. Please do not contact the university office, as this is a confidential early release. Reply with your student ID and bank login details to receive your grant.`,
  job: `Hi, we reviewed your application and are offering you a remote internship paying $4,000 per week. No interview is needed. To receive your employment contract, buy our $180 training package today. Also send a photo of your ID and your one-time SMS code through this chat.`,
  safe: `The university careers office is accepting applications for the summer research internship. The application deadline is December 3. You can find the job description, eligibility requirements, and the application form on the official campus careers portal. There are no application fees and shortlisted candidates will be interviewed. For questions, contact the department through the university directory.`,
  zh: `恭喜你獲得本年度獎學金！請在今晚前先匯款新台幣 2,000 元保證金到私人帳戶，才能領取補助。名額有限，不要聯絡學校查證。請在LINE傳送身分證正反面、網銀密碼與簡訊驗證碼，逾時取消資格。`
};

// Evidence findings are independently defined transparent rules, not model explanations.
const signals = [
  {id:'credentials',title:'Credential or verification code request', re:/(?:one[ -]?time (?:SMS )?(?:passcode|password|code)|\bOTP\b|bank(?:ing)? (?:login|password|PIN)|student portal password|\bPIN\b|網銀(?:帳號)?密碼|銀行帳密|提款卡密碼|認證碼|驗證碼|校務系統帳號密碼)/iu, severe:true, why:'Legitimate processes should not require you to send passwords or one-time codes in a message.'},
  {id:'payment',title:'Upfront payment / deposit',re:/(?:refundable.{0,20}(?:deposit|fee)|(?:verification|processing|training|unlock|booking|activation|handling) (?:deposit|fee|charge|package)|(?:wire|transfer|pay|send|purchase|buy).{0,45}(?:deposit|fee|gift cards|crypto|personal account|training package)|(?:匯款|轉帳|支付|先繳|先付|購買|入金).{0,30}(?:保證金|手續費|驗證費|解鎖費|培訓|私人帳戶|個人帳戶|點數卡|加密貨幣)|保證金.{0,12}(?:匯款|轉帳))/iu, severe:true, why:'An upfront transfer tied to receiving a scholarship or job can be a strong warning sign.'},
  {id:'privacy',title:'Sensitive document request',re:/(?:photo of (?:your |both sides of )?(?:ID|passport|bank card)|passport scan|national ID|bank card photo|身分證正反面|證件照片|護照照片|金融卡資料|身分證字號)/iu,severe:true,why:'Identity documents can be misused. Verify the institution and use its legitimate secure submission process.'},
  {id:'secrecy',title:'Discouraging independent verification',re:/(?:do not contact (?:the )?(?:university|school)|don.t verify|confidential early release|keep.{0,24}(?:secret|confidential)|avoid the official|不要聯絡學校|請勿.{0,15}查證|不能向.{0,10}確認|不要詢問公司|機密.{0,13}不要|私下聯絡)/iu,severe:true,why:'An authentic institution should not penalize you for independently checking an offer.'},
  {id:'urgent',title:'Artificial time pressure',re:/(?:within (?:one|two|[0-9]+) hours?|before midnight|expires tonight|immediately|urgent|right now|today.{0,25}or lose|within 2 hours|今晚前|逾時取消|一小時內|兩小時內|立即|馬上|名額有限|否則取消資格)/iu,severe:false,why:'Tight deadlines can discourage verification. Check the deadline on an official source.'},
  {id:'offplatform',title:'Off-platform / personal payment channel',re:/(?:private (?:group|chat|message|wallet|link)|personal (?:bank )?account|personal e-wallet|through this chat|in (?:a )?LINE|私人(?:群組|帳戶|銀行帳號)|個人(?:帳戶|電子錢包)|LINE.{0,12}(?:提供|傳送)|私訊.{0,12}(?:提供|傳送))/iu,severe:false,why:'Official recruitment and scholarships typically have published, independently verifiable contact and submission channels.'},
  {id:'remote',title:'Remote-control software request',re:/(?:remote.control app|share your screen|遠端控制程式|遠端操作電腦)/iu,severe:true,why:'Do not install remote access software at the request of an unverified contact.'}
];
const negateRe = /(?:no|not|never|without|avoid|warn(?:s|ing)? against|不會|不需|不必|勿|沒有|無須|無需|不得|不要求|不收取|警告|勿相信)/iu;

let model = null;
let latest = null;

function findEvidence(input) {
  const matched=[];
  for (const signal of signals) {
    const m = signal.re.exec(input);
    if (!m) continue;
    const prefix=input.slice(Math.max(0,m.index-24),m.index);
    // Some warnings about scams mention the same dangerous keywords; negate them.
    if (/(?:no |not |never |without |不會|不需|不必|勿|沒有|無須|無需|不收取|不要求|避免|禁止|警告)/iu.test(prefix.slice(-15)) && signal.id!=='secrecy') continue;
    matched.push({...signal, text:m[0], index:m.index});
  }
  return matched.sort((a,b)=>Number(b.severe)-Number(a.severe)||a.index-b.index);
}

function riskLevel(score){
  return score>=.67 ? {title:'Elevated concern', color:'#d46b50',line:'The model detects wording often seen in suspicious opportunities.'}:
    score>=.43 ? {title:'Pause and verify',color:'#d69c36',line:'The message is ambiguous. Check the claims before acting.'}:
    {title:'Fewer risk signals',color:'#3c977a',line:'The model found fewer risky patterns. This does not establish authenticity.'};
}

function el(tag,className,text){ const node=document.createElement(tag);if(className) node.className=className;if(text!==undefined)node.textContent=text;return node; }
function wipe(node){while(node.firstChild)node.removeChild(node.firstChild);}
function escapeCopyPII(text) {
  return text
    .replace(/\b[A-Z][12][0-9]{8}\b/giu,'[REDACTED TAIWAN ID]')
    .replace(/\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b/giu,'[REDACTED EMAIL]')
    .replace(/(?:\+886[-\s]?)?09\d{2}[-\s]?\d{3}[-\s]?\d{3}\b/g,'[REDACTED PHONE]')
    .replace(/\b(?:\+?\d[\d -]{11,}\d)\b/g,'[REDACTED LONG NUMBER]');
}
function makeActions(found){
 const ids = new Set(found.map(x=>x.id));
 const actions=[];
 if(ids.has('payment')) actions.push('Do not transfer any deposit, fee, or gift-card code before independently verifying the offer.');
 if(ids.has('credentials')||ids.has('privacy')) actions.push('Do not share passwords, OTP codes, identity documents, or bank credentials in chat.');
 if(ids.has('remote')) actions.push('Do not install screen-sharing or remote-control software from this invitation.');
 actions.push('Find the institution or employer website yourself; use its published office contact to verify the offer and deadline.');
 if(ids.has('secrecy')||ids.has('urgent')) actions.push('Give yourself time to verify, even if the sender claims secrecy or urgency.');
 if(actions.length<3) actions.push('Compare the message with an official listing and ask for a written contract or program reference.');
 return actions.slice(0,4);
}
function renderResult(text){
 const output = predict(text,model);
 const evidence = findEvidence(text);
 const risk = riskLevel(output.score);
 const percentage=Math.round(100*output.score);
 const serious=evidence.filter(x=>x.severe).length;
 latest={text,output,evidence,risk,percentage};
 $('result-placeholder').hidden=true;
 $('result-content').hidden=false;
 $('score').textContent=String(percentage);
 $('risk-title').textContent=risk.title;
 $('risk-title').style.color=risk.color;
 $('risk-caption').textContent='ML signal from synthetic training • not a verified fraud probability';
 $('risk-ring').style.background=`conic-gradient(${risk.color} ${percentage*3.6}deg,#e8eee8 ${percentage*3.6}deg)`;
 $('risk-summary').textContent=serious>0?`${risk.line} ${serious} potentially serious check${serious===1?'':'s'} surfaced below.`:risk.line+' No high-severity rule matched; keep verifying independently.';
 $('evidence-count').textContent=evidence.length===1?'1 observed signal':`${evidence.length} observed signals`;
 wipe($('evidence-list'));
 if(!evidence.length){$('evidence-list').append(el('div','evidence-none','No rules-based warning phrase matched. A message can still be deceptive.'));}
 else{
  evidence.slice(0,4).forEach(s=>{
   const row=el('div','evidence-item');
   row.append(el('div','evidence-icon',s.severe?'!':'•'));
   const content=el('div','evidence-body');
   content.append(el('b','',s.title),el('p','',s.why),el('q','',`“${escapeCopyPII(s.text)}”`));row.append(content);$('evidence-list').append(row);
  });
  if(evidence.length>4)$('evidence-list').append(el('div','evidence-none',`+ ${evidence.length-4} more observed signals. See the report for the complete list.`));
 }
 wipe($('action-list'));
 makeActions(evidence).forEach(s=>$('action-list').append(el('li','',s)));
 $('counterfactual').hidden=true;
}
async function copyReport(){
 if(!latest)return;
 const lines=[
   'ProofBeforePay — Privacy-safe risk triage report',
   `Model risk signal: ${latest.percentage}/100 (${latest.risk.title}; NOT verified fraud probability)`,
   `Evidence: ${latest.evidence.length} observed rule-based signals`,
   ...latest.evidence.map((s,i)=>`${i+1}. ${s.title}: ${escapeCopyPII(s.text)}`),
   'Safer next steps:',...makeActions(latest.evidence).map((s,i)=>`${i+1}. ${s}`),
   'Model trained/tested on synthetic examples. False negatives and positives possible.',
   'Sanitized message:',escapeCopyPII(latest.text)
 ];
 const report=lines.join('\n');
 try {await navigator.clipboard.writeText(report);}catch{
   const holder=el('textarea');holder.value=report;document.body.append(holder);holder.select();document.execCommand('copy');holder.remove();
 }
 $('copy-report').textContent='✓ Redacted draft copied — review before sharing';
 setTimeout(()=>{$('copy-report').textContent='↗ Copy redacted report draft';},2800);
}
function runWhatIf(){
 if(!latest)return;
 const {evidence,text,percentage}=latest;
 const first=evidence[0];
 const box=$('counterfactual');box.hidden=false;wipe(box);
 if(!first){box.textContent='No observed phrase to remove. Try an example with a risk signal.';return;}
 const amended=text.slice(0,first.index)+text.slice(first.index+first.text.length);
 const next=Math.round(predict(amended,model).score*100);
 const heading=el('div','',`WHAT IF WE REMOVED: “${escapeCopyPII(first.text)}”`);heading.style.fontWeight='800';box.append(heading);
 box.append(el('p','',`ML signal: ${percentage}/100 → ${next}/100 (${next-percentage>=0?'+':''}${next-percentage} points). This is one local what-if experiment, not proof that other wording is safe.`));
 box.append(el('div','', 'The evidence cards are separate detection rules; deleting a phrase changes the model input, not the truth of the offer.'));
}
async function loadModel(){
 try{
  const response=await fetch('./model/model.json',{cache:'no-store'});
  if(!response.ok)throw new Error('Model request failed.');
  model=await response.json();
  if(model.features.length!==model.weights.length||model.idf.length!==model.features.length)throw new Error('Invalid model size.');
  $('model-status').innerHTML='<span class="tiny-indicator"></span> MODEL READY';
  $('analyze').disabled=false;
  $('metric-acc').textContent=Math.round(model.metrics.accuracy*100)+'%';
  $('metric-f1').textContent=model.metrics.f1.toFixed(2);
  $('metric-size').textContent=String(model.metrics.holdout_size);
  analyze();
 }catch(error){
  $('model-status').textContent='MODEL UNAVAILABLE';
  $('result-placeholder').querySelector('h3').textContent='The model could not load.';
  $('result-placeholder').querySelector('p').textContent='Run with a local web server (python -m http.server 8000) or deploy to a static host. We do not fabricate an AI result when the model is unavailable.';
  console.error('On-device model error:',error);
 }
}
function analyze(){
 const message=$('message').value.trim();
 if(!model||!message){return;}
 renderResult(message);
}
function selectExample(which){
 $('message').value=examples[which];
 $('char-count').textContent=`${$('message').value.length} / 5000`;
 document.querySelectorAll('.sample').forEach(b=>b.classList.toggle('active',b.dataset.example===which));
 if(model) analyze();
}
$('message').addEventListener('input',()=>{$('char-count').textContent=`${$('message').value.length} / 5000`;document.querySelectorAll('.sample').forEach(b=>b.classList.remove('active'));});
$('analyze').addEventListener('click',analyze);
$('message').addEventListener('keydown',e=>{if((e.metaKey||e.ctrlKey)&&e.key==='Enter')analyze();});
$('sample-buttons').addEventListener('click',e=>{const button=e.target.closest('[data-example]');if(button)selectExample(button.dataset.example);});
$('copy-report').addEventListener('click',copyReport);
$('what-if').addEventListener('click',runWhatIf);
selectExample('scholarship');
loadModel();
