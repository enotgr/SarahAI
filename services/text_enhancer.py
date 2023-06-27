import gc
import torch

# Этот сервис умеет расставлять знаки препинания в тексте
# Но с одновременным использованием модели синтеза речи этот сервис делает дичь
# Пока не разобрался в чем дело
class TextEnhancer:
  def enhance_text(self, text: str, lang: str = 'ru'):
    if not text:
      return ''

    torch.backends.quantized.engine = 'qnnpack'
    model = self._get_model()

    text = model.enhance_text(text, lan=lang)
    model = None
    del model
    gc.collect()
    return text

  def _get_model(self):
    model, _, _, _, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                         model='silero_te',)
    return model

text_enhancer = TextEnhancer()
