# Based on THeK3nger's WavePlayerLoop class: https://tinyurl.com/yaullc85

import os
import wave
import threading
import pyaudio

from time import sleep


# Plays the given wav file
class WavePlayer(threading.Thread):
    # The number of frames read for each chunk of audio
    CHUNK = 1024
    
    # Initializes the WavePlayer
    def __init__(self, file_path, loop):
        super(WavePlayer, self).__init__()
        self.original_path = file_path
        self.file_path = os.path.abspath(file_path)
        self.loop = loop
        self.is_playing = False
        self.first_time = True
        self.wf = wave.open(self.file_path, 'rb')
        self.player = pyaudio.PyAudio()
        self.stream = self.player.open(format=self.player.get_format_from_width(self.wf.getsampwidth()),
                                       channels=self.wf.getnchannels(),
                                       rate=self.wf.getframerate(),
                                       output=True)
    
    # Runs the audio file
    def run(self):
        
        # Closes the stream after two seconds (The stream would otherwise usually close without finishing the audio)
        def close(closing_stream, closing_player):
            sleep(2)
            closing_stream.close()
            closing_player.terminate()
        
        # Plays the audio if it is supposed to be playing
        while self.is_playing and (self.first_time or self.loop):
            # Gets CHUNK frames of audio and writes it to the stream (to be played)
            data = self.wf.readframes(self.CHUNK)
            self.stream.write(data)
            
            # If the end of the data is reached and the file is supposed to loop,
            # the audio reader is put back at the beginning of the file data
            if data == b'':
                self.first_time = False
                if self.loop:
                    self.wf.rewind()
                
        # Closes the stream and player
        stop_it = threading.Thread(target=close, args=(self.stream, self.player))
        stop_it.start()

        # Reloads thread so it can be reused
        WavePlayer.__init__(self, self.original_path, self.loop)
        
    # Plays the audio file if it is not already being played
    def play(self):
        self.is_playing = True
        
        # Plays the audio if it is not already playing
        if not self.is_alive():
            self.start()
    
    # Stops the audio playback
    def stop(self):
        self.is_playing = False
