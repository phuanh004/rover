from picamera import PiCamera
from time import sleep


class Camera:
    def __init__(self) -> None:
        self.camera = PiCamera()

    def setup_default_settings(self) -> None:
        self.camera.resolution = (2592, 1944)
        self.camera.zoom = (0.25, 0.25, 0.5, 0.5)
        self.camera.framerate = 15
        self.camera.brightness = 50

    def capture(self, path: str, name: str) -> None:
        self.camera.capture(path + name + '.jpg')

    def close(self) -> None:
        self.camera.close()
