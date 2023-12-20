#!/usr/bin/env python
import os
from pydub import AudioSegment

def main():
    SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

    munch1 = AudioSegment.from_file(os.path.join(SCRIPT_DIR, 'munch_1.wav'),
                                    format='wav',
                                    sample_width=1)
    munch2 = AudioSegment.from_file(os.path.join(SCRIPT_DIR, 'munch_2.wav'),
                                    format='wav',
                                    sample_width=1)
    pause = AudioSegment.silent(duration=80)

    one_munch = munch1+pause+munch2+pause
    several_munches = one_munch*8
    several_munches.export('waka.wav', format='wav')

if __name__ == '__main__':
    main()