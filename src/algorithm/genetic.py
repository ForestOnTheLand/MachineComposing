import sys
from typing import List, Tuple, Callable, Sequence
from melody import Note, Melody
import random, math
from util.selection import RouletteSelection
from .operation import one_point_cross


class GeneticAlgorithm:

    # Functions
    score_function: Callable[[Melody], float]
    mutate_function: Callable[[Melody], None]
    cross_function: Callable[[Melody, Melody], Melody]

    # Music
    population: List[Melody]
    good_music: List[Tuple[Melody, float]]

    # Hyper-parameters
    threshold: float
    mutation_rate: float
    epoch: int

    # Options
    early_stop: bool

    # True when there is a good music and self.early_stop
    _end: bool

    def __init__(
        self,
        population: Sequence[Melody | Sequence[int | str | Note]],
        mutation_rate: float,
        epoch: int,
        score_function: Callable[[Melody], float],
        mutate_function: Callable[[Melody], None],
        cross_function: Callable[[Melody, Melody], Melody],
        *,
        early_stop: bool = False,
        threshold: float = 0.0,
        length: None | int = None,
    ) -> None:
        """
        constructor of Genetic Algorithm.
        
        Parameters
        ----------
        `population` : `List[Melody]`
            Initial population.
        `threshold` : `float`
            The threshold for good music.
        `mutation_rate` : `float`
            Mutation probability.
        `epoch` : `int`
            Number of iterations.
        `score_function` : `Callable[[Melody], float]`
            Score function.
            See module `algorithm.fitness` for more information.
        `mutate_function` : `Callable[[Melody], None]`
            Mutate function.
            See module `algorithm.operation` for more information.
        `cross_function` : `Callable[[Melody, Melody], Melody]`
            Cross function.
            See module `algorithm.operation` for more information.
        `early_stop` : `bool`, optional
            If True, the algorithm will stop immediately when a good music is found.
            By default `False`.
        """
        if not isinstance(population, Sequence):
            raise ValueError(f"Expected population: Sequence, given {type(population)}")
        if not population:
            raise ValueError(f"Empty population")

        if length is None:
            self.population = [Melody(m) for m in population]
            if any(len(melody) != len(self.population[0]) for melody in self.population):
                raise ValueError(f"Inconsistent length for melodies in population, "
                                 f"given length {[len(m) for m in self.population]}")
        else:
            self.population = [Melody(m).pad_or_cut_to(length) for m in population]

        self.score_function = lambda x: max(0, score_function(x))
        self.mutate_function = mutate_function
        self.cross_function = cross_function
        self.threshold = threshold
        self.mutation_rate = mutation_rate
        self.epoch = epoch
        self.early_stop = early_stop
        self._end = False

    def _update_score(self) -> None:
        self.score = [self.score_function(melody) for melody in self.population]
        self._end = self.early_stop and any(score > self.threshold for score in self.score)

    def choose_random(self) -> Melody:
        selector = RouletteSelection(len(self.score))
        for score in self.score:
            selector.submit(score)
        return self.population[selector.selected_index()]

    def choose_best(self) -> Melody:
        best_id = 0
        for i in range(1, len(self.score)):
            if self.score[i] > self.score[best_id]:
                best_id = i
        return self.population[best_id]

    def evolve(self) -> None:
        for epoch in range(self.epoch):
            self._update_score()
            if self._end:
                return
            new_population = [self.choose_best()]
            for i in range(1, len(self.population)):
                child = self.cross_function(self.choose_random(), self.choose_random())
                if random.random() < self.mutation_rate:
                    self.mutate_function(child)
                new_population.append(child)
            self.population = new_population
        self._update_score()
