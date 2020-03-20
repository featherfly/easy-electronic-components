class Sound:
    def stop(self, force=False):
        pass

class Sounder:
    def vocalize(self, sound):
        return Sound(sound)

import subprocess
import sys
import os
import logging
import time

class Speaker(Sounder):
    ESPEAK = "espeak"

    def __init__(self, single=False):
        self.set_default()
        self.single = single

    def vocalize(self, sound):
        if self.single:
            self._stop()
        cmds = [self.ESPEAK, "-v", self.language, "-g", str(self.gap) , "-s", str(self.rate), sound]
        logging.debug(cmds)
        self.sound = subprocess.Popen(cmds, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        return SpeakerSound(self.sound)

    def _stop(self, force=False):
        if (self.sound == None or self.sound.returncode != None):
            return
        if force:
            self.sound.kill()
            return
        self.sound.terminate()

    def set_default(self):
        self.rate = 120
        self.language = 'zh'
        self.gap = 35

    def set_volume(self, volume):
        self.volume = volume

    def set_language(self, language):
        self.language = language

    def set_rate(self, rate):
        self.rate = rate

    def set_wordgap(self, gap):
        self.gap = gap

class SpeakerSound(Sound):
    def __init__(self, popen:subprocess.Popen):
        self.popen = popen

    def stop(self, force=False):
        if (self.popen == None or self.popen.returncode != None):
            return
        if force:
            self.popen.kill()
            return
        self.popen.terminate()

from playsound import playsound

class Player(Sounder):
    def __init__(self, single=False):
        self.single = single

    def vocalize(self, audio_file_path):
        cmds = ["ffplay", "-nodisp", "-autoexit", audio_file_path]
        logging.debug(cmds)
        self.sound = subprocess.Popen(cmds, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        return PlayerSound(self.sound)

class PlayerSound(Sound):
    def __init__(self, popen:subprocess.Popen):
        self.popen = popen

    def stop(self, force=False):
        if (self.popen == None or self.popen.returncode != None):
            return
        if force:
            self.popen.kill()
            return
        self.popen.terminate()