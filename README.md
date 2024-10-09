# Instilled.AI Robot Server

This is a simple server that allows to you use the [instilled.ai teleoperation interface](https://demo.instilled.ai/host/) with your own robot(s).

## Setup
```
pip install -r requirements.txt
```

## Running

After cloning the repo to your local machine, run the server:
```
python server.py
```

On the same machine, visit [demo.instilled.ai/host/](https://demo.instilled.ai/host/) and select 'localhost' from the Robot dropdown.

This will load the robot description (urdf, yaml and meshes) hardcoded into `server.py` (by default: `robot_descriptions/marcel_plus_wx250s`). 

You can now click on the red, bottom left button on the website to move the left arm with your mouse along xyz. Right clicking will toggle between `{move left, rotate left, move right, rotate right}` modes. Esc will release your mouse.

To connect a VR headset to teleoperate using hand tracking:
1. for minimal latency, connect your VR headset and laptop to the same wifi network
2. visit [demo.instilled.ai/?connectionId=YOUR_SECRET_PASSWORD](https://demo.instilled.ai/) in your headset's browser, and change `YOUR_SECRET_PASSWORD` to something hard to guess.
3. visit [demo.instilled.ai/host/?connectionId=YOUR_SECRET_PASSWORD](https://demo.instilled.ai/host/) on your laptop and click `Connect VR Headset`.
4. wait a few seconds, then click `Enter VR` on your headset's browser.
5. feel free to move your VR headset to your forehead if, like me, you don't love passthrough quality yet. This way hand tracking should stay connected and you can see everything with your own eyes.


By default, the server will print the joint states every 1000ms. Replace this template code with your robot's python API to write the joint states to your robot at your desired frequency.

## Disclaimer

None of this is safe, you will probably break your robot or burn your house down. Use at your own peril.

Note: if anything doesn't work or stops working, refresh your laptop and VR browser pages, then connect again. Worst case, you might want to clear your browser cache (on chrome: `right click on page > inspect > right click on refresh button > Empty Cache and Hard Reload`).
