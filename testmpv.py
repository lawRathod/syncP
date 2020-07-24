import mpv

def my_log(loglevel, component, message):
    print('[{}] {}: {}'.format(loglevel, component, message))

# player = mpv.MPV(log_handler=my_log, ytdl=True, input_default_bindings=True, input_vo_keyboard=True)
player = mpv.MPV(ytdl=True, input_default_bindings=True, input_vo_keyboard=True)

player.play('./media/vid.mkv')
player.wait_for_playback()


