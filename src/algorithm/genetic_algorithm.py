from typing import List, Tuple, Callable
from melody import Note, Melody
import random, math
from util.selection import RouletteSelection


class GeneticAlgorithm:

    population: List[Melody]
    score_function: Callable[[Melody], float]
    threshold: float
    epoch: int

    good_music: List[Tuple[Melody, float]]

    def __init__(
        self,
        population: List[Melody],
        score_function: Callable[[Melody], float],
        threshold: float,
        mutation: float,
        epoch: int,
        *,
        early_stop: bool = False,
        debug: bool = False,
    ) -> None:
        """constructor.

        Parameters
        ----------
        `population` : `List[Melody]`
            initial population
        `score_function` : `Callable[[Melody], float]`
            score function
        `threshold` : `float`
            the threshold for a good music
        `epoch` : `int`
            max iterations
        `early_stop` : `bool`, optional
            if `True`, the algorithm will stop early if there is a melody good enough.
            By default False
        `debug` : `bool`, optional
            if `True`, additional debug info will be printed.
            By default False
        """
        self.population = population
        self.score_function = score_function
        self.threshold = threshold
        self.mutation = mutation
        self.epoch = epoch
        self.early_stop = early_stop
        self.debug = debug
        self.good_music = []

    def _update_score(self) -> None:
        self.score = [self.score_function(melody) for melody in self.population]
        for score, melody in zip(self.score, self.population):
            if score > self.threshold:
                self.good_music.append([melody, score])
            pass

    def _choose_random(self) -> Melody:
        selector = RouletteSelection(len(self.score))
        for score in self.score:
            selector.submit(math.exp(score) - 1)
        return self.population[selector.selected_index()]

    def _choose_best(self) -> Melody:
        best_id = 0
        for i in range(1, len(self.score)):
            if self.score[i] > self.score[best_id]:
                best_id = i
        return self.population[best_id]

    def evolve(self) -> None:
        for epoch in range(self.epoch):
            self._update_score()
            if self.debug:
                print(f"Epoch {epoch} start")
                print(self.score)
            if self.early_stop and len(self.good_music):
                return
            new_population = [self._choose_best()]
            for i in range(1, len(self.population)):
                child = Melody.cross(self._choose_random(), self._choose_random(),
                                     random.randint(0, 32))
                if random.random() < self.mutation:
                    child.mutate()
                new_population.append(child)
            self.population = new_population
            if self.debug:
                print(f"Epoch {epoch} end")
        self._update_score()
        if self.debug:
            print(self.score)
