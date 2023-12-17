#!/usr/bin/env python
from pydub import AudioSegment
from pydub.playback import play

munch1 = AudioSegment.from_wav('munch_1.wav')
munch2 = AudioSegment.from_wav('munch_2.wav')

full_munch = munch1 + munch2
play(full_munch)
