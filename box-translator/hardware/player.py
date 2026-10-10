import subprocess

DEVICE = "plughw:CARD=Headphones,DEV=0"


def play(path):
    subprocess.run(["aplay", "-D", DEVICE, path], check=True)
