"""Keep GitHub Pages from processing the rendered Quarto site with Jekyll."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
output = root / 'docs'
output.mkdir(exist_ok=True)
(output / '.nojekyll').touch()
