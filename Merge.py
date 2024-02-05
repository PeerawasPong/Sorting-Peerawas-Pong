from pyglet.window import Window
from pyglet.app import run
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch
from pyglet import clock
import random

class Renderer(Window):
    def __init__(self):
        super().__init__(width=1000, height=600, caption="Merge sort")
        self.batch = Batch()
        self.bar_width = 4   # ความกว้าง Bars
        self.spacing = 2     # ระยะห่างระหว่าง Bars
        self.bars = []
        self.num_bars = 100  # จำนวน Bars
        self.bar_color = (135, 206, 235)  # สี Bars

        # สร้างความสูงแบบสุ่ม
        self.heights = [random.randint(10, 500) for _ in range(self.num_bars)]
        self.create_bars()

        self.sorting_generator = self.merge_sort(self.heights, 0, len(self.heights) - 1)

    def create_bars(self):
        # ล้าง Bars ที่มีอยู่
        self.bars.clear()

        # คำนวณตำแหน่งเริ่มต้น Bars
        x = self.spacing
        for height in self.heights:
            bar = Rectangle(x, 0, self.bar_width, height, batch=self.batch, color=self.bar_color)
            self.bars.append(bar)
            x += self.bar_width + self.spacing

    def merge_sort(self, arr, start, end):
        if start < end:
            mid = (start + end) // 2
            yield from self.merge_sort(arr, start, mid)
            yield from self.merge_sort(arr, mid + 1, end)
            yield from self.merge(arr, start, mid, end)

    def merge(self, arr, start, mid, end):
        merged = []
        left_idx = start
        right_idx = mid + 1

        while left_idx <= mid and right_idx <= end:
            if arr[left_idx] < arr[right_idx]:
                merged.append(arr[left_idx])
                left_idx += 1
            else:
                merged.append(arr[right_idx])
                right_idx += 1

        while left_idx <= mid:
            merged.append(arr[left_idx])
            left_idx += 1

        while right_idx <= end:
            merged.append(arr[right_idx])
            right_idx += 1

        for i, val in enumerate(merged):
            arr[start + i] = val
            yield arr

    def on_update(self, dt):
        try:
            next(self.sorting_generator)
            self.create_bars()
        except StopIteration:
            clock.unschedule(self.on_update)

    def on_draw(self):
        self.clear()
        self.batch.draw()

if __name__ == "__main__":
    renderer = Renderer()
    clock.schedule_interval(renderer.on_update, 1 / 20.0)  # 20 เฟรม
    run()