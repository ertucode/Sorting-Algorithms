import pygame


class AlgorithmHandler:
    def __init__(self):
        self.algorithms = { "none": "No algorithm",
                            "bubble": "Current algorithm: Bubble Sort",
                            "quick_right" : "Current algorithm: Quick Sort (right-pivot)",
                            "quick_random" : "Current algorithm: Quick Sort (random-pivot)",
                            "radix" : "Current algorithm: Radix Sort",
                            "merge" : "Current algorithm: Merge Sort",
                            "insertion" : "Current algorithm: Insertion Sort",
                            "selection" : "Current algorithm: Selection Sort"
                            }

        self.algo = "none"

        self.algorithm_keys = {pygame.K_1: "bubble",
                               pygame.K_2: "quick_right",
                               pygame.K_3: "quick_random",
                               pygame.K_4: "radix",
                               pygame.K_5: "merge",
                               pygame.K_6: "insertion",
                               pygame.K_7: "selection",
        }


    def handle_key(self, key):

        if key in self.algorithm_keys:
            self.algo = self.algorithm_keys[key]
            return True