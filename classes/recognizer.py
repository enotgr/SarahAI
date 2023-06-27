import speech_recognition as sr

# from services import text_enhancer

class VoiceRecognizer:
  def __init__(self, timeout: int = 1, phrase_time_limit: int = 5):
    self.recognizer = sr.Recognizer()
    self.timeout = timeout
    self.phrase_time_limit = phrase_time_limit

  def recognize_voice(self) -> str:
    text = ''
    try:
      with sr.Microphone() as source:
        print('Listening...')
        audio = self.recognizer.listen(source, self.timeout, self.phrase_time_limit)

        # Используем Google Web Speech API для распознавания речи
        text = self.recognizer.recognize_google(audio, language='ru-RU')

        # Восстанавливаем пунктуацию в тексте
        # enhanced_text = text_enhancer.enhance_text(text)
        # print(f'You: {enhanced_text}')
        print(f'You: {text}')
    except sr.UnknownValueError:
        print('Google Web Speech API did not understand the audio')
    except sr.RequestError as e:
        print(f'Could not request results from Google Web Speech API; {e}')
    except sr.WaitTimeoutError as e:
        print(f'Timeout error; {e}')
    # if need_enhance:
    #   return enhanced_text
    return text
