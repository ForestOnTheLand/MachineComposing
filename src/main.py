from melody import save_midi, play_midi, Melody, Note, Tonality
from algorithm import RandomGenerator, GeneticAlgorithm
import algorithm.operation as op
import algorithm.fitness as F
import random, os, sys, time
from util import random_interval

little_star = Melody([
    8, 28, 8, 28, 15, 28, 15, 28, 17, 28, 17, 28, 15, 28, 28, 28, 13, 28, 13, 28, 12, 28, 12, 12,
    10, 28, 10, 28, 8, 28, 28, 28
])


def mutate(melody: Melody) -> None:
    value = random.random()
    if value < 0.4:
        op.one_point_mutate(melody, random.randint(0, 31))
    elif value < 0.6:
        op.transpose(melody, indices=random_interval(len(melody)))
    elif value < 0.8:
        op.inverse(melody, indices=random_interval(len(melody)))
    else:
        op.retrograde(melody, indices=random_interval(len(melody)))


def evaluator(x: Melody) -> float:
    return (0.4 * F.interval_score(x) + 0.6 * F.rhythm_score(x) +
            0.6 * F.tonality_score(x, "minor") - F.density_penalty(x) - F.stop_penalty(x))


if __name__ == '__main__':
    generator = RandomGenerator(32)
    algorithm = GeneticAlgorithm(
        [generator() for _ in range(10)],
        # [Melody(little_star) for _ in range(10)],
        threshold=0.99,
        mutation_rate=0.1,
        epoch=500,
        score_function=evaluator,
        mutate_function=mutate,
        cross_function=lambda x, y: op.two_points_cross(x, y, random_interval(32)),
        early_stop=False,
        debug=False,
    )
    algorithm.evolve()
    melody = algorithm.choose_best()
    print(melody)
    print(
        f"{F.interval_score(melody)}, {F.rhythm_score(melody)}, {F.tonality_score(melody, 'major')}"
    )
    save_midi(melody, './tmp.mid', instrument=0)
    play_midi('./tmp.mid')
