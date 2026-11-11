# STAT 386: EDA Day 1

One Quarto website project with Reveal.js slides, paired live/completed Titanic notebooks, and a student tornado starter. Rendered pages live in **docs/** for GitHub Pages.

## Teach with these files

| File | Use |
|---|---|
| `slides.qmd` | Main lecture and group-activity slides |
| `notebooks/titanic_live_scaffold.ipynb` | Complete the Titanic exploration live in Positron |
| `notebooks/titanic_complete.ipynb` | Matching completed code, results, and interpretations |
| `notebooks/tornadoes_starter.ipynb` | Students load and understand the data, then do their own EDA |
| `notebooks/plotting_reference.ipynb` | Optional syntax examples using Titanic |
| `data_dictionary.qmd` | Dataset row meanings, columns, units, categories, and missing values |
| `teaching_notes.qmd` | Timing, expected responses, and live-teaching guidance |

The Titanic notebooks use matching sections. The live scaffold includes setup and prompts, with analysis cells left for you to fill in. It has no saved outputs. The completed version has executed outputs. The tornado starter provides data loading, a preview, column information, and a missingness check. It leaves the substantive EDA to students.

The deck keeps the question framing and three optional Titanic plot references. The demonstration itself happens in the notebook. There is no investigation sheet in this package.

## Positron setup

1. Extract the whole project folder and open that folder in Positron.
2. In its terminal, run `uv sync`.
3. Select the Python interpreter in `.venv` as the notebook kernel.
4. Open the Titanic scaffold and run its setup cell before class. Keep the completed version in a second tab.
5. Ask students to run the tornado starter's loading cell before class.

Initial dependency installation requires internet. The data are local, so the class activities need no downloads afterward. Python 3.11-3.13 is supported. `uv sync` creates a lockfile, which you can commit with the course repository.

## Preview and edit the website

Install Quarto from https://quarto.org/docs/get-started/ if needed. The Quarto CLI is separate from the Python environment.

```bash
quarto preview
```

Edit the `.qmd` files directly. To rebuild all pages:

```bash
quarto render
```

The project renders into `docs/`. Notebook rendering uses saved outputs and does not execute their analysis. The pre-render script packages the notebook-and-data download. The post-render script creates `.nojekyll` for GitHub Pages.

The supplied `docs/` folder is already a static website preview with local assets. Open `docs/index.html` to browse it without installing Quarto. It can also be served from GitHub Pages as supplied. Its static preview build is produced by `scripts/build_static_preview.py`; a normal Quarto render replaces it using the same authoritative `.qmd` sources. Quarto itself was not available in the authoring environment, so that CLI render has not been run here.

## GitHub Pages: deploy from docs

1. Put the contents of this folder at the root of your chosen GitHub repository. Include `docs/`.
2. In the repository, open **Settings > Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select the branch containing your files, then the **/docs** folder, and save.

The site uses relative links, so it works under a repository path such as `https://OWNER.github.io/REPOSITORY/`. No owner or repository name is hard-coded. After editing, run `quarto render`, commit the updated source and `docs/`, and push. GitHub Pages serves those files directly.

The landing page provides a single download containing all notebooks and data with the expected directory layout. A static website lets students read or download notebooks. Running Python happens locally in Positron.

No GitHub repository or public site was created or changed during this delivery.

## Data

Titanic contains 891 passenger records from seaborn's example subset. Tornadoes contains **4,706 NOAA SPC whole tracks from 2015-2018**, with 17 columns and 111 missing EF ratings. This is the same documented snapshot used in the previous package, with a more detailed introduction.

Tornado start hours use CST everywhere, EF0 is a valid damage rating, path lengths use miles, and widths use yards. Starting state is not every state affected. The dataset has no duration, city/county names, or narrative summary.

Original snapshots and a reproducible preparation script are included. `python scripts/prepare_data.py` recreates the teaching CSVs without network access.

## Class timing

| Clock | Segment |
|---|---|
| 0-2 | Visualization warmup |
| 2-9 | Brief framing and live Titanic investigation |
| 9-12 | Tornado dataset orientation |
| 12-16 | Question generation |
| 16-18 | Choose and refine one question |
| 18-36 | Original-group EDA |
| 36-46 | New groups share findings |
| 46-50 | Synthesis and Day 2 bridge |

The slightly deeper data introduction preserves 18 minutes of exploration and 10 minutes of sharing. The optional warmup cell in the Titanic notebook and the three plot-reference slides are unscheduled supports.
