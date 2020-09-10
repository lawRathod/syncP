import os
from syncP import mpv

# Player class uses mpv backend to listen for events and control the main player 
class player:

    # Intantiate player object 
    # Params: None
    def __init__(self):
        self.player = mpv.MPV(ytdl=True, input_default_bindings=True, input_vo_keyboard=True, osc=True)
        self.selected = self.selectMedia()
        os.system('cls' if os.name == 'nt' else 'clear')
        self.conns = None

    # Method to start the player, config the keybinding for events and send message using the socket connection to host/clients
    # Params: connection list, payload is the timestamp received from host everytime a client is joined
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
        print("\n\n####################\n")
        print("Keyboard shortcuts~\n", "<space>    -toggle play/pause","s    -sync all clients (only host)" ,"q    -quit", sep="\n")
        print("\n\n###################\n\n")
        self.player.play(self.selected)
        self.pause()
        if payload != None:
            while self.player.time_pos == None:
                continue
            self.player.seek(payload[6:],reference="absolute")
        self.player.wait_for_playback()


    # Sync method to sync all the clients to same time as host in the video
    def sync(self):
        cur = self.conns.head
        payload = "sync: "+str(self.player.time_pos)
        while cur:
            cur.conn.send(payload.encode())
            cur = cur.next

    # Quit method to quit the player and close mpv core
    def quit(self):
        self.player.quit()

    # Toggle methos to cycle between play and pause 
    def toggle(self):
        self.player.cycle("pause")

    #pause method is called upon new connections joined or old connections closed
    def pause(self):
        self.player.command("set","pause", "yes")

    # Method to select the media file path from files in current directory
    def selectMedia(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        files = os.listdir('.')
        print("List of files in this directory:\n\n")
        for i in range(len(files)):
            print('['+str(i)+'] '+files[i])
        print("\n\nEnter the file number to select: ")

        return os.path.abspath(files[int(input())])


