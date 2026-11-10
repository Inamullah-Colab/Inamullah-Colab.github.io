#!/usr/bin/env python3
"""Validate the maintained vacancy registry; optionally compare another vacancy list."""
import json,re,sys
from pathlib import Path
from urllib.parse import urlsplit,parse_qsl,urlencode,urlunsplit
from datetime import date

def canonical_url(url):
    u=urlsplit(url)
    query=sorted((k,v) for k,v in parse_qsl(u.query,keep_blank_values=True) if not k.lower().startswith('utm_') and k.lower() not in {'source','referrer','fbclid','gclid'})
    return urlunsplit((u.scheme.lower(),u.netloc.lower(),u.path.rstrip('/'),urlencode(query),''))

def employer_ref(job):
    employer=re.sub(r'[^a-z0-9]','',job.get('employer','').lower().removeprefix('the '))
    ref=re.sub(r'[^a-z0-9]','',job.get('reference','').lower())
    return (employer,ref) if employer and ref else None

def check(data, existing=()):
    seen_urls={canonical_url(j['url']) for j in existing if j.get('url')}
    seen_refs={employer_ref(j) for j in existing if employer_ref(j)}
    ids=set();errors=[]
    for j in data['jobs']:
        for field in ['id','title','employer','location','reference','url','summary','eligibility','group','role_type','checked_at','closing_date','status']:
            if not isinstance(j.get(field),str) or not j[field].strip():errors.append(f"{j.get('id')}: missing {field}")
        if j['id'] in ids:errors.append('duplicate id: '+j['id'])
        ids.add(j['id'])
        key=canonical_url(j['url']);ref=employer_ref(j)
        if key in seen_urls or ref in seen_refs:errors.append('duplicate vacancy: '+j['id'])
        seen_urls.add(key);seen_refs.add(ref)
        if j['group'] not in ['research','teaching','professional']:errors.append('invalid group: '+j['id'])
        if j['status'] not in ['open','closed','unverified']:errors.append('invalid status: '+j['id'])
        for field in ['checked_at','closing_date']:date.fromisoformat(j[field])
        if j['status']=='open' and j['closing_date']<j['checked_at']:errors.append('past deadline marked open: '+j['id'])
        if not j['url'].startswith('https://') or 'jobs.ac.uk' in urlsplit(j['url']).netloc:errors.append('missing official employer URL: '+j['id'])
    if errors:raise ValueError('\n'.join(errors))
    return len(ids)
if __name__=='__main__':
    data=json.loads(Path('_data/university_jobs.json').read_text())
    existing=json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv)>1 else []
    print(f"Validated {check(data,existing)} unique vacancy records.")
