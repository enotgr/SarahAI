from Levenshtein import distance

def get_lev_dist(a: str, b: str):
  res = distance(a, b)
  print(res)

get_lev_dist('пока', 'до вчера')
