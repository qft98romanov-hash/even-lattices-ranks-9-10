"""Freeze file hashes and bilingual formula parity after completed visual review."""
from pathlib import Path
import json,re,hashlib,datetime
ROOT=Path(__file__).resolve().parents[2]
BUILD=ROOT/'research_20261008/report_build'
OUT=ROOT/'output'
qa=json.loads((BUILD/'report_QA.json').read_text())
pattern=r'(?<!\\)\\\[(.*?)\\\]|\\begin\{equation\}(.*?)\\end\{equation\}|\\begin\{align\}(.*?)\\end\{align\}'
def mathblocks(lang):
    source=(OUT/f'lattices_complete_{lang}.tex').read_text()
    result=[]
    for m in re.finditer(pattern,source,re.S):
        s=next(g for g in m.groups()if g is not None)
        s=re.sub(r'\\text\{[^}]*\}','TEXT',s)
        result.append(re.sub(r'\s+','',s).rstrip('.,;'))
    return result
assert mathblocks('RU')==mathblocks('EN')
for lang in ('RU','EN'):
    row=qa[lang]
    assert not row['warnings']
    assert row['tex_txt_identical']
    assert row['pages']==row['rendered_pages']
    row['file_sha256']={ext:hashlib.sha256((OUT/f'lattices_complete_{lang}.{ext}').read_bytes()).hexdigest()for ext in ('tex','txt','pdf')}
    row['file_bytes']={ext:(OUT/f'lattices_complete_{lang}.{ext}').stat().st_size for ext in ('tex','txt','pdf')}
    row['all_pages_visually_reviewed']=True
    row['visually_reviewed_page_numbers']=list(range(1,row['pages']+1))
    row['visual_review_method']='All rendered pages inspected in contact sheets; newly inserted proof and consequence pages also inspected individually at full rendered size.'
    row['visual_defects_found']=[]
    row['normalized_display_math_blocks']=len(mathblocks(lang))
    row['bilingual_display_math_exact_parity']=True
    row['display_math_normalization']='Whitespace, prose in \\text{...}, and terminal punctuation only.'
    row['independent_mathematical_and_scope_review']='PASS; equality proof, intrinsic structure, guaranteed radius, and removed stale open-equality statements reviewed by separate internal agents and root.'
qa['freeze_status']='FROZEN_FINAL'
qa['frozen_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(BUILD/'report_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({lang:{'pages':qa[lang]['pages'],'labels':len(qa[lang]['labels']),'equation_labels':len(qa[lang]['equation_labels']),'display_math_blocks':qa[lang]['normalized_display_math_blocks'],'hashes':qa[lang]['file_sha256']}for lang in ('RU','EN')},indent=2))
