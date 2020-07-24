import mpv
import os


class player:
    def __init__(self):
        self.player = mpv.MPV(ytdl=True, input_default_bindings=True, input_vo_keyboard=True)
        self.selected = "media/"+self.selectMedia()

    def start(self, conn):
        player = self.player
        @player.on_key_press("q")
        def on_quit():
            conn.send("quit".encode())
            self.quit()

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
        files = os.listdir('media/')
        for i in range(len(files)):
            print('['+str(i)+'] '+files[i])
        print("Enter the file number to select: ")

        return files[int(input())]


