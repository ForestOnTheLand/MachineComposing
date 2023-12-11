from melody import save_midi, play_midi, Melody, Note, Tonality
from algorithm import RandomGenerator, GeneticAlgorithm, operation, fitness
import random
from util import random_interval
import os, sys, time

little_star = Melody([
    8, 28, 8, 28, 15, 28, 15, 28, 17, 28, 17, 28, 15, 28, 28, 28, 13, 28, 13, 28, 12, 28, 12, 12,
    10, 28, 10, 28, 8, 28, 28, 28
])

# B flat major
note_list = [
    "0", "#F3", "G3", "A3", "B3", "#C4", "D4", "E4", "#F4", "G4", "A4", "B4", "#C5", "D5", "E5",
    "#F5", "G5", "-"
]


def mutate(melody: Melody) -> None:
    value = random.random()
    if value < 0.4:
        operation.one_point_mutate(melody, random.randint(0, 31))
    elif value < 0.6:
        operation.transpose(melody, indices=random_interval(len(melody)))
    elif value < 0.8:
        operation.inverse(melody, indices=random_interval(len(melody)))
    else:
        operation.retrograde(melody, indices=random_interval(len(melody)))


if __name__ == '__main__':
    generator = RandomGenerator(32, note_list[:-1])
    algorithm = GeneticAlgorithm(
        [generator() for _ in range(10)],
        threshold=0.99,
        mutation_rate=0.1,
        epoch=100,
        score_function=lambda x: fitness.interval_score(x) + max(
            fitness.rhythm_score(x) * 2 - 1, 0),
        mutate_function=mutate,
        cross_function=lambda x, y: operation.two_points_cross(x, y, random_interval(32)),
        early_stop=False,
        debug=True,
    )
    for melody in algorithm.population:
        print(melody)
    algorithm.evolve()
    melody = algorithm.choose_best()
    print(melody)
    print(
        f"{fitness.interval_score(melody)}, {fitness.variety_score(melody)}, {fitness.rhythm_score(melody)}"
    )
    save_midi(melody, './tmp.mid')
    play_midi('./tmp.mid')
