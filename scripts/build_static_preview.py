"""Build a local-assets static preview when the Quarto CLI is unavailable.

The .qmd files remain authoritative. Normal maintenance uses quarto render.
Requires Pandoc and PyYAML only for this fallback authoring path.
"""
from pathlib import Path
import base64
import html
import json
import re
import shutil
import subprocess
import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
DOCS.mkdir(exist_ok=True)
for directory in ['assets','vendor','downloads']:
    shutil.copytree(ROOT/directory,DOCS/directory,dirs_exist_ok=True)
(DOCS/'data').mkdir(exist_ok=True)
(DOCS/'notebooks').mkdir(exist_ok=True)
for p in (ROOT/'data').glob('*'):
    if p.is_file() and p.suffix in ['.csv','.md']:
        shutil.copy2(p,DOCS/'data'/p.name)
for p in (ROOT/'notebooks').glob('*.ipynb'):
    shutil.copy2(p,DOCS/'notebooks'/p.name)

def parts(path):
    text=path.read_text()
    _,meta,body=text.split('---',2)
    return yaml.safe_load(meta),body

def links(text):
    return re.sub(r'(?<=["\'])((?:\.\./)?[^"\'<>\s]+)\.qmd(?=["\'])',r'\1.html',text)

def page(title,body,prefix=''):
    nav=''.join(f'<a href="{prefix}{p}">{label}</a>' for p,label in [
        ('index.html','Home'),('slides.html','Slides'),('notebooks.html','Notebooks'),
        ('data_dictionary.html','Data guide'),('teaching_notes.html','Teaching notes')])
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{html.escape(title)} | STAT 386</title>'
        f'<link rel="stylesheet" href="{prefix}assets/site.css"></head><body>'
        f'<header class="site-header"><nav aria-label="Main navigation">{nav}</nav></header>'
        f'<main><h1>{html.escape(title)}</h1>{links(body)}</main>'
        '<footer>STAT 386 · Exploratory Data Analysis</footer></body></html>')

for name in ['index','notebooks','data_dictionary','sources','teaching_notes']:
    meta,body=parts(ROOT/f'{name}.qmd')
    rendered=subprocess.run(['pandoc','--from=markdown','--to=html5','--wrap=none'],input=body,text=True,capture_output=True,check=True).stdout
    (DOCS/f'{name}.html').write_text(page(meta['title'],rendered))

for path in (ROOT/'notebooks').glob('*.ipynb'):
    nb=json.loads(path.read_text())
    chunks=[]
    for c in nb['cells']:
        source=c['source'] if isinstance(c['source'],str) else ''.join(c['source'])
        if c['cell_type']=='markdown':chunks.append(source)
        elif c['cell_type']=='code':
            chunks.append('```python\n'+source+'\n```')
            for o in c['outputs']:
                if o['output_type']=='stream':
                    chunks.append('<pre class="output">'+html.escape(''.join(o['text']))+'</pre>')
                elif 'data' in o:
                    data=o['data']
                    if 'image/png' in data:
                        img=''.join(data['image/png'])
                        chunks.append(f'<img class="notebook-figure" alt="Notebook plot output" src="data:image/png;base64,{img}">')
                    elif 'text/html' in data:chunks.append('<div class="table-scroll">'+''.join(data['text/html'])+'</div>')
                    elif 'text/plain' in data:chunks.append('<pre class="output">'+html.escape(''.join(data['text/plain']))+'</pre>')
    body=subprocess.run(['pandoc','--from=markdown','--to=html5','--wrap=none'],input='\n\n'.join(chunks),text=True,capture_output=True,check=True).stdout
    title=nb['metadata'].get('title',path.stem)
    download=f'<p><a href="{path.name}" download>Download this notebook</a></p>'
    (DOCS/'notebooks'/f'{path.stem}.html').write_text(page(title,download+body,'../'))

meta,body=parts(ROOT/'slides.qmd')
# Pandoc uses the same Markdown and Reveal.js core. Convert only Quarto image sizes and column widths.
body=re.sub(r'\{width="100%"\}', '{style="width:100%"}',body)
body=re.sub(r'\{height="380"\}', '{style="height:380px"}',body)
body=re.sub(r'\.column width="(\d+%)"',r'.column style="width:\1"',body)
cover='# '+meta['title']+'\n\n'+meta['subtitle']+'\n\nSTAT 386 · Day 1\n\n'
source=cover+body
# Use a single slide level for the cover and content.
source=re.sub(r'^## ', '# ', source, flags=re.M)
args=['pandoc','--from=markdown','--to=revealjs','--standalone','--slide-level=1',
      '-V','revealjs-url=vendor/reveal','-V','transition=none',
      '-V','width=1280','-V','height=720','-V','margin=0.05','-V','center=false',
      '-V','slideNumber="c/t"','--css','assets/slides.css','--metadata','pagetitle=Exploratory Data Analysis']
output=subprocess.run(args,input=source,text=True,capture_output=True,check=True).stdout
output=output.replace('vendor/reveal/dist/reveal.js','vendor/reveal/reveal.js').replace('vendor/reveal/dist/reveal.css','vendor/reveal/reveal.css')
output=output.replace('vendor/reveal/dist/reset.css','vendor/reveal/reset.css')
output=re.sub(r'vendor/reveal/dist/theme/[^\"]+\.css','vendor/reveal/theme.css',output)
output=re.sub(r'<script src="vendor/reveal/plugin/[^\"]+"></script>','',output)
output=re.sub(r'plugins:\s*\[[^\]]*\]','plugins: []',output)
(DOCS/'slides.html').write_text(output)
(DOCS/'.nojekyll').touch()
print('Built static website preview from the Quarto sources and saved notebook outputs')
