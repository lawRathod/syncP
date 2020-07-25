import mpv
import os


class player:
    def __init__(self):
        self.player = mpv.MPV(ytdl=True, input_default_bindings=True, input_vo_keyboard=True)
        self.selected = self.selectMedia()
        self.curr_time = None

    def start(self, conn):
        player = self.player
        @player.property_observer('time-pos')
        def time_observer(_name, value):
            self.curr_time = value

        @player.on_key_press("q")
        def on_quit():
            conn.send("quit".encode())
            self.quit()

        @player.on_key_press("s")
        def on_sync():
            payload = "sync: "+str(self.curr_time)
            conn.send(payload.encode())

        @player.on_key_press("space")
        def on_toggle():
            conn.send("toggle".encode())
            self.toggle()

        self.player.play(self.selected)
        self.player.wait_for_playback()


    def quit(self):
        self.player.quit()

    def toggle(self):
        self.player.cycle("pause")

    def selectMedia(self):
        files = os.listdir('.')
        for i in range(len(files)):
            print('['+str(i)+'] '+files[i])
        print("Enter the file number to select: ")

        return os.path.abspath(files[int(input())])


