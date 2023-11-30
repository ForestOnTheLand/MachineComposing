from melody import save_midi, play_midi, Melody, Note
from algorithm import RandomGenerator, GeneticAlgorithm, operation, fitness
import random

little_star = Melody([
    8, 28, 8, 28, 15, 28, 15, 28, 17, 28, 17, 28, 15, 28, 28, 28, 13, 28, 13, 28, 12, 28, 12, 12,
    10, 28, 10, 28, 8, 28, 28, 28
])

# B flat major
NAME_LIST = [
    " ", "F3", "G3", "A3", "#A3", "C4", "D4", "#D4", "F4", "G4", "A4", "#A4", "C5", "D5", "#D5",
    "F5", "G5", "-"
]

if __name__ == '__main__':
    generator = RandomGenerator(32, NAME_LIST)
    algorithm = GeneticAlgorithm(
        [generator() for _ in range(10)],
        threshold=0.99,
        mutation_rate=0.1,
        epoch=100,
        score_function=lambda x: fitness.interval_score(x),
        mutate_function=lambda x: operation.one_point_mutate(x, random.randint(0, 31)),
        cross_function=lambda x, y: operation.one_point_cross(x, y, random.randint(0, 32)),
        early_stop=False,
        debug=True,
    )
    algorithm.evolve()
    melody = algorithm.choose_best()
    save_midi(melody, './tmp.mid')
    play_midi('./tmp.mid')
