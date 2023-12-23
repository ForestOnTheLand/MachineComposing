from melody import save_midi, play_midi, Melody, Note, Tonality, melodies
from algorithm import RandomGenerator, GeneticAlgorithm, operation as op, fitness as F
import random
from util import random_interval
import matplotlib.pyplot as plt
import os, sys, time

# Fixed random seed
random.seed(3407)  # Some magic number here!


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
    return (0.8 * F.interval_score(x) + 0.4 * F.rhythm_score(x) +
            0.6 * F.tonality_score(x, 'C major') + 0.2 * F.stable_score(x) +
            0.6 * F.boundary_score(x) - F.density_penalty(x) - F.stop_penalty(x) -
            F.rest_penalty(x) - F.consecutive_penalty(x, 7) - F.range_penalty(x, 18) -
            F.variety_penalty(x, 5) - F.lonely_penalty(x))


if __name__ == '__main__':
    generator = RandomGenerator(32)

    algorithm = GeneticAlgorithm(
        population=[generator() for _ in range(10)],  # Initial population
        mutation_rate=0.2,
        epoch=1000,
        score_function=evaluator,
        mutate_function=mutator,
        cross_function=lambda x, y: op.two_points_cross(x, y, random_interval(32)),
        early_stop=False,
        record=True,
    )

    algorithm.evolve()
    melody = algorithm.choose_best()
    print(melody)
    print("Total score: {:.2f}".format(evaluator(melody)))
    print(
        "Scores interval:{:.2f}, tonality:{}, rhythm:{:.2f}, stable:{:.2f}, boundary:{:.2f}".format(
            F.interval_score(melody),
            F.get_tonality(melody, 'C major'),
            F.rhythm_score(melody),
            F.stable_score(melody),
            F.boundary_score(melody),
        ))
    save_midi(melody, './tmp.mid')
    play_midi('./tmp.mid')
