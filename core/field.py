from random import choice
from copy import deepcopy
from math import log2
import pygame
from config import FREE_UNDOS, CELLS_R, ANIM_DELAY
from tkinter import filedialog as fd
from tkinter.messagebox import showerror


from .draw_utils import draw_cell

class GameField:
    MOVE_CONFIG = {
        'ne': {'vec': (1, 1, 0), 'axes': ('z', 'x'), 'reverse': True},
        'e': {'vec': (0, 1, -1), 'axes': ('x', 'y'), 'reverse': True},
        'se': {'vec': (-1, 0, -1), 'axes': ('y', 'z'), 'reverse': False},
        'sw': {'vec': (-1, -1, 0), 'axes': ('z', 'x'), 'reverse':False},
        'w': {'vec': (0, -1, 1), 'axes': ('x', 'y'), 'reverse': False},
        'nw': {'vec': (1, 0, 1), 'axes': ('y', 'z'), 'reverse': True},
    }

    def __init__(self, radius = CELLS_R, surface = None):
        # Защита от слишком больших и слишком маленьких значений
        radius = max(2, min(radius, 8))
        self.radius = radius
        self.cells = {}
        self.prev_state = None
        self.prev_score = 0
        self.surface = surface
        self.score = 0
        self.free_undos = FREE_UNDOS
        self.moves = 0

        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                z = x - y
                if abs(z) <= radius:
                    self.cells[(x, y, z)] = {
                        'value': 0,
                        'blocked': False,
                    }
        for i in range(1, 5):
            self.spawn_tile()

    def __int_to_bytes(self, value):
        buf = bytearray(4)
        for i in range(len(buf)):
            buf[i] = value % 256
            value //= 256
        return buf

    def __bytes_to_int(self, buf):
        result = 0
        for i in range(len(buf)):
            result += buf[i] * 256 ** i
        return result

    def can_move(self, x, y, z, direction):
        if direction not in self.MOVE_CONFIG:
            return False

        dx, dy, dz = self.MOVE_CONFIG[direction]['vec']
        x_new, y_new, z_new = x + dx, y + dy, z + dz

        # Проверяем, существует ли текущая  клетка
        if (x, y, z) not in self.cells:
            return False

        # Проверяем, существует ли целевая клетка
        if (x_new, y_new, z_new) not in self.cells:
            return False

        current = self.cells[(x, y, z)]
        target = self.cells[(x_new, y_new, z_new)]

        # Если в текущей ячейке ноль, нечего двигать
        if current['value'] == 0:
            return False

        # Если клетка заблокирована, никто никуда не идёт
        if target['blocked']:
            return False

        # На пустую клетку всегда можем перемещаться
        if target['value'] == 0:
            return True

        # Если такое же значение - можем двигаться, предстоит слияние
        if target['value'] == current['value']:
            return True

        # В остальных случаях не можем
        return False

    def global_move(self, direction):
        # Сохраняем состояние для возможной отмены хода во временную переменную
        tmp_state = deepcopy(self.cells)
        tmp_score = self.score
        merged = set()
        cfg = self.MOVE_CONFIG[direction]
        dx, dy, dz = cfg['vec']
        axis1, axis2 = cfg['axes']
        r = self.radius

        range1 = range(-r, r + 1)
        range2 = range(r, -r - 1, -1) if cfg['reverse'] else range(-r, r + 1)

        moved = True
        cycle = 0
        while moved:
            moved = False
            cycle += 1

            for val1 in range1:
                for val2 in range2:
                    if axis1 == 'x' and axis2 == 'y':
                        x, y = val1, val2
                        z = x - y
                    elif axis1 == 'y' and axis2 == 'z':
                        y, z = val1, val2
                        x = y + z
                    elif axis1 == 'z' and axis2 == 'x':
                        z, x = val1, val2
                        y = x - z
                    else:
                        continue

                    if abs(x) > r or abs(y) > r or abs(z) > r:
                        continue

                    if self.can_move(x, y, z, direction):
                        tx, ty, tz = x + dx, y + dy, z + dz
                        if self.cells[(tx, ty, tz)]['value'] == self.cells[(x, y, z)]['value']:
                            merged.add(self.cells[(tx, ty, tz)]['value'] + self.cells[(x, y, z)]['value'])
                        self.cells[(tx, ty, tz)]['value'] += self.cells[(x, y, z)]['value']
                        self.cells[(x, y, z)]['value'] = 0
                        moved = True

            if self.surface is not None:
                for index in self.cells.keys():
                    draw_cell(self.surface, index[0], index[1], self.cells[index]['value'])
                pygame.display.flip()
                pygame.time.wait(max(100, min(int(ANIM_DELAY), 1000)))

        # Если первый проход по массиву "пустой" (ничего не перемещалось), cycle будет равно 1, иначе больше.
        # Создаём новое значение только в том случае, если было перемещение хоть одной цифры
        # И сохраняем состояние для отмены только если были перемещения
        if cycle > 1:
            self.spawn_tile()
            self.prev_state = deepcopy(tmp_state)
            self.prev_score = tmp_score
            self.score += 1
            for n in merged:
                self.score += int(log2(n))
            self.moves += 1

        tmp_state = None
        tmp_score = 0

        return True

    def spawn_tile(self):
        keys = list(self.cells.keys())
        empty_indices = [i for i in range(len(keys)) if self.cells[keys[i]]['value'] == 0]

        if not empty_indices:
            return False

        idx = choice(empty_indices)
        self.cells[keys[idx]]['value'] = choice([2] * 9 + [4])
        return True

    def undo_last_move(self):
        if self.prev_state is not None:
            # Есть "бесплатные" отмены
            if self.free_undos > 0:
                self.free_undos -= 1
            # Счёт достаточный для отмены
            elif self.prev_score >= 50:
                self.prev_score -= 50
            # Иначе просто выходим
            else:
                return False
            # Восстанавливаем состояние игры и счёт
            self.cells = deepcopy(self.prev_state)
            self.score = self.prev_score
            self.moves -= 1
            # Обнуляем предыдущее состояние, отмена теперь не имеет смысла
            self.prev_state = None
            self.prev_score = 0
        return True

    def save_to_file(self):
        arr_len = len(self.cells) * 3 + 14
        ba = bytearray(arr_len)
        ba[0:4] = bytes('2048', 'utf-8')
        ba[4] = self.radius
        cnt = 0
        for coords, item in self.cells.items():
            ba[cnt * 3 + 5] = (coords[0] + 256) % 256
            ba[cnt * 3 + 6] = (coords[1] + 256) % 256
            ba[cnt * 3 + 7] = 255 if item['blocked'] else int(log2(item['value'])) if item['value'] > 0 else 0
            cnt += 1
        ba[-9] = self.free_undos
        ba[-8:-4] = self.__int_to_bytes(self.score)
        ba[-4:] = self.__int_to_bytes(self.moves)
        for i in range(5, len(ba)):
            ba[i] = ba[i] ^ ((i + 75) % 256)
        gamefile = fd.asksaveasfilename(
            defaultextension='.2048',
            filetypes=[('Hexagon 2048', '.2048'), ('All files', '*')],
            title='Save Game Field as...',
        )

        if gamefile is not None:
            try:
                with open(gamefile, 'wb') as f:
                    f.write(ba)
            except Exception as e:
                print(f"Error saving file: {e}")

    def open_from_file(self):
        gamefile = fd.askopenfilename(
            defaultextension='.2048',
            filetypes=[('Hexagon 2048', '.2048'), ('All files', '*')],
            title='Open Game Field...',
        )

        if gamefile is not None:
            try:
                with open(gamefile, 'rb') as f:
                    ba = bytearray(f.read())
                    for i in range(5, len(ba)):
                        ba[i] = ba[i] ^ ((i + 75) % 256)
                    corrupted = False
                    # Header
                    if ba[:4].decode('utf-8') != '2048':
                        corrupted = True
                    # File size
                    cells_count = 3 * (ba[4] ** 2 + ba[4]) + 1
                    if cells_count * 3 + 14 != len(ba):
                        corrupted = True
                    # Free undos
                    if ba[-9] > FREE_UNDOS:
                        corrupted = True
                    # Coordinates
                    for i in range(cells_count):
                        x = ba[i * 3 + 5]
                        if x > 127:
                            x -= 256
                        y = ba[i * 3 + 6]
                        if y > 127:
                            y -= 256
                        z = x - y
                        if max(abs(x), abs(y), abs(z)) > ba[4]:
                            corrupted = True

                    if corrupted:
                        showerror('Corrupted File', 'Game file is corrupted. Cannot load it.')
                    else:
                        self.cells = {}
                        self.score = self.__bytes_to_int(ba[-8:-4])
                        self.moves = self.__bytes_to_int(ba[-4:])
                        self.free_undos = ba[-9]
                        for i in range(cells_count):
                            x = ba[i * 3 + 5]
                            if x > 127:
                                x -= 256
                            y = ba[i * 3 + 6]
                            if y > 127:
                                y -= 256
                            z = x - y
                            self.cells[(x, y, z)] = {'value': 0, 'blocked': False}
                            if ba[i * 3 + 7] == 255:
                                self.cells[(x, y, z)]['blocked'] = True
                            elif ba[i * 3 + 7] > 0:
                                self.cells[(x, y, z)]['value'] = 2 ** ba[i * 3 + 7]

            except Exception as e:
                print(f"Error opening file: {e}")
