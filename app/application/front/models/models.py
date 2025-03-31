from dataclasses import dataclass, field


@dataclass
class User:
    oid:int = field(default=None)
    nickname:str = field(default="")
    login:str = field(default="")
    token:str = field(default="")

    def clear(self):
        self.oid = None
        self.nickname = ""
        self.login = ""
        self.token = ""