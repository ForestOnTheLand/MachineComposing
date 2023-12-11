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

# 2. 四季《春》第一乐章 - 维瓦尔第 - E大调 中 欢乐
seasons_spring_the_first = Melody(
    "C5 - #A4 A4 #A4 -  C5 - "
    "D5 - C5  -  -  -  F4 - "
    "C5 - #A4 A4 #A4 -  C5 - "
    "D5 - C5  -  -  -  F4 - "
    "D5 - C5  -  -  -  #A4 - "
    "-  - A4  -  G4 F4 G4 - "
    "- - - - - - - -".split()
)

# 3. d大调卡农 - 帕西贝尔 - D大调 高 平静
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

# 5. 巡逻兵进行曲 - 弗兰克·米查姆 - bE大调 - 高 - 欢乐
american_patrol = Melody(
    "#D4 - #D4 - #D4 D4 #D4 F4 "
    "G4 - G4 - G4 #F4 G4 #G4 "
    "#A4 - #A4 - #A4 A4 #A4 #D5 "
    "#A4 - - - - - - - ".split()
)

# 6. 拉德斯基进行曲 - 老约翰·施特劳斯 - C大调 - 高 - 欢乐
radetzky_march = Melody(
    "C5 0 C5 B4 C5 0 C5 B4 "
    "C5 0 B4 0 A4 0 C5 B4 "
    "C5 0 C5 B4 C5 0 C5 B4 "
    "C5 0 G5 0 F5 0 ".split()
)

# 7. 天鹅湖第二幕开场 - 柴可夫斯基 - C大调（已转） - 低 - 悲伤
ewan_lake_second = Melody(
    "E5 - - - - - - - "
    "A4 - B4 - C5 - D5 - "
    "E5 - - - C5 - E5 - "
    "- - C5 - E5 - - - "
    "A4 - C5 - A4 - E4 - "
    "C5 - A4 - - - - -".split()
)

# 8. 月光 - 贝多芬
seasons_spring_the_first_II = Melody(
    "".split()
)

# 9. night theme - PVZ - C大调（有点升降音） - 悲伤
night_theme_PVZ = Melody(
    "C5 -  A4 - - - B4 - "
    "A4 - E4 - F4 - F4 - "
    "E4 - A4 - #D4 E4 #G4 - "
    "A4 - - - - - - -".split()
)

# 10. 格兰瓦尔 - 塔雷加 - C大调 - 平静
gran_vals = Melody(
    "G5 F5 A4 - B4 - E5 D5 "
    "F4 - G4 - D5 C5 E4 - "
    "G4 - C5 - - - - -".split()
)

midi = gran_vals
save_midi(midi, "./tmp.mid")
play_midi("./tmp.mid")
