import pywhatkit

def play_youtube_video(search: str):
  pywhatkit.playonyt(search)
  return f"{search} youtube video playing"
