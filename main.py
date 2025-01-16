import tkinter as tk
from tkinter import filedialog
import random
import json
import os

# Константы
CELL_SIZE = 10  # Размер клетки
GRID_WIDTH = 80  # Ширина карты в клетках
GRID_HEIGHT = 60  # Высота карты в клетках
UPDATE_INTERVAL = 100  # Интервал обновления (мс)


class GameOfLife:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=GRID_WIDTH * CELL_SIZE, height=GRID_HEIGHT * CELL_SIZE, bg="white")
        self.canvas.pack()

        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

        self.running = False
        self.customizing = False
        self.painting = False
        self.painting_color = 1  # Цвет, который используется для рисования (1 - черный, 0 - белый)

        self.export_count = 0  # Для нумерации сохранённых полей

        # Добавление фрейма для кнопок
        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack()

        # Кнопки управления
        self.start_button = tk.Button(self.controls_frame, text="Start Again", command=self.start_again)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.exit_button = tk.Button(self.controls_frame, text="Exit", command=self.exit_game)
        self.exit_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.canvas.bind("<Button-1>", self.start_paint)
        self.canvas.bind("<B1-Motion>", self.paint_cell)
        self.canvas.bind("<ButtonRelease-1>", self.stop_paint)

        self.start_again()

    def start_again(self):
        self.running = False
        self.customizing = False
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

        # Очистка фрейма от кнопок, относящихся к предыдущей фазе
        self.clear_controls_frame()

        # Добавление кнопок для выбора режима генерации
        self.random_button = tk.Button(self.controls_frame, text="Random Generation", command=self.random_generation)
        self.random_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.custom_button = tk.Button(self.controls_frame, text="Custom Generation", command=self.custom_generation)
        self.custom_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.import_button = tk.Button(self.controls_frame, text="Import Field", command=self.import_field)
        self.import_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.update_canvas()

    def clear_controls_frame(self):
        for widget in self.controls_frame.winfo_children():
            if widget != self.start_button and widget != self.exit_button:
                widget.destroy()

    def random_generation(self):
        self.grid = [[random.choice([0, 1]) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.start_game_controls()
        self.update_canvas()

    def custom_generation(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.customizing = True
        self.start_game_controls()
        self.update_canvas()

    def start_game_controls(self):
        # Очистка фрейма от кнопок выбора генерации
        self.clear_controls_frame()

        # Добавление кнопок управления игрой
        self.continue_button = tk.Button(self.controls_frame, text="Continue", command=self.start_game)
        self.continue_button.pack(side=tk.LEFT, padx=5, pady=5)

    def start_paint(self, event):
        if not self.customizing:
            return
        self.painting = True
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            self.painting_color = 0 if self.grid[y][x] == 1 else 1
            self.toggle_cell(event)

    def toggle_cell(self, event):
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            self.grid[y][x] = self.painting_color
            self.update_canvas()

    def paint_cell(self, event):
        if not self.painting:
            return
        self.toggle_cell(event)

    def stop_paint(self, event):
        self.painting = False

    def start_game(self):
        self.running = True
        self.customizing = False

        # Убираем кнопки настройки и добавляем Pause
        self.clear_controls_frame()
        self.pause_button = tk.Button(self.controls_frame, text="Pause", command=self.toggle_pause)
        self.pause_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.update_grid()

    def toggle_pause(self):
        self.running = not self.running
        if self.running:
            self.pause_button.config(text="Pause")
            self.update_grid()
        else:
            self.pause_button.config(text="Play")
            self.add_export_button()

    def add_export_button(self):
        if not hasattr(self, "export_button") or not self.export_button:
            self.export_button = tk.Button(self.controls_frame, text="Export Field", command=self.export_field)
            self.export_button.pack(side=tk.LEFT, padx=5, pady=5)

    def export_field(self):
        self.export_count += 1
        filename = f"game_of_life_field_{self.export_count}.json"
        data = {
            "grid": self.grid,
            "grid_width": GRID_WIDTH,
            "grid_height": GRID_HEIGHT
        }
        with open(filename, "w") as f:
            json.dump(data, f)
        print(f"Field exported to {filename}")

    def import_field(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    if data["grid_width"] == GRID_WIDTH and data["grid_height"] == GRID_HEIGHT:
                        self.grid = data["grid"]
                        self.start_game_controls()
                        self.update_canvas()
                    else:
                        print("Field dimensions do not match current settings.")
            except (FileNotFoundError, KeyError, json.JSONDecodeError):
                print("Invalid field file.")

    def exit_game(self):
        self.root.destroy()

    def update_grid(self):
        if not self.running:
            return

        self.canvas.delete("all")
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] == 1:
                    x1 = x * CELL_SIZE
                    y1 = y * CELL_SIZE
                    x2 = x1 + CELL_SIZE
                    y2 = y1 + CELL_SIZE
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="white")

        self.grid = self.calculate_next_generation()
        self.root.after(UPDATE_INTERVAL, self.update_grid)

    def update_canvas(self):
        self.canvas.delete("all")
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] == 1:
                    x1 = x * CELL_SIZE
                    y1 = y * CELL_SIZE
                    x2 = x1 + CELL_SIZE
                    y2 = y1 + CELL_SIZE
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="white")

    def calculate_next_generation(self):
        new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                live_neighbors = self.count_live_neighbors(x, y)
                if self.grid[y][x] == 1:
                    if live_neighbors in [2, 3]:
                        new_grid[y][x] = 1
                elif live_neighbors == 3:
                    new_grid[y][x] = 1
        return new_grid

    def count_live_neighbors(self, x, y):
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                    count += self.grid[ny][nx]
        return count


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Game of Life")
    game = GameOfLife(root)
    root.mainloop()
