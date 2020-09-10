import os
from syncP import mpv

class player:
    def __init__(self):
        self.player = mpv.MPV(ytdl=True, input_default_bindings=True, input_vo_keyboard=True, osc=True)
        self.selected = self.selectMedia()
        os.system('cls' if os.name == 'nt' else 'clear')
        self.conns = None

    def start(self, conns, payload=None):
        player = self.player
        self.conns = conns

        @player.on_key_press("q")
        def on_quit():
            cur = conns.head
            while cur:
                cur.conn.send("quit".encode())
                cur = cur.next
            self.quit()

        @player.on_key_press("space")
        def on_toggle():
            cur = conns.head
            while cur:
                cur.conn.send("toggle".encode())
                cur = cur.next
            self.toggle()


        @player.on_key_press("s")
        def on_sync():
            self.sync()

        print("\n--------------------------------\n")
        print("\nNow Playing \n"+os.path.basename(self.selected)+"...")
        print("\n\n\t\t####################\n")
        print("\t\tKeyboard shortcuts~\n", "\t\t<space>    -toggle play/pause","\t\ts    -sync all clients (only host)" ,"\t\tq    -quit", sep="\n")
        print("\n\n\t\t####################")
        self.player.play(self.selected)
        self.pause()
        if payload != None:
            while self.player.time_pos == None:
                continue
            self.player.seek(payload[6:],reference="absolute")
        self.player.wait_for_playback()


    def sync(self):
        cur = self.conns.head
        payload = "sync: "+str(self.player.time_pos)
        while cur:
            cur.conn.send(payload.encode())
            cur = cur.next

    def quit(self):
        self.player.quit()

    def toggle(self):
        self.player.cycle("pause")

    def pause(self):
        self.player.command("set","pause", "yes")

    def selectMedia(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        files = os.listdir('.')
        print("List of files in this directory:\n\n")
        for i in range(len(files)):
            print('['+str(i)+'] '+files[i])
        print("\n\nEnter the file number to select: ")

        return os.path.abspath(files[int(input())])


