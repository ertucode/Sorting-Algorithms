from vars import *
import random
from enum import Enum

class Algo(Enum):
    no_algo = 1
    bubble = 2
    quick_right = 3
    quick_random = 4


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

        self.count = count

    def run(self):

        while self.running:

            self.check_events() 

            self.draw()
            if not self.sorted:
                if self.algo == Algo.bubble: self.bubble_sort()
                elif self.algo == Algo.quick_right or self.algo == Algo.quick_random: self._quick_sort()

                self.change_algo = False

            
    def create_random_list(self, count):
        self.current_list = random.sample(range(1, count + 1), count)
        rect_size = (WIDTH - 2 * X_PADDING) / count
        unit_height = SORT_MAX_HEIGHT / count


        self.rects = [pygame.Rect(( X_PADDING + i * rect_size, SORT_BOTTOM - r * unit_height, rect_size, r * unit_height )) for i, r in enumerate(self.current_list)]
        self.sorted = False

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
                    self.create_random_list(self.count)
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
                    case pygame.K_RIGHT:
                        self.FPS = min(self.FPS + 10, 500)
                    case pygame.K_LEFT:
                        self.FPS = max(self.FPS - 10, 1)
                    case pygame.K_UP:
                        self.FPS = min(self.FPS + 50, 500)
                    case pygame.K_DOWN:
                        self.FPS = max(self.FPS - 50, 1)
                    case pygame.K_RETURN:
                        self.change_algo = True
                        self.algo = Algo.no_algo
                        inp = input(f"[{2} - {WIDTH - 2 * X_PADDING}]: ")
                        try: 
                            inp = int(inp)
                            self.count = max(min(inp, WIDTH - 2 * X_PADDING), 2)
                            self.create_random_list(self.count)
                            return True
                        except ValueError: 
                            print("You didn't give a number") 
                    case pygame.K_SPACE:
                        self.change_algo = True
                        self.algo = Algo.no_algo
                        self.create_random_list(self.count)
                        return True
        

    def draw(self):

        self.clock.tick(FPS)

        if self.sorted: c = SORTED_COLOR
        else: c = IDLE_COLOR
        self.win.fill(BACKGROUND_COLOR)
        for r in self.rects:
            pygame.draw.rect(self.win, c, r)


        pygame.draw.rect(self.win, BACKGROUND_COLOR, (0, SORT_BOTTOM - 1, WIDTH, SORT_BOTTOM_PAD))

        pygame.display.update()


    def draw_rect(self, *rects):
        self.clock.tick(self.FPS)

        pygame.draw.rect(self.win, BACKGROUND_COLOR, (0, 0, WIDTH, SORT_TOP))
        fps_surface = my_font.render(f"FPS: {self.clock.get_fps():.0f} - {self.FPS}", True, "white")
        match self.algo:
            case Algo.quick_random:
                cur_alg = "Current algorithm: Quick Sort (random-pivot)"
            case Algo.quick_right:
                cur_alg = "Current algorithm: Quick Sort (right-pivot)"
            case Algo.bubble:
                cur_alg = "Current algorithm: Bubble Sort"

        algo_surface = my_font.render(cur_alg, True, "white")

        self.win.blit(fps_surface, FPS_TUPLE)
        self.win.blit(algo_surface, ALGO_TUPLE)

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