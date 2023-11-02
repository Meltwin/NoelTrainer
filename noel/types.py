class Film:
    def __init__(self) -> None:
        self.start = ""
        self.stop = ""
        self.channel = None
        self.title = ""
        self.subtitle = ""
        self.desc = ""
        self.date = ""
        self.category = ""
        self.length = 0
        self.icon = ""
        self.episode_num = ""
        self.audio = ""
        self.rating = ""

    def toJson(self):
        out = "{"

        def addElemStr(key, value) -> str : 
            if value == None:
                return ""
            n_val = value.strip("\r\n").strip().replace("\"", "\\\"")
            if n_val != "":
                return f"\"{key}\":\"{n_val}\","
            return ""
        
        def addDate(key, value) -> str:
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
                return f"\"{key}\":\"{year}-{month}-{day} {hour}:{minutes}:{seconds}\","
            return ""
        
        out += addDate("start", self.start)
        out += addDate("stop", self.stop)
        if self.channel != None:
            out += f"\"channel\": \"{self.channel.name}\","
        out += addElemStr("title", self.title)
        out += addElemStr("subtitle", self.subtitle)
        out += addElemStr("desc", self.desc)
        out += addElemStr("date", self.date)
        out += addElemStr("category", self.category)
        if self.length != 0:
            out += f"\"length\": {self.length},"
        out += addElemStr("icon", self.icon)
        out += addElemStr("audio", self.audio)
        out += addElemStr("rating", self.rating)
        out = out[:-1]
        out += "}"
        return out

class Channel:
    def __init__(self) -> None:
        self.id = ""
        self.name = ""
        self.icon = ""

    def __eq__(self, __value: any) -> bool:
        if type(__value) is not Channel:
            return False
        return self.id == __value.id
    
    def __str__(self):
        return f"Channel {self.name} [{self.id}] -> {self.icon}"

class TVProgram:
    def __init__(self) -> None:
        self.channels = []
        self.films = []