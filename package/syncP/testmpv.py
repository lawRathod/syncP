from syncP import mpv
import inspect
import os

def my_log(loglevel, component, message):
    print('[{}] {}: {}'.format(loglevel, component, message))

def run():
   # player = mpv.MPV(log_handler=my_log, ytdl=True, input_default_bindings=True, input_vo_keyboard=True)
    player = mpv.MPV(ytdl=True, osc=True,input_default_bindings=True, input_vo_keyboard=True)
    path = inspect.getfile(mpv)[:-7]
    print(path)
    player.play(os.path.join(path, "media/vid.mp4"))
    print("\n\n mpv works press q to exit\n\n")
    player.wait_for_playback()

if __name__=="__main__":
    run()
