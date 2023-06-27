import subprocess

def create_note(title: str, body: str):
  script = f'''
  tell application "Notes"
    tell account "iCloud"
      make new note at folder "Notes" with properties {{name: "{title}", body: "{body}"}}
    end tell
  end tell
  '''
  subprocess.run(['osascript', '-e', script])
