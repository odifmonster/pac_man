#!/usr/bin/env python
import os
from pydub import AudioSegment

if __name__ == '__main__':
    SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

    sirens = sorted([f for f in os.listdir(os.path.join(SCRIPT_DIR, 'wgot')) if 'siren' in f])
    sirens = [AudioSegment.from_file(os.path.join(SCRIPT_DIR, 'wgot', s), format='wav') + 9 for s in sirens]

    for i, s in enumerate(sirens):
        cut_s = s[10:]
        s.export(f'siren_{i+1}.wav', format='wav')
