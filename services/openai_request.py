import openai
# from .file_service import file_service
from consts import OPENAI_ORGANIZATION, OPENAI_API_KEY

# Use your organization and API keys
openai.organization = OPENAI_ORGANIZATION
openai.api_key = OPENAI_API_KEY

class OpenAIRequest:
  def __init__(self, context_messages: list[dict[str, str]] = []):
    # self.context: str
    # self.context_path: str = 'save/context2.txt'
    self.messages = context_messages

    # if context:
    #   self.context = context
    # else:
    #   self.context = self._load_context()

  # def get_openai_response(self, question):
  #   self.context = f'{self.context}\n\nВопрос: {question}?\nОтвет:'
  #   response = openai.Completion.create(
  #     model='text-davinci-003',
  #     prompt=self.context,
  #     temperature=0,
  #     max_tokens=150,
  #     top_p=1,
  #     frequency_penalty=0.0,
  #     presence_penalty=0.0,
  #     stop=['\n']
  #   )

  #   answer = response.get('choices')[0].get('text')
  #   self.context = f'{self.context} {answer}'

  #   self._update_context()

  #   return answer

  def lets_talk(self, text: str):
    if not text:
      return

    self.messages.append({ 'role': 'user', 'content': text })

    print('Request to openai...')
    response = openai.ChatCompletion.create(
      model='gpt-3.5-turbo',
      messages=self.messages,
      temperature=0.9,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0.0,
      presence_penalty=0.6,
    )

    answer = response.get('choices')[0].get('message').get('content')
    self.messages.append({ 'role': 'assistant', 'content': answer})

    return answer

  # def lets_talk(self, text):
  #   print('Request to openai...')
  #   self.context = f'{self.context}\n\nЧеловек: {text}\nИИ:'
  #   response = openai.Completion.create(
  #     model='text-davinci-003',
  #     prompt=self.context,
  #     temperature=0.9,
  #     max_tokens=200,
  #     top_p=1,
  #     frequency_penalty=0.0,
  #     presence_penalty=0.6,
  #     stop=[' Человек:', ' ИИ:']
  #   )

  #   answer = response.get('choices')[0].get('text')
  #   self.context = f'{self.context} {answer}'

  #   self._update_context()

  #   return answer

  def reset_context(self):
    # file_service.saveTextFile('Далее следует разговор с ИИ-помощником. Помощник полезен, креативен, умен и очень дружелюбен.', self.context_path)
    self.messages = []

  # def _load_context(self):
  #   return file_service.getTextFileByPath(self.context_path)

  # def _update_context(self):
  #   file_service.saveTextFile(self.context, self.context_path)

openai_request = OpenAIRequest()
