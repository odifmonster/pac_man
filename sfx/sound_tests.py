#!/usr/bin/env python
from pydub import AudioSegment
from pydub.playback import play

munch1 = AudioSegment.from_file('munch_1.wav', format='wav', sample_width=1)
munch2 = AudioSegment.from_file('munch_2.wav', format='wav', sample_width=1)
pause = AudioSegment.silent(duration=80)

full_munch = munch1 + pause + munch2 + pause
play(full_munch*4)
