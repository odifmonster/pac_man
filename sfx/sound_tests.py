#!/usr/bin/env python
from pydub import AudioSegment
from pydub.playback import play

s3 = AudioSegment.from_file('wgot/siren_3.wav', format='wav')+9
s3_fixed = s3[500:1180]*4

s3_fixed.export('siren_3.wav', format='wav')