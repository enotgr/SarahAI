from .answers import HOW_ARE_YOU_PHRASES, WELCOME_PHRASES

ACTIVATE_COMMANDS = ['сара']
DEACTIVATE_COMMANDS = ['до свидания', 'не слушай', 'не подслушивай', 'перестань слушать', 'хватит слушать', 'режим ожидания']

DESTROY_COMMANDS = ['деактивация', 'завершение работы', 'на сегодня хватит', 'заверши работу', 'выключись', 'отключись', 'пора спать', 'ты мне надоела']

ACTIVATE_OPENAI_MOD_COMMANDS = ['включи мозги', 'думай', 'давай поговорим', 'давай поболтаем']
DEACTIVATE_OPENAI_MOD_COMMANDS = ['выключи мозги', 'перестань думать', 'хватит думать']

ACTIVATE_EMOTION_DETECTOR_COMMANDS = ['включи зрение', 'открой глаза']
DEACTIVATE_EMOTION_DETECTOR_COMMANDS = ['выключи зрение', 'закрой глаза']

GOOGLE_REQUEST_COMMANDS = ['загугли']

OPEN_BROWSER_COMMANDS: list[dict[str, str or list[str]]] = [
  {
    'keys': [
      'открой поисковик',
      'открой гугл',
      'открой google',
    ],
    'target': 'https://www.google.com'
  },
  {
    'keys': [
      'открой видео',
      'открой ютуб',
      'открой ютьюб',
      'открой youtube',
    ],
    'target': 'https://youtube.com'
  }
]

OPEN_TELEGRAM_COMMANDS: list[dict[str, str or list[str]]] = [
  {
    'keys': [
      'открой телегу',
      'открой телеграмм',
      'открой телеграм',
      'открой telegram',
    ],
    'target': '',
  },
  {
    'keys': [
      'сообщение наташе',
      'сообщение наташа',
    ],
    'target': 'tetta_0',
  },
  {
    'keys': [
      'сообщение славе',
      'сообщение слава',
    ],
    'target': 'CurtCoban',
  }
]

FIND_VIDEO_COMMANDS = ['найди видео']

CREATE_NOTE_COMMANDS = ['запиши']

INCREASE_VOLUME_COMMANDS = ['прибавь громкость']
DECREASE_VOLUME_COMMANDS = ['убавь громкость']
SET_VOLUME_COMMANDS = ['установи громкость на']

INCREASE_BRIGHTNESS_COMMANDS = ['прибавь яркость']
DECREASE_BRIGHTNESS_COMMANDS = ['убавь яркость']
SET_BRIGHTNESS_COMMANDS = ['установи яркость на']

THANKS_COMMANDS = ['спасибо', 'благодар']

WEATHER_COMMANDS = ['погода']

TALK_COMMANDS = [
  {
    'commands': ['спасибо', 'благодар'],
    'answers': WELCOME_PHRASES,
  },
  {
    'commands': ['как дела', 'как ты', 'ты как', 'как оно', 'как поживаешь'],
    'answers': HOW_ARE_YOU_PHRASES,
  },
]
