from MisskeyNoteCore import MyMisskey
import requests
import configparser


class NowplayingMisskey(MyMisskey):
    def __init__(self) -> None:
        config_load = configparser.ConfigParser()
        try:
            config_load.read('config.ini')
            self.lastfmapikey = config_load.get("SETTING","LASTFM_KEY")
            self.userid = config_load.get("SETTING","LASTFM_USRID")
            self.misskey_instance = config_load.get("SETTING","MISSKEY_INSTANCE")
            self.misskey_apitoken = config_load.get("SETTING","MISSKEY_TOKEN")
            super().__init__(self.misskey_instance,self.misskey_apitoken)
            self.latest = config_load.get("SETTING","LATEST")
        except:
            self.lastfmapikey = input("Set Your Last.fm API Key: ")
            self.userid = input("Set Your Last.fm user ID: ")
            self.misskey_instance = input("Set Your Misskey Instance: ")
            self.misskey_apitoken = input("Set Your Misskey API acsess token: ")
            self.latest = ""
            super().__init__(self.misskey_instance,self.misskey_apitoken)
    def SaveSetting(self):
        config_save = configparser.RawConfigParser()
        config_save.add_section("SETTING")
        config_save.set("SETTING", 'LASTFM_USRID', self.userid)
        config_save.set("SETTING", 'LASTFM_KEY', self.lastfmapikey)
        config_save.set("SETTING", 'LATEST', self.ScrobbleInfo["url"])
        config_save.set("SETTING", 'MISSKEY_INSTANCE', self.misskey_instance)
        config_save.set("SETTING","MISSKEY_TOKEN",self.misskey_apitoken)
        with open('config.ini', 'w') as file:
            config_save.write(file)
        return
    def GetScrobble(self):
        # 取得先URLにアクセス
        # 対象を抽出
        headers = {"content-type": "application/json"}
        APIreq = requests.get(f"https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={self.userid}&api_key={self.lastfmapikey}&format=json", headers=headers)
        APIjson = APIreq.json()
        self.ScrobbleInfo = {
            "title" : APIjson["recenttracks"]["track"][0]["name"],
            "artist" : APIjson["recenttracks"]["track"][0]["artist"]["#text"] if APIjson["recenttracks"]["track"][0]["artist"]["#text"] != "不明なアーティスト" else "",
            "album" : APIjson["recenttracks"]["track"][0]["album"]["#text"],
            "url" : APIjson["recenttracks"]["track"][0]["url"],

        }
        if self.latest != self.ScrobbleInfo["url"]:
            NoteTEXT =f"#nowplaying {self.ScrobbleInfo['title']} - {self.ScrobbleInfo['artist']} {self.ScrobbleInfo['album']}"
            print(self.ScrobbleInfo['url'])
            self.Note(NoteTEXT)
            self.SaveSetting()



MisskeyClient = NowplayingMisskey()
MisskeyClient.GetScrobble()
