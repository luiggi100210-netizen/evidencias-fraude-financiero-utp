import json,urllib.request,urllib.parse,time,concurrent.futures
from pathlib import Path
out=Path(__file__).resolve().parent/'metadatos_citas';out.mkdir(exist_ok=True)
records=json.loads((Path(__file__).resolve().parent/'semillas.json').read_text(encoding='utf8'))
def get(r):
 doi=r['doi'];path=out/(str(r['sc'])+'.json')
 if path.exists():return
 url='https://api.semanticscholar.org/graph/v1/paper/DOI:'+urllib.parse.quote(doi,safe='/')+'?fields=title,references.title,references.externalIds,references.year,citations.title,citations.externalIds,citations.year'
 for k in range(3):
  try:
   data=json.load(urllib.request.urlopen(url,timeout=14));path.write_text(json.dumps(data,ensure_ascii=False),encoding='utf8');return
  except Exception as e:print(doi,str(e),flush=True);time.sleep(2+k)
with concurrent.futures.ThreadPoolExecutor(3) as pool:list(pool.map(get,records))
