import os
from syncP import mpv

class player:
    def __init__(self):
        self.player = mpv.MPV(ytdl=True, input_default_bindings=True, input_vo_keyboard=True)
        self.selected = self.selectMedia()
        self.curr_time = None

    def start(self, conns):
        player = self.player
        @player.property_observer('time-pos')
        def time_observer(_name, value):
            self.curr_time = value

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
            cur = conns.head
            payload = "sync: "+str(self.curr_time)
            while cur:
                cur.conn.send(payload.encode())
                cur = cur.next

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Now Playing \n"+os.path.basename(self.selected)+"...")
        self.player.play(self.selected)
        self.pause()
        self.player.wait_for_playback()


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


