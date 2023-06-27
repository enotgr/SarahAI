import cv2
from fer import FER

class EmotionsDetector:
  def __init__(self):
    self.emotion = 'neutral'
    self._cap = None
    self._detector = None

    self.is_running = False

  def init(self):
    if self.is_running:
      return

    self._cap = cv2.VideoCapture(1)
    self._detector = FER()
    self.is_running = True

  def destroy(self):
    if not self.is_running:
      return

    self.is_running = False
    self._cap.release()
    self._cap = None
    self._detector = None

  def detect_emotion(self) -> str:
    if not self.is_running:
      return

    _, frame = self._cap.read()
    res = self._detector.detect_emotions(frame)
    emotions: dict[str, int] = res[0].get('emotions')
    emotions_keys = emotions.keys()

    if not len(emotions_keys):
      return

    emotion = 'neutral'
    max_emotion_count = 0.0

    for key in emotions_keys:
      if emotions[key] > max_emotion_count:
        emotion = key
        max_emotion_count = emotions[key]

    self.emotion = emotion
    print('Your emotion:', emotion)

emotions_detector = EmotionsDetector()
