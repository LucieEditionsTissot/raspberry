from rpi_ws281x import PixelStrip, Color
import time
import math

class LedManager:
    def __init__(self, pin, number_of_leds):
        self.number_of_leds = number_of_leds
        self.strip = PixelStrip(number_of_leds, pin)
        self.strip.begin()
        self.isLit = False

    def set_pixel_color(self, index, color, intensity=1.0):
        if intensity > 1.0:
            intensity = 1.0
        if intensity < 0.0:
            intensity = 0.0
        r, g, b = color
        self.strip.setPixelColor(index, Color(int(r * intensity), int(g * intensity), int(b * intensity)))

    def set_strip_color(self, color, intensity=1.0):
        if intensity > 1.0:
            intensity = 1.0
        if intensity < 0.0:
            intensity = 0.0
        r, g, b = color
        for i in range(self.number_of_leds):
            print(r, g, b)
            self.strip.setPixelColor(i, Color(int(r * intensity), int(g * intensity), int(b * intensity)))
        self.strip.show()

    def light_up_gradually(self, color, intensity=0.5, delay=1):
        if intensity > 1.0:
            intensity = 1.0
        if intensity < 0.0:
            intensity = 0.0
        r, g, b = color
        for i in range(self.number_of_leds):
            self.strip.setPixelColor(i, Color(int(r * intensity), int(g * intensity), int(b * intensity)))
            self.strip.show()
            time.sleep(delay)

    def show(self):
        self.strip.show()


