"""Execute notebook code in order and retain standard table/figure outputs.

This small runner executes ordinary Python cells used in these materials.
It is not a replacement for the general Jupyter notebook execution protocol.
"""
from pathlib import Path
import ast
import base64
import contextlib
import io
import json
import os
import sys
import warnings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]

def run(path):
    original=path.read_text()
    nb=json.loads(original)
    namespace={'__name__':'__main__'}
    output=[]
    def display(obj):
        data={'text/plain':repr(obj)}
        if hasattr(obj,'_repr_html_'):
            html=obj._repr_html_()
            if html: data['text/html']=html
        output.append({'output_type':'display_data','metadata':{},'data':data})
    def show(*args,**kwargs):
        for num in plt.get_fignums():
            fig=plt.figure(num)
            buf=io.BytesIO()
            fig.savefig(buf,format='png',dpi=110,bbox_inches='tight',facecolor='white')
            output.append({'output_type':'display_data','metadata':{},'data':{'image/png':base64.b64encode(buf.getvalue()).decode(), 'text/plain':'<Figure>'}})
        plt.close('all')
    namespace['display']=display
    old_show=plt.show
    plt.show=show
    old_cwd=Path.cwd()
    os.chdir(path.parent)
    count=0
    try:
        for cell in nb['cells']:
            if cell['cell_type']!='code': continue
            count+=1
            output=[]
            source=cell['source'] if isinstance(cell['source'],str) else ''.join(cell['source'])
            tree=ast.parse(source)
            last=None
            if tree.body and isinstance(tree.body[-1],ast.Expr):
                last=tree.body.pop()
            stdout=io.StringIO()
            stderr=io.StringIO()
            with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
                exec(compile(tree,str(path),'exec'),namespace)
                if last:
                    val=eval(compile(ast.Expression(last.value),str(path),'eval'),namespace)
                    if val is not None: display(val)
            if stdout.getvalue(): output.insert(0,{'output_type':'stream','name':'stdout','text':stdout.getvalue()})
            if stderr.getvalue(): output.insert(0,{'output_type':'stream','name':'stderr','text':stderr.getvalue()})
            cell['outputs']=output
            cell['execution_count']=count
        if 'scaffold' not in path.name:
            path.write_text(json.dumps(nb,indent=1)+'\n')
        import nbformat
        nbformat.validate(nbformat.reads(json.dumps(nb),as_version=4))
        print(f'{path.name}: {count} code cells executed and notebook schema validated')
    finally:
        plt.show=old_show
        plt.close('all')
        os.chdir(old_cwd)

if __name__=='__main__':
    for path in sorted((ROOT/'notebooks').glob('*.ipynb')):
        run(path)
