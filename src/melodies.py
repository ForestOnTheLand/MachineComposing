from melody import Melody, save_midi, play_midi

"""
    有如下分类：
        音符频率：低 中 高
        情感：平静 欢乐 悲伤
"""

# 1. 欢乐颂选段 - 贝多芬 - C大调 中 平静
ode_an_die_freude = Melody(
    "E4 -  E4 -  F4 -  G4 -  "
    "G4 -  F4 -  E4 -  D4 -  "
    "C4 -  C4 -  D4 -  E4 - "
    "E4 -  -  D4 D4 -  -  - "
    "E4 -  E4 -  F4 -  G4 - "
    "G4 -  F4 -  E4 -  D4 - "
    "C4 -  C4 -  D4 -  E4 - "
    "D4 -  -  C4 C4 -  -  - "
    "- - - - - - - -".split())

# 2. 四季《春》第一乐章 - 维瓦尔第 - E大调 高 欢乐
seasons_spring_the_first = Melody(
    "C5 - #A4 A4 #A4 -  C5 - "
    "D5 - C5  -  -  -  F4 - "
    "C5 - #A4 A4 #A4 -  C5 - "
    "D5 - C5  -  -  -  F4 - "
    "D5 - C5  -  -  -  #A4 - "
    "-  - A4  -  G4 F4 G4 - "
    "- - - - - - - -".split()
)

# 3. d大调卡农 - 帕西贝尔 - D大调 中 平静
d_major_canon = Melody(
    "G5 -  E5 F5 G5 -  E5 F5 "
    "G5 G4 A4 B4 C5 D5 E5 F5 "
    "E5 -  C5 D5 E5 -  E4 F4 "
    "G4 A4 G4 F4 G4 E4 F4 G4 "
    "F4 -  A4 G4 F4 -  E4 D4 "
    "E4 D4 C4 D4 E4 F4 G4 A4 "
    "F4 -  A4 G4 A4 -  B4 C5 "
    "B4 A4 G4 A4 B4 C5 D5 E5 "
    "- - - - - - - -".split()
)

# 4. 十二平均律之c大调前奏曲 - 巴赫 - C大调 - 高 - 平静
twelve_tone_equal_temperament = Melody(
    "C4 E4 G4 C5 E5 G4 C5 E5 "
    "C4 E4 G4 C5 E5 G4 C5 E5 "
    "C4 E4 A4 D5 F5 A4 D5 F5 "
    "C4 E4 A4 D5 F5 A4 D5 F5 "
    "- - - - - - - -".split()
)

midi = seasons_spring_the_first
save_midi(midi, "./tmp.mid")
play_midi("./tmp.mid")
