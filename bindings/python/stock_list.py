#!/usr/bin/env python
# Display a runtext with double-buffering.
import random
from samples.samplebase import SampleBase
from rgbmatrix import graphics
import time


class StockList(SampleBase):
    FONT_WIDTH = 4
    FONT_HEIGHT = 6

    def __init__(self, *args, **kwargs):
        super(StockList, self).__init__(*args, **kwargs)

    def get_tickers(self):
        with open('tickers.txt', 'r') as f:
            tickers = f.read().splitlines()
        return tickers

    def get_day_change(self, ticker: str, interval: str) -> float:
        return round(random.uniform(-2.0, 2.0), 1)

    def get_ticker_changes(self, interval: str):
        tickers = self.get_tickers()
        ticker_changes: dict[str, float] = {}
        for ticker in tickers:
            ticker_changes[ticker] = self.get_day_change(ticker)
        return ticker_changes

    def run(self):
        canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont(f"../../../fonts/{StockList.FONT_WIDTH}x{StockList.FONT_WIDTH}.bdf")

        ticker_changes = self.get_ticker_changes("day")

        y_pos = 0
        for ticker, change in ticker_changes.items():
            print(f"{ticker}: {change}")
            text_color = graphics.Color(155, 255, 0) if change > 0 else graphics.Color(255, 0, 0)
            graphics.DrawText(canvas, font, 0, y_pos, text_color, f"{ticker} {change}")
            y_pos += StockList.FONT_HEIGHT

# Main function
if __name__ == "__main__":
    stock_list = StockList()
    if (not stock_list.process()):
        stock_list.print_help()
