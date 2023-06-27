from .get_brightness import get_brightness
from .set_brightness import set_brightness

# is not working :(
def decrease_brightness(value: int = 10):
  value /= 100
  new_brightness = max(0, get_brightness() - value)
  set_brightness(new_brightness)
