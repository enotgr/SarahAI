import os

def get_volume() -> int:
  command = "osascript -e 'output volume of (get volume settings)'"
  return int(os.popen(command).read().strip())
