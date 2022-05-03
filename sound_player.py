
import numpy as np
import pygame

class SoundPlayer:
    def __init__(self, count):
        self.count = count

        self.notes = {} # dict to store samples
        START = 50 # start frequency
        STOP = 1000
        self.SOUND_COUNT = 20
        SOUND_STEP = (STOP - START) // self.SOUND_COUNT

        for i in range(self.SOUND_COUNT):
            freq = START + i * SOUND_STEP
            sample = SoundPlayer.synth(freq, 0.05, 66123)
            self.notes[i] = sample

    @staticmethod
    def synth(frequency, duration=1.5, sampling_rate=44100):
        frames = int(duration*sampling_rate)
        arr = np.cos(2*np.pi*frequency*np.linspace(0,duration, frames))
        arr = arr + np.cos(4*np.pi*frequency*np.linspace(0,duration, frames))
        arr = arr - np.cos(6*np.pi*frequency*np.linspace(0,duration, frames))
        sound = np.asarray([32767*arr,32767*arr]).T.astype(np.int16)
        sound = pygame.sndarray.make_sound(sound.copy())
        sound.set_volume(0.008)
        
        return sound

    def play(self, i):
        i = self.SOUND_COUNT * i // self.count
        self.notes[i].play()

