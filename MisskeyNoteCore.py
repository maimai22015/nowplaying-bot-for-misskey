from misskey import Misskey

class MyMisskey:
    def __init__(self,MISSKEY_INSTANCE = None,MISSKEY_TOKEN = None) -> None:
        # Usage: Overwrite this class and load&set misskey setting.
        if MISSKEY_INSTANCE == None or MISSKEY_TOKEN == None:
            MISSKEY_INSTANCE = input("Set Your Misskey Instance: ")
            MISSKEY_TOKEN = input("Set You Misskey API acsess token: ")
        self.mk = Misskey(MISSKEY_INSTANCE)
        self.mk.token = MISSKEY_TOKEN
    def Note(self, NoteText):
        # エスケープ
        new_note = self.mk.notes_create(text=NoteText.replace('殺', '.').replace('@', '@.').replace('http', 'http.'),visibility="home")
        return
