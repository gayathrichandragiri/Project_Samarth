import pandas as pd
def normalize_rainfall_df(df):
    # expect columns: state,district,year,month,rainfall_mm
    df = df.rename(columns={c:c.strip() for c in df.columns})
    if 'rainfall_mm' in df.columns:
        df['rainfall_mm'] = pd.to_numeric(df['rainfall_mm'], errors='coerce')
    return df

def normalize_crop_df(df):
    # expect columns: state,district,year,crop,production_tonnes
    df = df.rename(columns={c:c.strip() for c in df.columns})
    if 'production_tonnes' in df.columns:
        df['production_tonnes'] = pd.to_numeric(df['production_tonnes'], errors='coerce')
    return df
