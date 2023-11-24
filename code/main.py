from util import save_midi, play_midi

little_star = [
    8, 28, 8, 28, 15, 28, 15, 28, 17, 28, 17, 28, 15, 28, 28, 28, 13, 28, 13, 28, 12, 28, 12, 12,
    10, 28, 10, 28, 8, 28, 28, 28
]

if __name__ == '__main__':
    save_midi(little_star, './new.mid')
    play_midi('./new.mid')
