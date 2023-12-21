#!/usr/bin/env python
import os
from pydub import AudioSegment

def main():
    SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

    death1 = AudioSegment.from_file(os.path.join(SCRIPT_DIR, 'death_1.wav'),
                                    format='wav',
                                    sample_width=1) + 4
    death2 = AudioSegment.from_file(os.path.join(SCRIPT_DIR, 'death_2.wav'),
                                    format='wav',
                                    sample_width=1) + 4
    
    pause = AudioSegment.silent(duration=10)

    death_end = (death2+pause)*2
    full_death = death1[:1350] + death_end
    full_death.export('death.wav', format='wav')

if __name__ == '__main__':
    main()