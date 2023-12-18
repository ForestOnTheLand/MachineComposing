from melody import save_midi, play_midi, Melody, Note, Tonality, melodies
from algorithm import RandomGenerator, GeneticAlgorithm, operation as op, fitness as F
import random
from util import random_interval
import os, sys, time

little_star = Melody([
    8, 28, 8, 28, 15, 28, 15, 28, 17, 28, 17, 28, 15, 28, 28, 28, 13, 28, 13, 28, 12, 28, 12, 12,
    10, 28, 10, 28, 8, 28, 28, 28
])


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
    return (0.5 * F.interval_score(x) + 0.4 * F.rhythm_score(x) +
            0.6 * F.tonality_score(x, ["C major"]) - F.density_penalty(x) - F.stop_penalty(x) -
            F.rest_penalty(x) - F.consecutive_penalty(x, 7))


if __name__ == '__main__':
    generator = RandomGenerator(32)

    algorithm = GeneticAlgorithm(
        population=[generator() for _ in range(10)],  # Initial population
        mutation_rate=0.2,
        epoch=500,
        score_function=evaluator,
        mutate_function=mutator,
        cross_function=lambda x, y: op.two_points_cross(x, y, random_interval(32)),
        early_stop=False,
    )

    algorithm.evolve()
    melody = algorithm.choose_best()
    print(melody)
    print("{}, {}, {}".format(
        F.interval_score(melody),
        F.get_tonality(melody, ['C major']),
        F.rhythm_score(melody),
    ))
    save_midi(melody, './tmp.mid')
    play_midi('./tmp.mid')
