from vars import *
import random
from enum import Enum
import time

class Algo(Enum):
    no_algo = "No algo"
    bubble = "Current algorithm: Bubble Sort"
    quick_right = "Current algorithm: Quick Sort (right-pivot)"
    quick_random = "Current algorithm: Quick Sort (random-pivot)"
    radix = "Current algorithm: Radix Sort"
    merge = "Current algorithm: Merge Sort"


class Manager:
    def __init__(self, count):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sorting Algorithms")   
        self.running = True
        self.clock = pygame.time.Clock()
        self.list = self.create_random_list(count)
        self.sorted = False
        self.algo = Algo.no_algo
        self.change_algo = False

        self.FPS = FPS

        self.time_in_algo = 0

        self.data_count = count



    def run(self):

        while self.running:

            self.check_events() 

            self.draw()
            self.change_algo = False
            if not self.sorted:
                if self.algo == Algo.no_algo: self.time_in_algo = 0
                else:
                    self.start = time.time()
                    if self.algo == Algo.bubble: self.bubble_sort()
                    elif self.algo == Algo.quick_right or self.algo == Algo.quick_random: self._quick_sort()
                    elif self.algo == Algo.radix: self.radix_sort()
                    elif self.algo == Algo.merge: self._merge_sort()
                    self.time_spent = time.time() - self.start



            
    def create_random_list(self, count):
        self.current_list = random.sample(range(1, count + 1), count)
        self.rect_size = (WIDTH - 2 * X_PADDING) / count
        self.unit_height = SORT_MAX_HEIGHT / count


        self.rects = [pygame.Rect(( X_PADDING + i * self.rect_size, SORT_BOTTOM - r * self.unit_height, self.rect_size, r * self.unit_height )) for i, r in enumerate(self.current_list)]
        self.sorted = False

        self.count_surface = my_font.render(f"Data count: {count}", True, "white")

    def bubble_sort(self):
        n = len(self.current_list)
 
        for i in range(n):
            for j in range(0, n-i-1):
    
                if self.current_list[j] > self.current_list[j+1]:
                    self.current_list[j], self.current_list[j+1] = self.current_list[j+1], self.current_list[j]
                    self.rects[j].y, self.rects[j].h, self.rects[j+1].y, self.rects[j+1].h = self.rects[j+1].y, self.rects[j+1].h, self.rects[j].y, self.rects[j].h   

                if self.check_events(): return

                self.draw_rect((j, SORTING_COLOR1), (j+1, SORTING_COLOR2))
        
        self.sorted = True

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return True 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.algo = Algo.bubble
                    self.change_algo = True
                    return True
                elif event.key == pygame.K_2:
                    self.algo = Algo.quick_right
                    self.change_algo = True
                    return True
                elif event.key == pygame.K_SPACE:
                    self.change_algo = True
                    self.algo = Algo.no_algo
                    self.create_random_list(self.data_count)
                    return True

    def change_items(self, i1, i2):
        self.current_list[i1], self.current_list[i2] = self.current_list[i2], self.current_list[i1]
        self.rects[i2].y, self.rects[i2].h, self.rects[i1].y, self.rects[i1].h = self.rects[i1].y, self.rects[i1].h, self.rects[i2].y, self.rects[i2].h  

    def _quick_sort(self):

        def partition(low, high):
            i = (low-1)

            if self.algo == Algo.quick_random:
                r = random.randint(low, high)
                self.change_items(r, high)
                self.draw_rect((r, SORTING_COLOR1), (high, PIVOT_COLOR))

            pivot = self.current_list[high]
        
            for j in range(low, high):
                if self.current_list[j] <= pivot:
                    i = i+1
                    self.change_items(i, j)

                
                if self.check_events(): return

                self.draw_rect((min(pivot, len(self.current_list) - 1), PIVOT_COLOR), (j, SORTING_COLOR1), (i, SORTING_COLOR2))

            self.change_items(i+1, high)
            self.draw_rect((high, PIVOT_COLOR), (i+1, SORTING_COLOR1))
            return (i+1)

        def quick_sort(low, high):
            if not self.running or self.change_algo: return
            
            if low <= high:
                pi = partition(low, high)
                if not pi == None:
                    quick_sort(low, pi-1)
                    quick_sort(pi+1, high)

        quick_sort(0, len(self.current_list) -  1)

        if self.change_algo: return
        if self.running: self.sorted = True

    def radix_sort(self):
        max_num = max(self.current_list)
        digit_count = len("%i" % max_num)

        
        
        for i in range(digit_count):
            prev_list = self.current_list[:]
            prev_rects = self.rects[:]

            modulo = 10 ** i
            digits = [[] for _ in range(10)]
            digit_rects = [[] for _ in range(10)]


            for index, j in enumerate(self.current_list):
                digits[j // modulo % 10].append(j)

            index = 0
            for d, digit in enumerate(digits):
                for val in digit:
                    digit_rects[d].append(pygame.Rect( X_PADDING + index * self.rect_size, SORT_BOTTOM - val * self.unit_height, self.rect_size,val * self.unit_height ))
                    index += 1

            self.current_list = []
            self.rects = []
            length = 0
            for digit, digit_rect in zip(digits, digit_rects):
                self.current_list += digit
                self.rects += digit_rect

                for j in range(len(digit_rect)):
                    if self.check_events():
                        self.current_list = prev_list
                        self.rects = prev_rects
                        return
                        
                    self.draw_rect((length + j, SORTING_COLOR1))
                length = len(self.rects)

            self.current_list = [num for digit in digits for num in digit]

        self.sorted = True

    def _merge_sort(self):
        def merge(low, mid, high):
            if self.change_algo: return
            i1, i2 = low, mid + 1
            temp = []
            while i1 <= mid and i2 <= high:
                if self.current_list[i1] < self.current_list[i2]: 
                    temp.append(self.current_list[i1])
                    i1 += 1
                else: 
                    temp.append(self.current_list[i2])
                    i2 += 1

            if i1 > mid:
                temp.extend(self.current_list[i2:high+1])
            else: 
                temp.extend(self.current_list[i1:mid+1])
            
            for val in temp:
                self.current_list[low] = val
                self.rects[low] = pygame.Rect( X_PADDING + low * self.rect_size, SORT_BOTTOM - val * self.unit_height, self.rect_size,val * self.unit_height )
                self.draw_rect((low, SORTING_COLOR1))
                if self.check_events(): return
                low += 1


        def merge_sort(low, high):
            if self.change_algo: return
            mid = (high + low) // 2

            if low < high:
                merge_sort(low, mid)
                merge_sort(mid + 1, high)
                merge(low, mid, high)

        merge_sort(0, len(self.current_list) - 1)

        if not self.change_algo: self.sorted = True


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return True 

            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_1:
                        self.algo = Algo.bubble
                        self.change_algo = True
                        return True
                    case pygame.K_2:
                        self.algo = Algo.quick_right
                        self.change_algo = True
                        return True
                    case pygame.K_3:
                        self.algo = Algo.quick_random
                        self.change_algo = True
                        return True
                    case pygame.K_4:
                        self.algo = Algo.radix
                        self.change_algo = True
                        return True
                    case pygame.K_5:
                        self.algo = Algo.merge
                        self.change_algo = True
                        return True
                    case pygame.K_RIGHT:
                        self.FPS = min(self.FPS + 10, 500)
                    case pygame.K_LEFT:
                        self.FPS = max(self.FPS - 10, 1)
                    case pygame.K_UP:
                        self.FPS = min(self.FPS + 50, 500)
                    case pygame.K_DOWN:
                        self.FPS = max(self.FPS - 50, 1)
                    case pygame.K_c:
                        self.change_algo = True
                        self.algo = Algo.no_algo
                        
                        self.data_count = self.get_user_input("Data count", 2, WIDTH - 2 * X_PADDING, 4, self.data_count)
                        self.create_random_list(self.data_count)
                        return True
                    case pygame.K_f:
                        self.FPS = self.get_user_input("FPS", 1, 500, 3, self.FPS)
                    case pygame.K_SPACE:
                        self.change_algo = True
                        self.algo = Algo.no_algo
                        self.create_random_list(self.data_count)
                        return True
        

    def draw(self):

        self.clock.tick(FPS)
        self.win.fill(BACKGROUND_COLOR)

        pygame.draw.rect(self.win, BACKGROUND_COLOR, (0, 0, WIDTH, SORT_TOP))
        fps_surface = my_font.render(f"FPS: {self.clock.get_fps():.0f} - {self.FPS}", True, "white")

        self.win.blit(fps_surface, FPS_TUPLE)
        self.win.blit(self.count_surface, COUNT_TUPLE)

        if self.sorted:
            time_surface = my_font.render(f"Time spent: {self.time_spent:.2f}", True, "white")
            algo_surface = my_font.render(self.algo.value, True, "white")
            self.win.blit(time_surface, TIME_TUPLE)
            self.win.blit(algo_surface, ALGO_TUPLE)

        if self.sorted: c = SORTED_COLOR
        else: c = IDLE_COLOR
        for r in self.rects:
            pygame.draw.rect(self.win, c, r)


        pygame.draw.rect(self.win, BACKGROUND_COLOR, (0, SORT_BOTTOM - 1, WIDTH, SORT_BOTTOM_PAD))

        pygame.display.update()


    def draw_rect(self, *rects):

        self.clock.tick(self.FPS)

        pygame.draw.rect(self.win, BACKGROUND_COLOR, (0, 0, WIDTH, SORT_TOP))

        fps_surface = my_font.render(f"FPS: {self.clock.get_fps():.0f} - {self.FPS}", True, "white")
        algo_surface = my_font.render(self.algo.value, True, "white")
        time_surface = my_font.render(f"Time spent: {time.time()-self.start:.2f}", True, "white")

        self.win.blit(fps_surface, FPS_TUPLE)
        self.win.blit(algo_surface, ALGO_TUPLE)
        self.win.blit(self.count_surface, COUNT_TUPLE)
        self.win.blit(time_surface, TIME_TUPLE)

        for r, c  in rects:
            cur = self.rects[r]
            pygame.draw.rect(self.win, BACKGROUND_COLOR, (cur.x, SORT_TOP, cur.w, SORT_MAX_HEIGHT))
            pygame.draw.rect(self.win, c, cur)  

        pygame.draw.rect(self.win, BACKGROUND_COLOR, (0, SORT_BOTTOM - 1, WIDTH, SORT_BOTTOM_PAD))

        pygame.display.update()  

        for r, _ in rects:
                cur = self.rects[r]
                pygame.draw.rect(self.win, BACKGROUND_COLOR, (cur.x, SORT_TOP, cur.w, SORT_MAX_HEIGHT))
                pygame.draw.rect(self.win, IDLE_COLOR, cur) 

    def get_user_input(self, message, min_bound, max_bound, max_digit, default):
        entry = ""

        def draw_input_field(num):
            input_surface = my_font.render(f"{message} [{min_bound} - {max_bound}]: {num}", True, "white")
            pygame.draw.rect(self.win, BACKGROUND_COLOR, ENTRY_RECT)
            self.win.blit(input_surface, ENTRY_RECT)
            pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return True 

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        entry = entry[:-1]
                    elif event.key == pygame.K_RETURN:
                        return max(min(int(entry or default), max_bound), min_bound)
                        
                    try:
                        int(event.unicode) 
                        if len(entry) < max_digit: entry += event.unicode
                    except:
                        pass

            draw_input_field(entry)

                

            