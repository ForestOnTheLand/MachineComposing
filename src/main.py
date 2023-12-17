from melody import save_midi, play_midi, Melody, Note, Tonality
from algorithm import RandomGenerator, GeneticAlgorithm
import algorithm.operation as op
import algorithm.fitness as F
import random
from util import random_interval
import os, sys, time
import melodies

little_star = Melody([
    8, 28, 8, 28, 15, 28, 15, 28, 17, 28, 17, 28, 15, 28, 28, 28, 13, 28, 13, 28, 12, 28, 12, 12,
    10, 28, 10, 28, 8, 28, 28, 28
])

# B flat major
note_list = [
    "0", "#F3", "G3", "A3", "B3", "#C4", "D4", "E4", "#F4", "G4", "A4", "B4", "#C5", "D5", "E5",
    "#F5", "G5", "-"
]


def mutator(melody: Melody) -> None:
    value = random.random()
    if value < 0.4:
        op.one_point_mutate(melody)
    elif value < 0.6:
        op.transpose(melody)
    elif value < 0.8:
        op.inverse(melody)
    else:
        op.retrograde(melody)


def evaluator(x: Melody) -> float:
    return (0.4 * F.interval_score(x) + 0.2 * F.rhythm_score(x) +
            0.6 * F.tonality_score(x, "major") - F.density_penalty(x) - F.stop_penalty(x))


if __name__ == '__main__':
    print(len(melodies.d_major_canon))
    generator = RandomGenerator(32, note_list[:-1])
    algorithm = GeneticAlgorithm(
        [melodies.d_major_canon for _ in range(10)],
        threshold=0.99,
        mutation_rate=0.1,
        epoch=500,
        score_function=evaluator,
        mutate_function=mutator,
        cross_function=lambda x, y: op.two_points_cross(x, y, random_interval(32)),
        early_stop=False,
    )
    # for melody in algorithm.population:
    #     print(melody)
    algorithm.evolve()
    melody = algorithm.choose_best()
    print(melody)
    print(f"{F.interval_score(melody)}, {F.variety_score(melody)}, {F.rhythm_score(melody)}")
    save_midi(melody, './tmp.mid')
    play_midi('./tmp.mid')
