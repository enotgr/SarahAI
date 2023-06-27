import subprocess

# is not working :(
def set_brightness(value: int):
  if not 0 <= value <= 1:
    print('ValueError: Brightness level should be between 0 and 100.')
    return False

  command = f"brightness {value}"
  subprocess.call(command, shell=True)
  return True
