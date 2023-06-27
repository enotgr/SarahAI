from num2words import num2words

def number_to_words(text: str) -> str:
  for word in text.split():
    if word.isdigit():
      word_to_words = num2words(int(word), lang='ru')
      text = text.replace(word, word_to_words)
  return text
