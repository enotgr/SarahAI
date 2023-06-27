from IPython.display import Audio
import simpleaudio as sa

def play_sound(file_path):
  audio = Audio(file_path, autoplay=True)
  sa.play_buffer(audio.data[128:], 1, 2, 44100).wait_done()
