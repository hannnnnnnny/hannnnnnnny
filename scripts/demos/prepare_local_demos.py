"""Store real offline CLI output for the explicitly labelled replay viewer."""
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]

if __name__ == '__main__':
    base = ROOT / 'output/playwright'
    result = subprocess.run([str(base/'guardrun-env/Scripts/python.exe'),
                             str(base/'sources/guardrun/examples/offline_demo.py')],
                            capture_output=True, text=True, check=True, timeout=30)
    lines = result.stdout.splitlines()
    stages = [lines[:3], lines[3:6], lines[6:]]
    (base/'recordings/guardrun-output.json').write_text(json.dumps(stages), encoding='utf-8')
