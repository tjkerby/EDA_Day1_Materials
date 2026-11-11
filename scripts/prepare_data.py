"""Prepare the bundled teaching snapshots without accessing the network."""
from pathlib import Path
import hashlib
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'

def main():
    frames = [pd.read_csv(RAW / f'{year}_torn.csv') for year in range(2015, 2019)]
    raw = pd.concat(frames, ignore_index=True)
    whole = raw.loc[raw['sg'].eq(1)].copy()
    duplicate_count = int(whole.duplicated().sum())
    whole = whole.drop_duplicates().sort_values(['date', 'time', 'om']).reset_index(drop=True)
    assert not whole.duplicated(['yr', 'om']).any()
    assert whole['tz'].eq(3).all()
    tornadoes = whole.rename(columns={
        'yr': 'year', 'mo': 'month', 'date': 'event_date', 'time': 'start_time_cst',
        'st': 'start_state', 'mag': 'ef_rating', 'slat': 'start_latitude',
        'slon': 'start_longitude', 'elat': 'end_latitude', 'elon': 'end_longitude',
        'len': 'path_length_miles', 'wid': 'max_width_yards',
        'inj': 'injuries', 'fat': 'fatalities', 'ns': 'states_affected'
    })
    tornadoes['tornado_id'] = tornadoes['year'].astype(str) + '-' + tornadoes['om'].astype(str)
    tornadoes['ef_rating'] = tornadoes['ef_rating'].replace(-9, pd.NA).astype('Int64')
    tornadoes['start_hour_cst'] = pd.to_datetime(tornadoes['start_time_cst'], format='%H:%M:%S').dt.hour
    for col in ['start_latitude', 'start_longitude', 'end_latitude', 'end_longitude']:
        tornadoes[col] = tornadoes[col].replace(0, float('nan'))
    columns = ['tornado_id','event_date','year','month','start_time_cst','start_hour_cst',
               'start_state','ef_rating','path_length_miles','max_width_yards',
               'start_latitude','start_longitude','end_latitude','end_longitude',
               'states_affected','injuries','fatalities']
    tornadoes[columns].to_csv(ROOT / 'data/tornadoes.csv', index=False)
    titanic = pd.read_csv(RAW / 'titanic_seaborn.csv')
    titanic = titanic[['survived','pclass','sex','age','fare','sibsp','parch','embarked']].copy()
    titanic.insert(0, 'row_id', range(len(titanic)))
    titanic.to_csv(ROOT / 'data/titanic.csv', index=False)
    manifest = {
        'coverage': '2015-2018', 'raw_rows': len(raw), 'whole_track_rows_before_deduplication': len(raw.loc[raw.sg.eq(1)]),
        'exact_duplicates_removed': duplicate_count, 'teaching_rows': len(tornadoes),
        'unknown_ef_ratings': int(tornadoes.ef_rating.isna().sum()),
        'row_definition': 'One whole-track tornado record, sg == 1, with exact duplicates removed.',
        'transformations': ['Retain 2015-2018 source files', 'Retain sg == 1', 'Remove exact duplicate rows',
                            'Rename selected fields', 'Recode EF -9 to missing', 'Recode zero coordinates to missing',
                            'Add year-event identifier and CST hour', 'Omit loss fields and county segment fields'],
        'sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in sorted((ROOT / 'data').rglob('*.csv'))}
    }
    (ROOT / 'data/preparation_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({k: v for k, v in manifest.items() if k not in ['sha256','transformations']}, indent=2))

if __name__ == '__main__':
    main()
