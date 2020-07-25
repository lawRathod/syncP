import mpv
def my_log(loglevel, component, message):
    print('[{}] {}: {}'.format(loglevel, component, message))

def run():
   # player = mpv.MPV(log_handler=my_log, ytdl=True, input_default_bindings=True, input_vo_keyboard=True)
    player = mpv.MPV(ytdl=True, input_default_bindings=True, input_vo_keyboard=True)
    curr_time = None
    @player.property_observer('time-pos')
    def time_observer(_name, value):
        # Here, _value is either None if nothing is playing or a float containing
        # fractional seconds since the beginning of the file.
        global curr_time
        curr_time = value
    @player.on_key_press("s")
    def seekSync():
        global curr_time
        print(curr_time)
        player.seek("00:21",reference="absolute")
    player.play('./media/vid.mkv')
    player.wait_for_playback()
