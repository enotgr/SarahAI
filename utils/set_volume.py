import os

def set_volume(value: int = 0):
  if not 0 <= value <= 100:
    print('ValueError: Volume value should be between 0 and 100.')
    return False

  os.system(f"osascript -e 'set volume output volume {value}'")
  return True
