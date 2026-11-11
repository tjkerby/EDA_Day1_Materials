# Data sources and preparation

## Titanic demonstration

The bundled `titanic.csv` contains 891 passenger records from the seaborn example dataset, a familiar subset associated with the Kaggle Titanic training data. It is a subset of Titanic passengers, not a complete passenger manifest or a random sample of everyone aboard.

- Retrieved through the GitHub connection on November 11, 2026.
- Source: https://github.com/mwaskom/seaborn-data/blob/master/titanic.csv
- Original snapshot: `raw/titanic_seaborn.csv`.
- Preparation: retain eight variables used in the existing dimensionality reduction notebook and add `row_id`.
- Retain missing ages and embarkation codes. Day 1 uses complete `survived`, `pclass`, and `sex` fields, so it does not impute or discard rows.
- `sex` preserves the source's recorded categories. `survived` is 1 for survived and 0 otherwise. `fare` is the recorded fare in pounds sterling, with possible shared-ticket complications.
- The seaborn-data repository describes these files as example datasets and cautions that some are modified from their canonical sources: https://github.com/mwaskom/seaborn-data

## Tornado group investigation

The old slides contain a Wikipedia table for 2015-2022 but do not include the underlying data file. This package uses a **2015-2018 NOAA Storm Prediction Center snapshot** instead. It does not contain city names, narrative summaries, or end times. The change in coverage and schema is explicit throughout these materials.

- Primary publisher: NOAA / National Weather Service Storm Prediction Center, Severe Weather Database, https://www.spc.noaa.gov/wcm/#data
- Field specification: https://www.spc.noaa.gov/wcm/data/SPC_severe_database_description.pdf
- Accessible copy of that specification: https://www.gsa.state.al.us/apps/CAGDV/Metadata/Hazards/SPC_severe_database_description.pdf
- Annual NOAA CSV snapshots obtained from the teaching repository https://github.com/gabrielodom/PHC6701_r4ds/tree/main/_data/purrr_example_data
- Original files: `raw/2015_torn.csv` through `raw/2018_torn.csv`.
- The four annual snapshots contain 4,820 rows including state and county continuation segments. Keep `sg == 1` to retain whole tracks, then remove one exact duplicate. This produces 4,706 records.
- NOAA/SPC is the data publisher. The GitHub repository is the retrieval mirror, not a separate observing system. Treat this as a historical snapshot that can differ from later NOAA revisions.
- Federal NOAA data are public domain. Credit NOAA/SPC when reusing the data. General NOAA guidance: https://www.noaa.gov/information-technology/open-data-dissemination

## Preparation choices

Run `python scripts/prepare_data.py` from the repository root to recreate the teaching CSVs from the bundled raw snapshots. No network access is needed.

1. Retain whole-track rows (`sg == 1`). Extra state and continuing county segments would otherwise count some tornadoes more than once.
2. Remove the one exact duplicate. Validate the resulting year-event identifier.
3. Rename fields and add `tornado_id` and `start_hour_cst`.
4. Recode EF rating -9 as missing. Preserve 0 as the valid EF0 category.
5. Recode zero latitude or longitude as missing. Preserve recorded zero path measurements rather than assigning an undocumented meaning to them.
6. Omit monetary loss fields because the source's units and coding change across years.
7. Omit county codes and narrative fields absent from this snapshot.

All retained source records use timezone code 3, which the SPC specification defines as Central Standard Time. The hour is therefore **CST for every record**, not local clock time at each tornado location. No daylight saving adjustment is applied.

`start_state` names the state attached to the whole-track record, associated with the tornado's start. A tornado can affect more than one state. Counts by this column are counts assigned to the starting state, not counts of all tornadoes affecting each state.

The preparation manifest records row counts and SHA-256 hashes. The snapshot has 111 unknown EF ratings, retained as missing. For analyses requiring EF, report the number of excluded records. Geographic comparisons of raw counts do not account for area, population, or reporting differences. These four years support descriptive investigation, not a long-term climate trend claim.
