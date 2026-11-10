#!/usr/bin/env python3
"""Build employer/role roundups for the existing Knowledge & Opportunity reader."""
import json
import re
import runpy
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
    'academic': 'Academic, teaching & professorial roles',
    'computing': 'AI, computing, data & IT roles',
    'health': 'Biomedical, health & life sciences roles',
    'engineering': 'Engineering, physical sciences & environment',
    'social': 'Humanities, business & social science roles',
    'professional': 'Administration, student services & professional roles',
    'technical': 'Technical, facilities & operational roles',
}
EMPLOYERS = {
    'University of Bath': ('bath', 'Bath'),
    'University of Leeds': ('leeds', 'Leeds'),
    'The University of Manchester': ('manchester', 'Manchester'),
    'University of the Arts London': ('arts-london', 'University of the Arts London'),
    'Queen Mary University of London': ('queen-mary', 'Queen Mary University of London'),
    'Newcastle University': ('newcastle', 'Newcastle'),
    'University of Aberdeen': ('aberdeen', 'Aberdeen'),
    'University of Sheffield': ('sheffield', 'Sheffield'),
    'LASE (University of Kent)': ('kent', 'LASE / University of Kent'),
    'University of Surrey': ('surrey', 'Surrey'),
}

def build(data):
    runpy.run_path(str(ROOT / 'scripts/check-university-jobs.py'))['check'](data)
    groups = defaultdict(list)
    for job in data['jobs']:
        if job['collection_group'] not in GROUPS:
            raise ValueError('Unknown collection group: ' + job['id'])
        if job['employer'] not in EMPLOYERS:
            raise ValueError('Add a stable employer slug: ' + job['employer'])
        groups[job['employer'], job['collection_group']].append(job)
    articles = []
    for (employer, group), jobs in sorted(groups.items()):
        slug, label = EMPLOYERS[employer]
        items = []
        for job in sorted(jobs, key=lambda j: (j['closing_date'], j['reference'])):
            note = ' '.join(filter(None, [job['summary'], job['eligibility'], job['role_type'], job.get('editor_note', '')]))
            item = dict(title=job['title'], department=' · '.join(dict.fromkeys(filter(None, [job.get('department'), job['location']]))),
                        salary=job.get('salary', ''), deadline=job['closing_date'], availability=job['status'],
                        reference=job['reference'], url=job['url'], restrictions='', note=note)
            time = re.fullmatch(r'(\d{1,2}:\d{2})(?:\s*(?:UK time|GMT|BST))?', job.get('closing_time', ''))
            if time:
                item['deadlineAt'] = datetime.fromisoformat(job['closing_date'] + 'T' + time[1].zfill(5)).replace(tzinfo=ZoneInfo('Europe/London')).isoformat()
            elif job.get('closing_time'):
                item['note'] += ' Advertised cut-off: ' + job['closing_time'] + '; check the employer’s instructions.'
            items.append(item)
        count = len(items)
        checked = min(j['checked_at'] for j in jobs)
        title = f'{label}: {GROUPS[group]}'
        source = jobs[0]['url']
        articles.append(dict(
            id=f'university-{slug}-{group}', title=title, category='Jobs',
            excerpt=f'{count} '+('role' if count == 1 else 'roles')+f' at {employer}, with salaries, eligibility notes, closing dates and official application links.',
            body=f'{GROUPS[group]} at {employer}. Browse the selected vacancies below, or search by role, department or reference.\n\nEach entry links directly to the employer’s advert. Red deadline indicators identify roles closing within seven days. Read the full person specification and application instructions before applying.',
            level='Everyone', region='United Kingdom', deadline='', source=source, references='',
            status='published', updated=max(j['checked_at'] for j in jobs), kind='Job roundup',
            jobRoundup=dict(employer=employer, checkedAt=checked, sourceUrl=source, items=items),
        ))
    return articles

if __name__ == '__main__':
    data = json.loads((ROOT / '_data/university_jobs.json').read_text())
    articles = build(data)
    (ROOT / '_data/university_job_articles.json').write_text(json.dumps(articles, ensure_ascii=False, indent=2) + '\n')
    print(f"Built {len(articles)} university/role collections containing {sum(len(a['jobRoundup']['items']) for a in articles)} unique vacancies.")
