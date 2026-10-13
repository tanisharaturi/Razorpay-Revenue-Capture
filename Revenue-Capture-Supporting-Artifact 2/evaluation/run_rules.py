"""Transparent baselines. Frozen before viewing any live-model output; not production code."""
import json,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ALIASES={
 'extra unloading':['extra unloading','unloading assistance','offloading assistance'],
 'apply festive sleeves':['apply festive sleeves','festive sleeves','festival pack adaptation'],
 'pallet wrapping':['pallet wrapping','stretch film','shrink wrap'],
 'carton relabelling':['carton relabelling','replacement barcode labels'],
 'extra labour':['extra labour','extra labor','additional unloading labour'],
 'bank reconciliation':['bank reconciliation','bank feed reconciliation'],
 'two social video cutdowns':['social video cutdowns','video cutdowns'],
 'subtitle synchronisation':['subtitle synchronisation','subtitle synchronization'],
 'carpet shampoo':['carpet shampoo','carpet shampooing'],
}
def prediction(c,decision='hold',amount=None,rid=None,reason='Insufficient or ambiguous support'):
 return {'id':c['id'],'decision':decision,'amount_inr':amount,'completion_id':rid,'reason':reason}
def amount_for(c,r):
 p=c['approval']['pricing'];units=r['units']
 if p['mode']=='fixed':return p['fixed_amount'] if units==p['approved_units'] else None
 if p['mode']=='unit':return units*p['rate'] if units<=p['approved_units'] else None
 if p['mode']=='hourly':
  hours=r['hours']
  return None if hours is None or units!=p['workers'] else max(0,hours-p['included_hours'])*p['workers']*p['rate']
def baseline(c,strong):
 a=c['approval'];service=a['service'].lower();terms=ALIASES.get(service,[service]) if strong else [service]
 approval=a['text'].lower();updates=' '.join(m['text'] for m in c['later_messages']).lower()
 # Exact phrases, common completion states, and standard commercial safeguards.
 if any(x in updates for x in ['waived','bundled','no additional charge','included in the original fee']):return prediction(c,'exclude',reason='Explicit waiver or bundling')
 if any(any(x in line['description'].lower() for x in terms) for line in c['billing_lines']):return prediction(c,'exclude',reason='Existing invoice description matches service')
 if any(x in approval for x in ['quote only','approval pending']):return prediction(c)
 if any(x in updates for x in ['dispute','not completed','not delivered','identity is unresolved']):return prediction(c)
 if not c['billing_register_complete']:return prediction(c)
 matches=[]
 for r in c['completion_candidates']:
  if r['customer']!=a['customer'] or r['job_id'] not in [None,a['job_id']]:continue
  if not strong and r['job_id']!=a['job_id']:continue
  if r['batch']!=a['batch']:continue
  note=r['completion_note'].lower()
  if any(x in note for x in ['not completed','cancelled','canceled','pending','scheduled']):continue
  if 'completed' not in note:continue
  if a['customer_ack_required'] and 'customer acknowledged' not in note:continue
  if not any(x in r['description'].lower() for x in terms):continue
  amount=amount_for(c,r)
  if amount is None or amount<=0 or amount>a['pricing']['max_amount']:continue
  matches.append((r['id'],amount))
 if len(matches)!=1:return prediction(c)
 rid,amount=matches[0];return prediction(c,'propose',amount,rid,'Unique matching completion, approval and pricing gates passed')
def score(preds,labels):
 by={p['id']:p for p in preds};fields=['decision','amount_inr','completion_id']
 exact=sum(all(by[k][f]==v[f] for f in fields) for k,v in labels.items())
 proposed=[k for k,p in by.items() if p['decision']=='propose']
 unsafe=[k for k in proposed if labels[k]['decision']!='propose']
 tp=sum(labels[k]['decision']=='propose' for k in proposed);positives=sum(v['decision']=='propose' for v in labels.values())
 return {'exact_case_correct':exact,'n':len(labels),'false_proposals':len(unsafe),'false_proposal_cases':unsafe,'valid_proposals':tp,'proposals':len(proposed),'eligible_cases':positives,'missed_eligible_cases':positives-tp,'proposal_precision':tp/len(proposed) if proposed else None,'proposal_recall':tp/positives,'wrong_cases':[k for k,v in labels.items() if not all(by[k][f]==v[f] for f in fields)]}
if __name__=='__main__':
 cases=json.loads((ROOT/'cases.json').read_text());labels=json.loads((ROOT/'labels.json').read_text());summary={}
 for name,strong in [('job_keyword',False),('guarded_synonym',True)]:
  preds=[baseline(c,strong) for c in cases];(ROOT/f'{name}-predictions.json').write_text(json.dumps({'predictions':preds},indent=2));summary[name]=score(preds,labels)
 (ROOT/'rules-results.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
