from melody import save_midi, play_midi, Melody, Note
from algorithm import RandomGenerator, interval_score, GeneticAlgorithm, variety_score

little_star = Melody([
    8, 28, 8, 28, 15, 28, 15, 28, 17, 28, 17, 28, 15, 28, 28, 28, 13, 28, 13, 28, 12, 28, 12, 12,
    10, 28, 10, 28, 8, 28, 28, 28
])

if __name__ == '__main__':
    generator = RandomGenerator(32)
    algorithm = GeneticAlgorithm(
        [generator() for _ in range(10)],
        lambda x: interval_score(x),
        threshold=0.99,
        mutation=0.1,
        epoch=100,
        early_stop=True,
        debug=True,
    )
    algorithm.evolve()
    melody = algorithm._choose_best()
    save_midi(melody, './tmp.mid')
    play_midi('./tmp.mid')
