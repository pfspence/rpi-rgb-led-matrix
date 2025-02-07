import os
import logging
import io
import time
from PIL import Image
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from rgbmatrix import graphics, RGBMatrixOptions, RGBMatrix
from dotenv import load_dotenv

load_dotenv()


path = os.path.dirname(__file__)
log = logging.getLogger(__name__)

schedule = BackgroundScheduler(daemon=True)
schedule.start()


class Weather:
    def __init__(self, canvas):
        self.framerate = 1
        self.canvas = canvas

        self.api_key = os.getenv("OPENWEATHERMAP_APIKEY")
        self.lat = os.getenv("LATITUDE")
        self.lon = os.getenv("LONGITUDE")
        self.refresh_minutes = 5

        self.temp = "--°F"
        self.icon_url = "https://openweathermap.org/img/wn/03d@2x.png"
        self.icon = requests.get(self.icon_url)

        schedule.add_job(self._get_weather_data)
        schedule.add_job(self._get_weather_data, "interval", minutes=self.refresh_minutes)

    def _get_weather_data(self):
        raw = None
        try:
            r = requests.get(
                f"https://api.openweathermap.org/data/3.0/onecall?lat={self.lat}&lon={self.lon}&exclude=hourly,daily&units=imperial&appid={self.api_key}",
                timeout=7,
            )
            raw = r.json()["current"]

            self.description = raw["weather"][0]["description"].upper()
            self.temp = str(round(raw["temp"])) + "°F"
            self.icon_url = (
                "http://openweathermap.org/img/wn/"
                + raw["weather"][0]["icon"]
                + "@2x.png"
            )
            self.icon = requests.get(self.icon_url, timeout=7)

            log.info(
                "_get_weather_data: Temp: %s, Icon URL: %s" % (self.temp, self.icon_url)
            )
        except:
            log.warning("_get_weather_data: exception occurred %s" % raw)

    def get_framerate(self):
        return self.framerate

    def show(self, matrix):
        self.canvas = matrix.SwapOnVSync(self.draw())

    def draw(self):
        self.canvas.Clear()
        font = graphics.Font()
        font.LoadFont(path + "/../../fonts/4x6.bdf")
        amber = graphics.Color(255, 155, 0)

        image = Image.open(io.BytesIO(self.icon.content))
        image.thumbnail((40, 40))
        icon = image.convert("RGB")
        self.canvas.SetImage(icon, 0, -8)

        temp_x_pos = 64 - 4 * len(self.temp)
        desc_x_pos = 64 - 4 * len(self.description)
        desc_x_pos = 0 if desc_x_pos < 0 else desc_x_pos

        graphics.DrawText(
            self.canvas,
            font,
            temp_x_pos,
            26,
            amber,
            self.temp,
        )
        graphics.DrawText(
            self.canvas,
            font,
            desc_x_pos,
            32,
            amber,
            self.description,
        )
        graphics.DrawText(
            self.canvas,
            font,
            59,
            6,
            amber,
            time.strftime("%H:%M").upper(),
        )

        return self.canvas


if __name__ == "__main__":

    options = RGBMatrixOptions()

    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.row_address_type = 0
    options.multiplexing = 0
    options.pwm_bits = 11
    options.brightness = 100
    options.pwm_lsb_nanoseconds = 130
    options.led_rgb_sequence = "RGB"
    options.pixel_mapper_config = ""
    options.panel_type = ""
    options.show_refresh_rate = 0
    options.gpio_slowdown = 4
    options.disable_hardware_pulsing = True
    options.drop_privileges = True

    matrix = RGBMatrix(options=options)

    canvas = matrix.CreateFrameCanvas()
    weather = Weather(canvas)
    time.sleep(5)
    weather.show(matrix)
    time.sleep(120)
