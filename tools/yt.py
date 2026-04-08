import pywhatkit

class Youtube:

  #play youtube video
  def play_youtube_video(self, search: str):
    pywhatkit.playonyt(search)
    return f"{search} youtube video playing"
