import pyaudio
import numpy as np

class AudioFrameGetter:
  def __init__(self, rate: int = 16000, frame_length: int = 512):
    self.rate = rate
    self.frame_length = frame_length
    self.audio: pyaudio.PyAudio = None
    self.stream: pyaudio._Stream = None

  def get_next_audio_frame(self):
    buffer = self.stream.read(self.frame_length)
    frame = np.frombuffer(buffer, dtype=np.int16)
    return frame

  def open(self):
    if self.audio is None and self.stream is None:
      self.audio = pyaudio.PyAudio()
      self.stream = self.audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=self.rate,
        input=True,
        frames_per_buffer=self.frame_length
      )

  def close(self):
    if self.stream is not None:
      self.stream.stop_stream()
      self.stream.close()
      self.stream = None
    if self.audio is not None:
      self.audio.terminate()
      self.audio = None

  def is_open(self):
    return self.audio is not None and self.stream is not None
