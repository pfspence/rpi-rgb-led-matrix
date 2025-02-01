#!/usr/bin/env python
# Display a runtext with double-buffering.
import random
from samples.samplebase import SampleBase
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time


class StockList:
    FONT_WIDTH = 4
    FONT_HEIGHT = 6
    def __init__(self, *args, **kwargs):
        options = RGBMatrixOptions()

        # options.hardware_mapping = "adafruit-hat-pwm"
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
        options.disable_hardware_pulsing = False
        options.drop_privileges = True

        self.matrix = RGBMatrix(options=options)

    def get_tickers(self):
        with open('tickers.txt', 'r') as f:
            tickers = f.read().splitlines()
        return tickers

    def get_change(self, ticker: str, interval: str = "day") -> float:
        return round(random.uniform(-20.0, 20.0), 1)

    def get_ticker_changes(self, interval: str = "day") -> dict[str, float]:
        tickers = self.get_tickers()
        ticker_changes: dict[str, float] = {}
        for ticker in tickers:
            ticker_changes[ticker] = self.get_change(ticker, interval)
        return ticker_changes

    def run(self):
        canvas = self.matrix.CreateFrameCanvas()

        font = graphics.Font()
        font.LoadFont(f"../../fonts/{StockList.FONT_WIDTH}x{StockList.FONT_HEIGHT}.bdf")

        while True:
            canvas.Clear()
            ticker_changes = self.get_ticker_changes("day")
            y_pos = StockList.FONT_HEIGHT
            x_pos = 0
            for ticker, change in ticker_changes.items():

                text_color = graphics.Color(155, 255, 0) if change > 0 else graphics.Color(255, 0, 0)
                change = abs(change)
                if change < 1:
                    change = "." + str(change)[-1]  # 0.1 -> .1
                else:
                    change = str(int(round(change)))  # 12.1 -> 12, 1.5 -> 1, 1.51 -> 2
                graphics.DrawText(canvas, font, x_pos, y_pos, text_color, f"{ticker} {change}")

                if x_pos == 0:
                    x_pos = 32
                elif x_pos == 32:
                    x_pos = 0
                    y_pos += StockList.FONT_HEIGHT

            canvas = self.matrix.SwapOnVSync(canvas)
            time.sleep(5)

# Main function
if __name__ == "__main__":
    stock_list = StockList()
    stock_list.run()
