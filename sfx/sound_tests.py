#!/usr/bin/env python
from pydub import AudioSegment
from pydub.playback import play

death1 = AudioSegment.from_file('death_1.wav', format='wav', sample_width=1) + 4
death2 = AudioSegment.from_file('death_2.wav', format='wav', sample_width=1) + 4
pause = AudioSegment.silent(duration=10)
death_end = death2+pause+death2+pause*8
full_death = death1[:1350] + death_end

play(full_death)
