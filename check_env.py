import sys
import os
from pathlib import Path

checks = []

print("Running Emotrics environment checks\n")

# packages to test
packages = [
    ("numpy", "import numpy as np; print(np.__version__)") ,
    ("scipy", "import scipy; print(scipy.__version__)") ,
    ("pandas", "import pandas as pd; print(pd.__version__)") ,
    ("opencv (cv2)", "import cv2; print(cv2.__version__)") ,
    ("PyQt5", "from PyQt5 import QtCore; print('PyQt5', QtCore.PYQT_VERSION_STR, 'Qt', QtCore.QT_VERSION_STR)") ,
    ("dlib", "import dlib; print(getattr(dlib, '__version__', 'unknown'))"),
    ("openpyxl", "import openpyxl; print(openpyxl.__version__)") ,
    ("xlsxwriter", "import xlsxwriter; print(xlsxwriter.__version__)")
]

for name, code in packages:
    try:
        exec(code, {})
        print(f"OK: {name}")
        checks.append((name, True, None))
    except Exception as e:
        print(f"MISSING/ERROR: {name} -> {e}")
        checks.append((name, False, str(e)))

# verify dlib model files exist
print('\nChecking model files in include/data:')
root = Path(__file__).resolve().parent
models_dir = root / 'include' / 'data'
expected = [
    'shape_predictor_68_face_landmarks.dat',
    'mee_shape_predictor_68_face_landmarks.dat'
]
for m in expected:
    p = models_dir / m
    if p.exists():
        print(f"OK: {m} -> {p}")
    else:
        print(f"MISSING: {m} (expected at {p})")

# quick sanity for loading a dlib predictor (if available)
try:
    import dlib
    predictor_path = None
    for cand in expected:
        candp = models_dir / cand
        if candp.exists():
            predictor_path = str(candp)
            break
    if predictor_path is not None:
        try:
            print('\nAttempting to load dlib shape predictor (this may take a moment)...')
            sp = dlib.shape_predictor(predictor_path)
            print('Loaded shape_predictor OK')
        except Exception as e:
            print('ERROR loading shape_predictor:', e)
    else:
        print('\nNo shape predictor file found to attempt load.')
except Exception as e:
    print('\nSkipping dlib predictor load because dlib import failed:', e)

print('\nSummary:')
for name, ok, msg in checks:
    print(f"- {name}: {'OK' if ok else 'MISSING/ERROR'}{(' - '+msg) if msg else ''}")

print('\nIf all critical packages (numpy, scipy, pandas, cv2, PyQt5, dlib) report OK and at least one .dat shape predictor exists in include/data, you should be able to run `python Emotrics.py`.')
