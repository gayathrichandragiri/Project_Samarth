import pandas as pd
from data_fetcher import load_all_samples
from normalizer import normalize_rainfall_df, normalize_crop_df
import numpy as np

FRAMES, METAS = load_all_samples()
RAIN_DF = normalize_rainfall_df(FRAMES['sample_rainfall.csv'])  #rainfall
CROP_DF = normalize_crop_df(FRAMES['sample_crop_production.csv']) #crop production

def _avg_rainfall_by_state(state, years):
    sub = RAIN_DF[(RAIN_DF.state.str.lower()==state.lower()) & (RAIN_DF.year.isin(years))]
    if sub.empty:
        return None, []
    vals = sub.groupby('year')['rainfall_mm'].sum().reset_index()  # sum monthly -> annual
    avg = float(vals['rainfall_mm'].mean())
    # citation
    cit = {
        'dataset_title': METAS['sample_rainfall.csv']['title'],
        'dataset_url': METAS['sample_rainfall.csv']['url'],
        'aggregation': f"annual rainfall summed from monthly records for state={state}, years={years}"
    }
    return avg, cit

def _top_crops_by_state(state, years, topk=3):
    sub = CROP_DF[(CROP_DF.state.str.lower()==state.lower()) & (CROP_DF.year.isin(years))]
    if sub.empty:
        return [], None
    agg = sub.groupby('crop')['production_tonnes'].sum().reset_index().sort_values('production_tonnes', ascending=False)
    top = agg.head(topk).to_dict(orient='records')
    cit = {
        'dataset_title': METAS['sample_crop_production.csv']['title'],
        'dataset_url': METAS['sample_crop_production.csv']['url'],
        'aggregation': f"sum(production_tonnes) grouped by crop for state={state}, years={years}"
    }
    return top, cit

def parse_years_from_question(q):
    # naive: if "last N years" present return last N years from data; else use available years
    import re
    m = re.search(r'last (\d+) years', q.lower())
    years = sorted(RAIN_DF['year'].unique())
    if m:
        n = int(m.group(1))
        return years[-n:]
    return years

def answer_question(q):
    ql = q.lower()
    years = parse_years_from_question(q)
    # example: detect "compare average annual rainfall in X and Y" and "top M crops"
    import re
    state_matches = re.findall(r'in ([a-zA-Z ]+?) and ([a-zA-Z ]+?) for', q)
    if state_matches:
        s1, s2 = state_matches[0][0].strip(), state_matches[0][1].strip()
        avg1, cit1 = _avg_rainfall_by_state(s1, years)
        avg2, cit2 = _avg_rainfall_by_state(s2, years)
        # detect top M
        m = re.search(r'top (\d+) most produced crops', q)
        topk = int(m.group(1)) if m else 3
        top1, topcit1 = _top_crops_by_state(s1, years, topk)
        top2, topcit2 = _top_crops_by_state(s2, years, topk)
        answer = {
            'answer_text': f"Average annual rainfall {s1}: {avg1} mm; {s2}: {avg2} mm (years: {list(years)})",
            'details':{
                s1: {'avg_rainfall_mm': avg1, 'top_crops': top1},
                s2: {'avg_rainfall_mm': avg2, 'top_crops': top2}
            },
            'citations':[cit1, cit2, topcit1, topcit2]
        }
        return answer
 
    return {'answer_text':'Sorry — this prototype recognized no complex pattern. Try: "Compare average annual rainfall in State_X and State_Y for the last N years and list top M most produced crops."'}
