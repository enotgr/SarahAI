def get_suffix(value: int, suffixes: list[str]) -> str:
  if len(suffixes) != 3:
    return ''

  rest_of_100 = value % 100

  if rest_of_100 > 10 and rest_of_100 < 20:
    return suffixes[2]

  rest = value % 10

  if rest == 1:
    return suffixes[0]

  if rest > 1 and rest < 5:
    return suffixes[1]
  return suffixes[2]
