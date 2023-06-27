import webbrowser
import random
import urllib.parse
import pvporcupine

from consts import DEACTIVATE_COMMANDS, ACTIVATE_OPENAI_MOD_COMMANDS, DEACTIVATE_OPENAI_MOD_COMMANDS, GOOGLE_REQUEST_COMMANDS, OPEN_BROWSER_COMMANDS, OPEN_TELEGRAM_COMMANDS, FIND_VIDEO_COMMANDS, CREATE_NOTE_COMMANDS, INCREASE_VOLUME_COMMANDS, DECREASE_VOLUME_COMMANDS, SET_VOLUME_COMMANDS, WEATHER_COMMANDS, DESTROY_COMMANDS, HELLO_PHRASES, TALK_COMMANDS, ACTIVATE_EMOTION_DETECTOR_COMMANDS, DEACTIVATE_EMOTION_DETECTOR_COMMANDS, PICOVOIVE_ACCESS_KEY
from classes import VoiceRecognizer, Speaker
from services import google_request, openai_request, weather, emotions_detector
from utils import create_note, increase_volume, decrease_volume, set_volume, play_sound

class CommandHandler:
  def __init__(self, voice_recognizer: VoiceRecognizer, speaker: Speaker, audio_frame_getter):
    self._voice_recognizer: VoiceRecognizer = voice_recognizer
    self._speaker: Speaker = speaker

    self._keywords = ['commands/sarah.ppn']
    self._porcupine_handler: pvporcupine.Porcupine = None
    self._audio_frame_getter = audio_frame_getter

    self._is_chat_active: bool = False
    self._is_openai_mod: bool = False

    self._is_running: bool = False
    self._silence_count: int = 0

  def listening(self):
    self._is_running = True
    while self._is_running:
      if self._is_chat_active:
        self._phrase_handler()
        continue
      else:
        self._check_activate()

  def _check_activate(self):
    if not self._audio_frame_getter.is_open():
      self._audio_frame_getter.open()
    # Use your Picovoice access key (https://console.picovoice.ai/)
    self._porcupine_handler = pvporcupine.create(access_key=PICOVOIVE_ACCESS_KEY, keyword_paths=self._keywords)

    print('Waiting for an activation phrase...')

    try:
      while True:
        pcm = self._audio_frame_getter.get_next_audio_frame()
        keyword_index = self._porcupine_handler.process(pcm)
        if keyword_index >= 0:
          self._is_chat_active = True
          hello_phrase_index: int = random.randint(0, len(HELLO_PHRASES) - 1)
          hello_phrase: str = HELLO_PHRASES[hello_phrase_index]
          self._speaker.speak(hello_phrase)
          break
    finally:
      if self._is_chat_active:
        self._audio_frame_getter.close()
        self._porcupine_handler.delete()

  def _phrase_handler(self):
    phrase: str = ''
    self._silence_count = 0
    while self._is_chat_active:
      if self._silence_count > 1:
        emotions_detector.destroy()
        self._is_chat_active = False
        print('*** Deactivated ***')
        play_sound('sounds/deactivated.wav')
        continue

      emotions_detector.detect_emotion()
      last_emotion = emotions_detector.emotion

      if emotions_detector.emotion == 'sad' and emotions_detector != last_emotion:
        self._speaker.speak('Вижу, что вам грустно. Могу я посоветовать вам какой-нибудь фильм?')

      phrase = self._voice_recognizer.recognize_voice()

      if not phrase:
        self._silence_count += 1
        continue
      else:
        self._silence_count = 0

      if 'давай' in phrase.lower():
        answer = openai_request.lets_talk('Посоветуй какой-нибудь фильм для поднятия настроения')
        self._speaker.speak(answer)
        self._is_openai_mod = True
        self._openai_talk()
        continue

      if self._check_destroy(phrase):
        continue

      if self._check_deactivate(phrase):
        continue

      if self._includes_command(phrase, ACTIVATE_OPENAI_MOD_COMMANDS):
        self._speaker.speak('Мозги актив+ированы. Теперь можем общаться на любые темы! Чем я могу быть пол+езна?')
        self._is_openai_mod = True
        self._openai_talk()
        continue

      if self._check_activate_emotions_detection(phrase):
        continue

      if self._check_deactivate_emotions_detection(phrase):
        continue

      if self._check_google(phrase):
        continue

      if self._check_open_browser(phrase):
        continue

      if self._check_open_telegram(phrase):
        continue

      if self._check_find_video(phrase):
        continue

      if self._check_create_note(phrase):
        continue

      if self._check_increase_volume(phrase) or self._check_decrease_volume(phrase) or self._check_set_volume(phrase):
        continue

      if self._check_weather(phrase):
        continue

      if self._check_talk(phrase):
        continue

      # self._speaker.speak(phrase)

  def _check_deactivate(self, phrase: str):
    if self._includes_command(phrase, DEACTIVATE_COMMANDS):
      self._is_chat_active = False
      self._speaker.speak('Отключаюсь...')
      return True
    return False

  def _check_destroy(self, phrase: str):
    if self._includes_command(phrase, DESTROY_COMMANDS):
      emotions_detector.destroy()
      self._is_chat_active = False
      self._is_running = False
      self._speaker.speak('Завершаю работу...')
      return True
    return False

  def _check_google(self, phrase: str = '') -> bool:
    if not phrase:
      return

    for command in GOOGLE_REQUEST_COMMANDS:
      if command in phrase:
        phrase = phrase.replace(command, '').strip()
        answer = google_request.find(phrase)

        if not answer:
          answer = f'Я не смогла ничего найти по запросу "{phrase}" в Г+угле.'
        self._speaker.speak(answer)
        return True
    return False

  def _openai_talk(self):
    while self._is_openai_mod:
      phrase: str = self._voice_recognizer.recognize_voice()

      if self._silence_count > 1:
        emotions_detector.destroy()
        # TODO: Может и не надо отключать мозги?
        self._is_openai_mod = False
        self._is_chat_active = False
        openai_request.reset_context()
        print('*** Deactivated ***')
        play_sound('sounds/deactivated.wav')
        continue

      if not phrase:
        self._silence_count += 1
        continue

      if self._includes_command(phrase, DEACTIVATE_OPENAI_MOD_COMMANDS):
        self._speaker.speak('Мозги деактив+ированы.')
        self._is_openai_mod = False
        openai_request.reset_context()
        continue

      answer = openai_request.lets_talk(phrase)
      self._speaker.speak(answer)

  def _check_activate_emotions_detection(self, phrase: str) -> bool:
    if self._includes_command(phrase, ACTIVATE_EMOTION_DETECTOR_COMMANDS):
      if emotions_detector.is_running:
        return True
      emotions_detector.init()
      self._speaker.speak('Рада вас видеть!')
      return True
    return False

  def _check_deactivate_emotions_detection(self, phrase: str) -> bool:
    if self._includes_command(phrase, DEACTIVATE_EMOTION_DETECTOR_COMMANDS):
      if not emotions_detector.is_running:
        return True
      emotions_detector.destroy()
      return True
    return False

  def _check_open_browser(self, phrase: str) -> bool:
    if not phrase:
      return False

    for command in OPEN_BROWSER_COMMANDS:
      keys = command.get('keys')
      for key in keys:
        if key in phrase.lower():
          target = command.get('target')
          webbrowser.open_new_tab(target)
          return True
    return False

  def _check_open_telegram(self, phrase: str):
    if not phrase:
      return False

    for command in OPEN_TELEGRAM_COMMANDS:
      keys = command.get('keys')
      for key in keys:
        if key in phrase.lower():
          url = 'tg://resolve'
          target = command.get('target')
          if target:
            url += f'?domain={target}'
          webbrowser.open(url)
          return True
    return False

  def _check_find_video(self, phrase: str):
    if not phrase:
      return False

    for command in FIND_VIDEO_COMMANDS:
      if command in phrase.lower():
        parts = phrase.split(command)
        search = parts[-1]
        if not len(parts) or not search:
          self._speaker.speak('Я не поняла какое видео найти.')
        else:
          url = f'https://www.youtube.com/results?search_query={urllib.parse.quote(search.strip())}'
          webbrowser.open(url)
        return True
    return False

  def _check_create_note(self, phrase: str):
    if not phrase:
      return False

    phrase_lower = phrase.lower()

    for command in CREATE_NOTE_COMMANDS:
      if command in phrase_lower:
        parts = phrase_lower.split(command)

        if not len(parts):
          self._speaker.speak('Я не поняла, что нужно записать.')
          return True

        note = parts[-1].strip()

        if not note:
          self._speaker.speak('Я не поняла, что нужно записать.')
        else:
          create_note('SaraAI Note', note)
          self._speaker.speak(f'Записала в заметки: "{note}"')
        return True
    return False

  def _check_increase_volume(self, phrase):
    if self._includes_command(phrase, INCREASE_VOLUME_COMMANDS):
      increase_volume()
      self._speaker.speak('Прибавляю!')
      return True
    return False

  def _check_decrease_volume(self, phrase):
    if self._includes_command(phrase, DECREASE_VOLUME_COMMANDS):
      decrease_volume()
      self._speaker.speak('Убавляю...')
      return True
    return False

  def _check_set_volume(self, phrase: str):
    command = self._includes_command(phrase, SET_VOLUME_COMMANDS)
    if not command:
      return False

    value = None
    try:
      s_value = phrase.lower().split(command)[-1].strip()
      if 'максимум' in s_value:
        value = 100
      elif 'минимум' in s_value:
        value = 0
      else:
        value: int = int(s_value)
      if value == None:
        self._speaker.speak('Я не поняла на какое значение установить громкость.')
        return True
    except:
      self._speaker.speak('Кажется, я неправильно услышала число.')
      return True
    set_volume(value)
    self._speaker.speak('Как пожелаете!')
    return True

  def _check_weather(self, phrase: str) -> bool:
    command: str = self._includes_command(phrase, WEATHER_COMMANDS)
    if not command:
      return False

    phrase_lower = phrase.lower()
    parts = phrase_lower.split(command)

    if not len(parts):
      self._speaker.speak('Я не поняла, что о каком городе речь.')
      return True

    city = parts[-1].strip().split()[0]
    res = weather.get_weather(city)
    self._speaker.speak(res)
    return True

  def _check_talk(self, phrase: str) -> bool:
    for command_dict in TALK_COMMANDS:
      commands = list(command_dict.get('commands'))
      if self._includes_command(phrase, commands):
        answers = list(command_dict.get('answers'))
        talk_phrase_index: int = random.randint(0, len(answers) - 1)
        talk_phrase = answers[talk_phrase_index]
        self._speaker.speak(talk_phrase)
        return True
    return False

  def _includes_command(self, phrase: str, commands: list[str]) -> str:
    if not phrase:
      return ''
    for command in commands:
      if command in phrase.lower():
        return command
    return ''
