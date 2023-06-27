from .get_volume import get_volume
from .set_volume import set_volume

def decrease_volume(value: int = 10):
  new_volume = max(0, get_volume() - value)
  set_volume(new_volume)
