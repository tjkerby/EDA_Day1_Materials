"""Package notebook downloads with the local data and Python project settings."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'downloads'
out.mkdir(exist_ok=True)
instructions = '''# EDA Day 1: notebooks and data

Extract this whole folder and open it in Positron. In the terminal, run:

    uv sync

Select the .venv Python interpreter as the notebook kernel.

Instructor live coding: notebooks/titanic_live_scaffold.ipynb
Instructor reference: notebooks/titanic_complete.ipynb
Student investigation: notebooks/tornadoes_starter.ipynb
Optional syntax support: notebooks/plotting_reference.ipynb

Keep the data/ directory next to notebooks/. Data load locally after setup.
Tornado coverage is 2015-2018. See data/data_dictionary.md and data/SOURCES.md.
'''
with ZipFile(out / 'EDA_Day1_Notebooks_and_Data.zip', 'w', ZIP_DEFLATED) as z:
    for pattern in ['notebooks/*.ipynb','data/*.csv','data/*.md','pyproject.toml']:
        for p in ROOT.glob(pattern):
            z.write(p, Path('EDA_Day1') / p.relative_to(ROOT))
    z.writestr('EDA_Day1/README.md', instructions)
print('Prepared notebook-and-data download')
