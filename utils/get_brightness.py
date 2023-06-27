import subprocess

# is not working :(
def get_brightness():
  command = "brightness -l | grep 'display 0: brightness' | cut -f4 -d' '"
  output = subprocess.check_output(command, shell=True)
  if not output:
    return 0.5
  return float(output.decode().strip())
