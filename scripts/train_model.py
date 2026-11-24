"""Train transparent, self-contained ML model with sklearn; browser does not need Python.
Usage: python scripts/build_dataset.py && python scripts/train_model.py
"""
import json, math
from pathlib import Path
from datetime import date
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score, confusion_matrix
ROOT=Path(__file__).resolve().parents[1]
def read(name):
    return [json.loads(line) for line in (ROOT/'data'/f'{name}.jsonl').read_text(encoding='utf8').splitlines()]
def main():
    train=read('train');test=read('holdout')
    assert not ({r['group'] for r in train}&{r['group'] for r in test})
    v=TfidfVectorizer(analyzer='char',ngram_range=(2,4),lowercase=True,sublinear_tf=True,min_df=2,max_features=11500)
    x=v.fit_transform([r['text'] for r in train]); y=[r['label'] for r in train]
    clf=LogisticRegression(C=3.5,max_iter=2000,random_state=12)
    clf.fit(x,y)
    preds=clf.predict(v.transform([r['text'] for r in test]))
    probs=clf.predict_proba(v.transform([r['text'] for r in test]))[:,1]
    metrics={
      'data_disclaimer':'Small, balanced synthetic bilingual scenario set. NOT an external or real-world performance estimate.',
      'train_size':len(train),'holdout_size':len(test),'train_groups':len({r['group'] for r in train}),
      'holdout_groups':len({r['group'] for r in test}),
      'accuracy':round(float(accuracy_score([r['label'] for r in test],preds)),3),
      'precision':round(float(precision_score([r['label'] for r in test],preds,zero_division=0)),3),
      'recall':round(float(recall_score([r['label'] for r in test],preds,zero_division=0)),3),
      'f1':round(float(f1_score([r['label'] for r in test],preds,zero_division=0)),3),
      'confusion_matrix_tn_fp_fn_tp':confusion_matrix([r['label'] for r in test],preds,labels=[0,1]).ravel().tolist(),
      'holdout_bilingual':{lang:{'correct':int(sum(int(p==r['label']) for p,r in zip(preds,test) if r['language']==lang)),
                                 'total':sum(r['language']==lang for r in test)} for lang in ('en','zh-TW')},
      'test_cases':[{'text':r['text'],'label':r['label'],'predicted':int(p),'score':round(float(s),4),'lang':r['language']} for r,p,s in zip(test,preds,probs)]
    }
    names=v.get_feature_names_out().tolist()
    model={
       'name':'ProofBeforePay-charTFIDF-logistic-v1',
       'created':'2026-11-25',
       'intended_use':'Educational triage of suspicious student opportunity messages, not proof of fraud',
       'score_meaning':'Uncalibrated synthetic-trained ML risk signal; not a verified probability of fraud',
       'algorithm':'TF-IDF character n-grams (2-4) + L2 logistic regression',
       'features':names,
       'idf':[round(float(x),8) for x in v.idf_],
       'weights':[round(float(x),8) for x in clf.coef_[0]],
       'intercept':round(float(clf.intercept_[0]),8),
       'ngram_min':2,'ngram_max':4,'sublinear_tf':True,
       'metrics':{k:value for k,value in metrics.items() if k!='test_cases'},
    }
    (ROOT/'model'/'model.json').write_text(json.dumps(model,ensure_ascii=False,separators=(',',':')),encoding='utf8')
    (ROOT/'model'/'evaluation.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf8')
    print('Model features',len(names),'accuracy',metrics['accuracy'],'f1',metrics['f1'],'confusion',metrics['confusion_matrix_tn_fp_fn_tp'])

if __name__=='__main__':main()
