#!/usr/bin/env python
# Display a runtext with double-buffering.
import random
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import yfinance as yf
import time


class StockList:
    FONT_WIDTH = 4
    FONT_HEIGHT = 6
    def __init__(self, *args, **kwargs):
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
        options.disable_hardware_pulsing = False
        options.drop_privileges = True

        self.matrix = RGBMatrix(options=options)

    def get_tickers(self):
        with open('tickers.txt', 'r') as f:
            tickers = f.read().splitlines()
        return tickers

    def get_change(self, ticker: str, interval: str = "day") -> float:
        return round(random.uniform(-20.0, 20.0), 1)

    def get_ticker_data(self) -> list[tuple[str, tuple[int, int, int]]]:

        lines = []
        for ticker in self.get_tickers():
            if " as " in ticker:
                ticker, display_ticker = ticker.split(" as ")
            else:
                display_ticker = ticker

            fast_info = yf.Ticker(ticker).fast_info
            day_open = fast_info.open
            last_price = fast_info.last_price
            display_last_price = round(last_price)

            day_change = round((last_price / day_open - 1) * 100, 1)
            color = (0, 255, 0) if day_change > 0 else (255, 0, 0)
            day_change = abs(day_change)
            if day_change > 9.9:
                day_change = round(day_change)

            display_ticker = display_ticker.ljust(5)
            display_last_price = f"${str(display_last_price)}".rjust(6)
            display_change = f"{str(day_change)}%".rjust(5)

            lines.append((f"{display_ticker}{display_last_price}{display_change}", color))  # tuple of text and color
            time.sleep(1)

        print(lines)
        return lines


    def run(self):
        canvas = self.matrix.CreateFrameCanvas()

        font = graphics.Font()
        font.LoadFont(f"../../fonts/{StockList.FONT_WIDTH}x{StockList.FONT_HEIGHT}.bdf")

        while True:
            canvas.Clear()
            lines = self.get_ticker_data()
            y_pos = StockList.FONT_HEIGHT
            x_pos = 0

            batch_size = 5  # we can only display 5 lines at a time
            for i in range(0, len(lines), batch_size):
                batch = lines[i:i + batch_size]
                for line, text_color in batch:
                    graphics.DrawText(canvas, font, x_pos, y_pos, text_color, line)
                    y_pos += StockList.FONT_HEIGHT

                canvas = self.matrix.SwapOnVSync(canvas)
                time.sleep(60)  # wait 60 seconds after displaying each batch
                y_pos = StockList.FONT_HEIGHT  # reset y position for the next batch
                canvas.Clear()

# Main function
if __name__ == "__main__":
    stock_list = StockList()
    stock_list.run()
