from pathlib import Path
import hashlib,json,sys
root=Path(sys.argv[1]).resolve();manifest=json.loads((root/'bundle_manifest.json').read_text())
for relative,info in manifest['files'].items():
    path=(root/relative).resolve()
    if not path.is_relative_to(root) or not path.is_file():raise ValueError('Missing or unsafe artifact: '+relative)
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    if h.hexdigest()!=info['sha256']:raise ValueError('Artifact checksum mismatch: '+relative)
print('All',len(manifest['files']),'model/code artifacts verified')
