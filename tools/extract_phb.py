from pathlib import Path
import json, hashlib, re, argparse
import pdfplumber
parser=argparse.ArgumentParser(description='Extract PHB table evidence; review layout before mapping content.')
parser.add_argument('source',type=Path)
parser.add_argument('output',type=Path)
args=parser.parse_args()
source=args.source
out=args.output
out.mkdir(parents=True,exist_ok=True)
tables=[]; headings=[]
with pdfplumber.open(source) as pdf:
 for n,p in enumerate(pdf.pages,1):
  if n<14: continue
  bands={}
  for r in p.rects:
   color=r.get('non_stroking_color')
   if isinstance(color,(tuple,list)) and len(color)==3 and max(color)<0.4 and r['width']>12:
    bands.setdefault(round(r['top'],1),[]).append(r)
  starts=sorted(bands)
  for top in starts:
   rects=sorted(bands[top],key=lambda r:r['x0']); x0=rects[0]['x0']; x1=rects[-1]['x1']
   xs=sorted(set(round(r['x0'],2) for r in rects)|{round(x1,2)})
   bottom=min([y for y in starts if y>top and abs(bands[y][0]['x0']-x0)<2]+[800])
   ys=sorted(set(round(l['top'],2) for l in p.lines if abs(l['x0']-x0)<1 and abs(l['x1']-x1)<1 and top-1<=l['top']<=bottom+0.5))
   if len(ys)<2: continue
   end=next((i for i in range(1,len(ys)) if ys[i]-ys[i-1]>85),len(ys));ys=ys[:end]
   rows=[]
   for a,b in zip(ys,ys[1:]):
    # A gap between tables may contain a green section heading; it is not a data row.
    if any(a<c['top']<b and x0<=c['x0']<x1 and isinstance(c.get('non_stroking_color'),(tuple,list)) and len(c['non_stroking_color'])==3 and c['non_stroking_color'][1]>c['non_stroking_color'][0]+0.05 and c['non_stroking_color'][1]>c['non_stroking_color'][2]+0.01 for c in p.chars): continue
    cells=[]
    for left,right in zip(xs,xs[1:]):
     cells.append(p.crop((left,a,right,b)).extract_text(x_tolerance=1,y_tolerance=2) or '')
    if any(cells): rows.append([' '.join(c.split()) for c in cells])
   if rows: tables.append({'pdfPage':n,'printedPage':n-13,'top':top,'rows':rows})
  # Font-based headings include unnumbered vehicle/discipline names, unlike TOC-only extraction.
  lines={}
  for c in p.chars:
   if 40<c['top']<790 and c.get('non_stroking_color') and isinstance(c['non_stroking_color'],(list,tuple)):
    col=c['non_stroking_color']
    if len(col)==3 and col[1]>col[0]+0.05 and col[1]>col[2]+0.01 and c['size']>=9:
     lines.setdefault(round(c['top'],1),[]).append(c)
  for y,chars in sorted(lines.items()):
   title=''.join(c['text'] for c in sorted(chars,key=lambda c:c['x0'])).strip()
   if title:headings.append({'pdfPage':n,'printedPage':n-13,'text':title})
(out/'tables.json').write_text(json.dumps(tables,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'headings.json').write_text(json.dumps(headings,ensure_ascii=False,indent=2),encoding='utf-8')
print('Tables',len(tables),'headings',len(headings),'sha256',hashlib.sha256(source.read_bytes()).hexdigest())
