from .get_weather import getWeather

#tool map
TOOL_MAP = {
    "current_weather": getWeather
}


#avaliable tools and its schema
TOOLS_SCHEMA = [
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
    }
]
