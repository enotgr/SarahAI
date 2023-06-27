from .get_volume import get_volume
from .set_volume import set_volume

def increase_volume(value: int = 10):
  new_volume = min(100, get_volume() + value)
  set_volume(new_volume)
