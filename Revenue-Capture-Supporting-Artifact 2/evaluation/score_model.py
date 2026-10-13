"""Score a saved first-pass response without changing the frozen fixtures or rules."""
import argparse, csv, hashlib, json
from pathlib import Path
from run_rules import score

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('response',type=Path)
args=parser.parse_args()
manifest=json.loads((ROOT/'manifest.json').read_text())
for name,expected in manifest['files'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected, f'Frozen file changed: {name}'
raw=json.loads(args.response.read_text())
predictions=raw['predictions']
labels=json.loads((ROOT/'labels.json').read_text())
ids=[p['id'] for p in predictions]
assert len(ids)==len(set(ids))==len(labels) and set(ids)==set(labels),'Missing, duplicate or extra cases'
for p in predictions:
    assert p['decision'] in ['propose','hold','exclude']
    assert isinstance(p['reason'],str) and p['reason'].strip()
    if p['decision']=='propose':
        assert type(p['amount_inr']) in [int,float] and p['amount_inr']>0
        assert isinstance(p['completion_id'],str)
    else:
        assert p['amount_inr'] is None and p['completion_id'] is None
results=json.loads((ROOT/'rules-results.json').read_text())
results['fresh_codex_evaluator']=score(predictions,labels)
(ROOT/'comparison-results.json').write_text(json.dumps(results,indent=2)+'\n')
by_model={p['id']:p for p in predictions}
baselines={name:{p['id']:p for p in json.loads((ROOT/f'{name}-predictions.json').read_text())['predictions']} for name in ['job_keyword','guarded_synonym']}
with (ROOT/'case-comparison.csv').open('w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['case','expected_decision','expected_amount_inr','expected_completion','job_keyword_exact','guarded_synonym_exact','model_exact','model_decision','model_amount_inr','model_completion','model_reason'])
    for k,v in labels.items():
        same=lambda p:all(p[x]==v[x] for x in ['decision','amount_inr','completion_id'])
        p=by_model[k]
        w.writerow([k,v['decision'],v['amount_inr'],v['completion_id'],same(baselines['job_keyword'][k]),same(baselines['guarded_synonym'][k]),same(p),p['decision'],p['amount_inr'],p['completion_id'],p['reason']])
print(json.dumps(results,indent=2))
