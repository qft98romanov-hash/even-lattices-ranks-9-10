"""Compile the two standalone reports and create review contact sheets."""
from pathlib import Path
import subprocess, shutil, json, re
from PIL import Image, ImageOps, ImageDraw
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2]
BUILD=ROOT/'research_20261008/report_build'
OUT=ROOT/'output'
qa={}
for lang in ('RU','EN'):
    name='lattices_complete_'+lang
    source=OUT/(name+'.tex')
    text=source.read_text()
    for step in range(3):
        p=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(BUILD),str(source)],capture_output=True,text=True)
        (BUILD/(name+'.stdout')).write_text(p.stdout+p.stderr)
        if p.returncode: raise RuntimeError(p.stdout[-4000:]+p.stderr)
    shutil.copyfile(BUILD/(name+'.pdf'),OUT/(name+'.pdf'))
    shutil.copyfile(source,OUT/(name+'.txt'))
    log=(BUILD/(name+'.log')).read_text()
    warnings=[s for s in log.splitlines() if 'Warning' in s or 'Overfull' in s or 'Underfull' in s or 'Missing character' in s]
    pdf=PdfReader(OUT/(name+'.pdf'))
    page_dir=BUILD/('render_'+lang);page_dir.mkdir(exist_ok=True)
    subprocess.run(['pdftoppm','-r','85','-png',str(OUT/(name+'.pdf')),str(page_dir/'page')],check=True,capture_output=True)
    pages=sorted(page_dir.glob('page-*.png'))
    for k in range(0,len(pages),8):
        canvas=Image.new('RGB',(1500,1100),'#e5e5e5');draw=ImageDraw.Draw(canvas)
        for j,path in enumerate(pages[k:k+8]):
            page=Image.open(path).convert('RGB');page.thumbnail((365,515))
            # Four columns and two rows keep each full sheet readily viewable.
            x=(j%4)*375+(375-page.width)//2;y=(j//4)*550+30
            draw.text((x,y-21),f'{lang} page {k+j+1}',fill='black')
            canvas.paste(page,(x,y))
        canvas=canvas.crop((0,0,1500,1100 if len(pages[k:k+8])>4 else 550))
        canvas.save(BUILD/f'contact_{lang}_{k//8+1}.jpg',quality=90)
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    equation_labels=[]
    for m in re.finditer(r'\\begin\{(equation|align)\}(.*?)\\end\{\1\}',text,re.S):
        equation_labels+=re.findall(r'\\label\{([^}]+)\}',m.group(2))
    qa[lang]={'pages':len(pdf.pages),'warnings':warnings,'labels':labels,'equation_labels':equation_labels,'tex_txt_identical':source.read_bytes()==(OUT/(name+'.txt')).read_bytes(),'rendered_pages':len(pages)}
assert qa['RU']['labels']==qa['EN']['labels'], 'Label parity mismatch'
assert qa['RU']['equation_labels']==qa['EN']['equation_labels'], 'Equation parity mismatch'
(BUILD/'report_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
print(json.dumps({k:{'pages':v['pages'],'warnings':v['warnings'],'labels':len(v['labels'])}for k,v in qa.items()},ensure_ascii=False,indent=2))
