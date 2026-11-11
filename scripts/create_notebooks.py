"""Create paired Titanic notebooks and a student tornado starter."""
from pathlib import Path
import json
import textwrap
import uuid

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'notebooks'
OUT.mkdir(exist_ok=True)

def cell(kind, text):
    result = {'cell_type':kind, 'id':uuid.uuid4().hex[:8], 'metadata':{},
              'source':textwrap.dedent(text).strip() + '\n'}
    if kind == 'code':
        result.update(execution_count=None, outputs=[])
    return result

def save(name, cells, title):
    nb = {'cells':cells, 'metadata':{
        'title':title,
        'kernelspec':{'display_name':'Python 3', 'language':'python', 'name':'python3'},
        'language_info':{'name':'python', 'version':'3.11'}},
        'nbformat':4, 'nbformat_minor':5}
    (OUT / name).write_text(json.dumps(nb, indent=1) + '\n')

setup = '''
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

# Open the project folder in Positron and select its .venv interpreter.
# Support kernels starting in the project root or in notebooks/.
ROOT = Path.cwd()
if not (ROOT / "data/titanic.csv").is_file():
    ROOT = ROOT.parent
if not (ROOT / "data/titanic.csv").is_file():
    raise FileNotFoundError("Open the project folder, then run this notebook again.")

titanic = pd.read_csv(ROOT / "data/titanic.csv")
sns.set_theme(style="whitegrid", context="talk")
'''

steps = [
('The records',
 'What does one row represent? Which columns can help us compare survival across passenger classes?',
 '''titanic.head()''',
 '''# TODO: Preview the first few passenger records.
# Hint: a familiar DataFrame method is enough.''',
 'One row represents one passenger in this 891-record subset. This is not the complete Titanic manifest.'),
('Available information',
 'Are the fields we need complete? Age and embarkation may matter for later questions.',
 '''print(f"Passenger records: {len(titanic):,}")
titanic.isna().sum()''',
 '''# TODO: Check the number of records and count missing values by column.''',
 '`survived`, `pclass`, and `sex` are complete. `age` has 177 missing values and `embarked` has 2. All 891 records contribute to the comparisons below.'),
('Optional warmup: the fare distribution',
 'What do you notice? What would you ask next? This matches the opening slide and can be skipped during the seven-minute demonstration.',
 '''sns.histplot(data=titanic, x="fare", bins=range(0, 551, 50))
plt.xlabel("Recorded fare (pounds sterling)")
plt.ylabel("Passengers")
plt.tight_layout()
plt.show()''',
 '''# OPTIONAL: Plot a histogram of fare.
# Label the horizontal axis with its units.''',
 'Most recorded fares are in the lower bins, with a long right tail. A comparison by class would be a reasonable next question.'),
('First question: how many survivors in each class?',
 'Begin with a count. What does this view leave unresolved if we want to compare survival proportions?',
 '''survivors = titanic.loc[titanic["survived"].eq(1)]
counts = survivors.groupby("pclass").size()
display(counts)
ax = counts.plot.bar(rot=0, color="#087F83")
ax.set(xlabel="Passenger class", ylabel="Survivors")
plt.tight_layout()
plt.show()''',
 '''# TODO: Keep passengers who survived.
# TODO: Count survivors within each passenger class.
# TODO: Draw and label a bar chart.
# Ask: what denominator would let us compare survival proportions?''',
 'The survivor counts are 136, 87, and 119. The class sizes differ, so the counts alone do not answer the proportion question.'),
('Follow-up: what proportion survived?',
 'Use all passengers in each class as the denominator. For complete 0/1 data, the mean equals the proportion of ones.',
 '''class_summary = titanic.groupby("pclass")["survived"].agg(
    survivors="sum", passengers="size", survival_rate="mean"
)
display(class_summary.round(3))
ax = class_summary["survival_rate"].plot.bar(rot=0, color="#087F83")
ax.set(xlabel="Passenger class", ylabel="Survival proportion", ylim=(0, 1))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
plt.tight_layout()
plt.show()''',
 '''# TODO: Return to all passengers and group by class.
# TODO: Summarize the number of survivors, the group size, and the mean of survived.
# TODO: Plot survival proportions with a 0-1 vertical axis.
# Optional formatting: mtick.PercentFormatter(1).''',
 'The proportions are 63.0% (136/216), 47.3% (87/184), and 24.2% (119/491). The next question asks whether that aggregate pattern looks similar within sex categories.'),
('Another question: does the pattern look similar within sex categories?',
 'Keep the class comparison and add recorded sex through color. Predict what might change before running the cell.',
 '''group_summary = titanic.groupby(["pclass", "sex"])["survived"].agg(
    survivors="sum", passengers="size", survival_rate="mean"
)
display(group_summary.round(3))
rates = group_summary["survival_rate"].unstack("sex")
ax = rates.plot.bar(rot=0, color=["#087F83", "#C76B2A"])
ax.set(xlabel="Passenger class", ylabel="Survival proportion", ylim=(0, 1))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.legend(title="Recorded sex")
plt.tight_layout()
plt.show()''',
 '''# TODO: Group by both class and recorded sex.
# TODO: Compute group sizes and survival proportions.
# TODO: Use .unstack("sex") to put the color groups into columns.
# TODO: Make a grouped bar chart and explain its denominator.''',
 'First-class survival proportions exceed third-class proportions within both recorded categories. Female survival proportions exceed male proportions within each class. These are descriptive associations in the passenger subset, not isolated causal effects.')
]

for completed in [True, False]:
    label = 'Completed reference' if completed else 'Live coding scaffold'
    cells = [cell('markdown',f'''# Titanic EDA: {label}

**Question:** How does survival vary by passenger class? What should we investigate after the first plot?

{('All code and outputs are supplied. Use this as your teaching reference or recovery copy.' if completed else 'Setup and discussion prompts are supplied. Complete the analysis cells live in Positron. The optional warmup can stay blank.')}

The paired notebooks use the same sections. Open the scaffold for class and keep the completed version in another tab.

Data: the bundled seaborn Titanic subset. See [the data dictionary](../data_dictionary.qmd) and [source notes](../sources.qmd).'''),
             cell('markdown','## Setup\n\nRun this cell before class. The dataset loads from the project folder without a download.'),
             cell('code',setup)]
    for title, prompt, solution, scaffold, answer in steps:
        cells.extend([cell('markdown',f'## {title}\n\n{prompt}'),cell('code',solution if completed else scaffold)])
        cells.append(cell('markdown',('**Interpretation:** '+answer) if completed else '**Discuss:** What does this view show? What does it leave unresolved?'))
    cells.extend([cell('markdown','''## Where would we go next?

Does age help explain variation within a class-by-sex group? How should we handle the missing ages?

What could fare, family size, and embarkation add to our understanding of passenger profiles?

Keep these questions open for Day 2. Today the reusable move is to explain why the next view helps answer the next question.''')])
    save('titanic_complete.ipynb' if completed else 'titanic_live_scaffold.ipynb',cells,'Titanic EDA: '+label)

tornado_cells = [cell('markdown','''# Tornado data: starter notebook

Run the setup and inspection cells before your investigation. After brainstorming with your group, use the open cells at the end for your own EDA.

**Dataset:** NOAA SPC historical tornado records, **2015-2018**. There are 4,706 whole-track records and 17 columns. One row represents one tornado track after removing duplicate and continuation records.

[Data guide](../data_dictionary.qmd) and [source notes](../sources.qmd). The same information is also summarized below.'''),
cell('markdown','## 1. Load the local CSV\n\nDates become datetimes. The EF rating uses pandas nullable integers so unknown ratings stay missing while EF0 stays zero.'),
cell('code','''from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path.cwd()
if not (ROOT / "data/tornadoes.csv").is_file():
    ROOT = ROOT.parent
if not (ROOT / "data/tornadoes.csv").is_file():
    raise FileNotFoundError("Open the project folder, then run this notebook again.")

tornadoes = pd.read_csv(
    ROOT / "data/tornadoes.csv",
    parse_dates=["event_date"],
    dtype={"tornado_id": "string", "start_state": "string", "ef_rating": "Int64"},
)
sns.set_theme(style="whitegrid", context="talk")
print(f"Loaded {len(tornadoes):,} records and {tornadoes.shape[1]} columns.")'''),
cell('markdown','## 2. Preview a few records\n\nRead the units in the column names. A whole track can begin and end at different coordinates.'),
cell('code','''tornadoes[[
    "tornado_id", "event_date", "start_state", "ef_rating",
    "path_length_miles", "max_width_yards", "states_affected"
]].head()'''),
cell('markdown','''## 3. Understand the fields

| Kind of information | Columns | Meaning |
|---|---|---|
| Identifier | `tornado_id` | A year-event identifier, not a measurement |
| Date | `event_date`, `year`, `month` | Source start date and derived calendar fields |
| Clock time | `start_time_cst`, `start_hour_cst` | CST for every record, not local time everywhere |
| Starting location | `start_state`, `start_latitude`, `start_longitude` | Where the recorded track begins |
| Ending location | `end_latitude`, `end_longitude` | Where the recorded track ends |
| Track size | `path_length_miles`, `max_width_yards` | Total length and maximum width in different units |
| Intensity | `ef_rating` | Ordered EF damage category, not a direct wind-speed measurement |
| Extent and outcomes | `states_affected`, `injuries`, `fatalities` | Recorded counts associated with the whole track |

EF0 is valid. An unknown EF rating is `<NA>`. The categories are ordered, but EF4 does not mean twice the wind speed of EF2. The rating is based on damage surveys and estimated winds.

A multi-state track still occupies one row. `start_state` assigns it to its beginning, not every state it affected. All start hours use a common CST clock, including records outside that zone.

The snapshot has no city or county name, narrative description, end time, duration, population, or exposed-area denominator.'''),
cell('code','''tornadoes.info()'''),
cell('markdown','## 4. Check missing information\n\nThis checks availability, without choosing your research question or dropping records.'),
cell('code','''missing = tornadoes.isna().sum()
display(missing[missing.gt(0)].rename("missing_records").to_frame())
print("Unknown EF ratings:", tornadoes["ef_rating"].isna().sum())
print("Records with an observed EF rating:", tornadoes["ef_rating"].notna().sum())'''),
cell('markdown','''Keep the full DataFrame. If your chosen question requires EF rating, decide explicitly how to handle the 111 unknown values. A question using dates or path lengths may not need to exclude them.

`.dropna()` with no subset would drop records for every missing field. Prefer `dropna(subset=[...])` for the variables your question actually needs, and report how many rows remain.

## 5. Your investigation

Choose a question after your group's brainstorming. You can use ordinary pandas, seaborn, or matplotlib code below.

**Our question:** ...

**Variables, units, comparison, and any denominator:** ...'''),
cell('code','''# Your first summary or visualization.
'''),
cell('markdown','**What does the result show? What remains unresolved?** ...\n\n**Our follow-up question or check:** ...'),
cell('code','''# Your follow-up summary or visualization.
'''),
cell('markdown','''## Before regrouping

Keep your plot available. Be ready to explain the question, evidence, how your investigation changed, and what you would investigate next.

If you need syntax support, see `plotting_reference.ipynb`. Its examples use Titanic so your tornado investigation remains your own.''')]
save('tornadoes_starter.ipynb',tornado_cells,'Tornado data: starter notebook')
print('Created completed and scaffolded Titanic notebooks and the tornado starter')
