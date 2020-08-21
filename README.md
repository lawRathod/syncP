# syncP

A tool to sync mpv player between host and clients. Great help from [jaseg/python-mpv](https://github.com/jaseg/python-mpv), please check it out.

## How to use

### Requirements
- libmpv_32bit
- python3

### Steps

Install the wheel package manually by downloading it from [releases](https://github.com/lawRathod/syncP/releases/download/v0.1-alpha/syncP_lawRathod-0.0.1-py3-none-any.whl) or using **pip install -i syncP**.

[For Windows]
- You will need to download the libmpv zip from [Official Mpv Project](https://sourceforge.net/projects/mpv-player-windows/files/libmpv/), please use the lastest 32 bit version of libmpv.
- After extracting to a folder, add the path of the folder in your system path variable.
- To test if the path is set right, execute **syncp test** and check if the test video plays, you can press **q** to exit.
- Assuming the test works, you can now either host a connection or join, I have explained the step below.

[For Linux]
- Install mpv for you distribution and then try executing **syncp test** in your terminal.
- Assuming the test works, you can now either host a connection or join, I have explained the step below.

### Using the tool
[For Host]
- Navigate to the directory with your media file you wanna sync and run **syncp host**. Follow the instructions on the terminal and this will open a port on your system for communication.
- You will need to port forward using [ngrok](https://ngrok.com/) or config your router, I would suggest use [ngrok](https://ngrok.com/) tcp feature for this purpose.

[For Client]
- Nagigate to the directory with your media file you wanna sync and run **syncp client**. Follow the instructions where it will ask you for the host url and port.
- Upon entering the details you can choose the media.

If everything went well you will be connected and the media will begin to play in your own respective mpv windows. 

### Keybindings
Not all events are synced, for now you can use **space** to sync pause and play and the host can use **s** to sync the location of the mediaplayback. I would suggest you better pause before syncing the location. No on screen controls are avaible for now. Default mpv keybindings work and you can find them [here](https://defkey.com/mpv-media-player-shortcuts). 

#### Disclaimer
This project is in no way perfect and could have multiple bugs I will try to fix along with adding some more features. For now it just works and my gf and I enjoy watching movies together. 😁
