from typing import Any


class Film:
    def __init__(self) -> None:
        self.start: str = ""
        self.stop: str = ""
        self.channel: Channel|None = Channel()
        self.title: str = ""
        self.subtitle: str|None = ""
        self.desc: str = ""
        self.date: str|None = ""
        self.category: str|None = ""
        self.length: int = 0
        self.icon: str = ""
        self.episode_num: str|None = ""
        self.audio: str|None = ""
        self.rating: str|None = ""

    @staticmethod
    def make_date(value) -> str:
        if value == None:
            return ""
        n_val = value.strip("\r\n").strip().replace("\"", "\\\"")
        if n_val != "":
            year = n_val[:4]
            month = n_val[4:6]
            day = n_val[6:8]
            hour = n_val[8:10]
            minutes = n_val[10:12]
            seconds = n_val[12:14]
            return f"{year}-{month}-{day} {hour}:{minutes}:{seconds}"
        return ""

    def toJson(self):
        out = "{"

        def add_elem(key: str, elem: Any) -> str:
            return f"\"{key}\":\"{elem}\","

        out += add_elem("start", self.start)
        out += add_elem("stop", self.stop)
        if self.channel != None:
            out += add_elem("channel", self.channel.name)
        out += add_elem("title", self.title)
        out += add_elem("subtitle", self.subtitle)
        out += add_elem("desc", self.desc)
        out += add_elem("date", self.date)
        out += add_elem("category", self.category)
        if self.length != 0:
            out += add_elem("length", self.length)
        out += add_elem("icon", self.icon)
        out += add_elem("audio", self.audio)
        out += add_elem("rating", self.rating)
        out = out[:-1]+"}"
        return out

class Channel:
    def __init__(self) -> None:
        self.id = ""
        self.name = ""
        self.icon = ""

    def __eq__(self, __value) -> bool:
        if type(__value) is not Channel:
            return False
        return self.id == __value.id
    
    def __str__(self):
        return f"Channel {self.name} [{self.id}] -> {self.icon}"

class TVProgram:
    def __init__(self) -> None:
        self.channels = []
        self.films = []