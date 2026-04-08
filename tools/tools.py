from .get_weather import Weather
from .open_app import LocalApp
from .spotify import Spotify
from .yt import Youtube
from .whatsapp import WhatsApp

#objects
weather = Weather()
localapp = LocalApp()
spotify = Spotify()
yt = Youtube()
wh = WhatsApp()

# tool map
TOOL_MAP = {
    "current_weather": weather.getWeather,
    "open_app": localapp.open_app,
    "play_spotify_song" : spotify.play_spotify_song,
    "play_spotify_playlist" : spotify.play_spotify_playlist,
    "get_spotify_song_link" : spotify.get_spotify_song_link,
    "play_youtube_video" : yt.play_youtube_video,
    "send_whastapp_message" : wh.send_whastapp_message
}


# avaliable tools and its schema
TOOLS_SCHEMA = [

    # get weather - tool
    {
        "type": "function",
        "function": {
            "name": "current_weather",
            "description": "Get current weather of a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    },

    # open an app - tool
    {
        "type": "function",
        "function": {
            "name": "open_app",
            "description": "Open an app",
            "parameters": {
                "type": "object",
                "properties": {
                    "app": {"type": "string"}
                },
                "required": ["app"]
            }
        }
    },


    # play a spotify song - tool
    {
        "type": "function",
        "function": {
            "name": "play_spotify_song",
            "description": "play a spotify song",
            "parameters": {
                "type": "object",
                "properties": {
                    "song_name": {"type": "string"}
                },
                "required": ["song_name"]
            }
        }
    },

    #play a spotify playlist - tool
    {
        "type": "function",
        "function": {
            "name": "play_spotify_playlist",
            "description": "play a spotify playlist",
            "parameters": {
                "type": "object",
                "properties": {
                    "playlist_name": {"type": "string"}
                },
                "required": ["playlist_name"]
            }
        }
    },

    #get spotify song link
    {
        "type": "function",
        "function": {
            "name": "get_spotify_song_link",
            "description": "get a spotify song link",
            "parameters": {
                "type": "object",
                "properties": {
                    "song_name": {"type": "string"}
                },
                "required": ["song_name"]
            }
        }
    },


    #play yt video
    {
        "type": "function",
        "function": {
            "name": "play_youtube_video",
            "description": "play a youtube video",
            "parameters": {
                "type": "object",
                "properties": {
                    "search": {"type": "string"}
                },
                "required": ["search"]
            }
        }
    },

    #send a message on whatsapp
    {
        "type": "function",
        "function": {
            "name": "send_whastapp_message",
            "description": "send_whastapp_message",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"name": "string"},
                    "message" : {"message": "string"}
                },
                "required": ["name", "message"]
            }
        }
    },

]
