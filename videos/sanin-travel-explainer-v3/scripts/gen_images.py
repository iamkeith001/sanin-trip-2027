"""Generate v3 scene images with the draw skill (gpt-image-2.5-flare, low, 1536x1024).
Skips names that already have a PNG in assets/images/gen. Run with /usr/bin/python3."""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
P = Path(__file__).resolve().parents[1]
OUT = P / 'assets/images/gen'; OUT.mkdir(parents=True, exist_ok=True)
DRAW = Path.home() / '.claude/skills/draw/draw.py'
d = json.loads((P / 'scripts/gen_prompts.json').read_text())
only = set(sys.argv[1:])
jobs = [(n, p + ' ' + d['_style'][s]) for n, s, p in d['images']
        if (not only or n in only) and not list(OUT.glob(f'{n}_*.png'))]
def run(job):
    n, prompt = job
    r = subprocess.run([sys.executable, str(DRAW), prompt, '--size', '1536x1024', '--quality', 'low',
                        '--name', n, '--outdir', str(OUT)], capture_output=True, text=True)
    return n, r.returncode, (r.stderr or r.stdout)[-300:]
with ThreadPoolExecutor(4) as ex:
    for n, rc, msg in ex.map(run, jobs):
        print(('ok   ' if rc == 0 else 'FAIL ') + n + ('' if rc == 0 else ' :: ' + msg.strip()), flush=True)
print(len(list(OUT.glob('*.png'))), 'images in', OUT)
