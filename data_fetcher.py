import pandas as pd
import os, json
DATA_DIR = 'data_files'
os.makedirs(DATA_DIR, exist_ok=True)

def load_csv_local(filename):
    path = os.path.join(DATA_DIR, filename)
    df = pd.read_csv(path)
    meta = {
        'title': filename,
        'url': f'file://{path}',
        'downloaded_at': None,
        'original_file': path
    }
    return df, meta

# registry loader
def load_all_samples():
    # sample filenames used in this prototype
    samples = [
        ('sample_rainfall.csv','Sub‑Divisional Monthly Rainfall (sample)'),
        ('sample_crop_production.csv','District Crop Production (sample)')
    ]
    frames = {}
    metas = {}
    for fname, title in samples:
        df, meta = load_csv_local(fname)
        meta['title'] = title
        metas[fname] = meta
        frames[fname] = df
    return frames, metas
