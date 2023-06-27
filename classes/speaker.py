import re
import torch
import simpleaudio as sa
from IPython.display import Audio

from helpers import number_to_words

class Speaker:
  def __init__(self, character: str = 'xenia', sample_rate: int = 48000):
    self._model = self._get_model()
    self._character: str = character
    self._sample_rate: int = sample_rate

  def speak(self, text: str = ''):
    if not text:
      return

    # if not self._is_not_english(text):
      # text = 'Пока я говорю только на русском языке.'
    text = self._remove_english_letters(text)
    text = number_to_words(text)

    print(f'SarahAI: {text}')
    try:
      self._play_synthesize_speech(text)
    except:
      self._play_synthesize_speech('Я не знаю, как это произнести:')
      print(f'Problems with text: {text}')

  def _play_synthesize_speech(self, text: str):
    put_accent=True
    put_yo=True

    res_audio = self._model.apply_tts(text=text,
                            speaker=self._character, # aidar, baya, kseniya, xenia, eugene, random
                            sample_rate=self._sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo)
    audio = Audio(res_audio, rate=self._sample_rate)
    sa.play_buffer(audio.data[64:], 1, 2, self._sample_rate).wait_done()

  def _get_model(self):
    language = 'ru'
    model_id = 'v3_1_ru'
    # device = torch.device('cpu')
    model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                         model='silero_tts',
                                         language=language,
                                         speaker=model_id)
    # model.to(device)
    return model

  def _remove_english_letters(self, text: str) -> str:
    return re.sub(r'[a-zA-Z]', '', text)

  # deprecated
  def _is_not_english(self, text: str) -> bool:
    return not bool(re.search('[a-zA-Z]', text))
