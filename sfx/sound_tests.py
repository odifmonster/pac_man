#!/usr/bin/env python
from pydub import AudioSegment
from pydub.playback import play

start_up = AudioSegment.from_file('wgot/game_start.wav', format='wav') + 9
start_up.export('siren_0.wav', format='wav')