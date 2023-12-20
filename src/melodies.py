from melody import Melody, save_midi, play_midi
"""
    有如下分类：
        音符频率：低 中 高
        情感：平静 欢乐 悲伤
"""

# 1. 欢乐颂选段 - 贝多芬 - C大调 中 平静
ode_an_die_freude = Melody("E4 -  E4 -  F4 -  G4 -  "
                           "G4 -  F4 -  E4 -  D4 -  "
                           "C4 -  C4 -  D4 -  E4 - "
                           "E4 -  -  D4 D4 -  -  - "
                           "E4 -  E4 -  F4 -  G4 - "
                           "G4 -  F4 -  E4 -  D4 - "
                           "C4 -  C4 -  D4 -  E4 - "
                           "D4 -  -  C4 C4 -  -  - "
                           "- - - - - - - -".split())

# 2. 四季《春》第一乐章 - 维瓦尔第 - E大调 中 欢乐
seasons_spring_the_first = Melody("C5 - #A4 A4 #A4 -  C5 - "
                                  "D5 - C5  -  -  -  F4 - "
                                  "C5 - #A4 A4 #A4 -  C5 - "
                                  "D5 - C5  -  -  -  F4 - "
                                  "D5 - C5  -  -  -  #A4 - "
                                  "-  - A4  -  G4 F4 G4 - "
                                  "- - - - - - - -".split())

# 3. d大调卡农 - 帕西贝尔 - D大调 高 平静
d_major_canon = Melody("G5 -  E5 F5 G5 -  E5 F5 "
                       "G5 G4 A4 B4 C5 D5 E5 F5 "
                       "E5 -  C5 D5 E5 -  E4 F4 "
                       "G4 A4 G4 F4 G4 E4 F4 G4 "
                       "F4 -  A4 G4 F4 -  E4 D4 "
                       "E4 D4 C4 D4 E4 F4 G4 A4 "
                       "F4 -  A4 G4 A4 -  B4 C5 "
                       "B4 A4 G4 A4 B4 C5 D5 E5 "
                       "- - - - - - - -".split())

# 4. 十二平均律之c大调前奏曲 - 巴赫 - C大调 - 高 - 平静
twelve_tone_equal_temperament = Melody("C4 E4 G4 C5 E5 G4 C5 E5 "
                                       "C4 E4 G4 C5 E5 G4 C5 E5 "
                                       "C4 E4 A4 D5 F5 A4 D5 F5 "
                                       "C4 E4 A4 D5 F5 A4 D5 F5 "
                                       "- - - - - - - -".split())

# 5. 巡逻兵进行曲 - 弗兰克·米查姆 - bE大调 - 高 - 欢乐
american_patrol = Melody("#D4 - #D4 - #D4 D4 #D4 F4 "
                         "G4 - G4 - G4 #F4 G4 #G4 "
                         "#A4 - #A4 - #A4 A4 #A4 #D5 "
                         "#A4 - - - - - - - ".split())

# 6. 拉德斯基进行曲 - 老约翰·施特劳斯 - C大调 - 高 - 欢乐
radetzky_march = Melody("C5 0 C5 B4 C5 0 C5 B4 "
                        "C5 0 B4 0 A4 0 C5 B4 "
                        "C5 0 C5 B4 C5 0 C5 B4 "
                        "C5 0 G5 0 F5 0 ".split())

# 7. 天鹅湖第二幕开场 - 柴可夫斯基 - C大调（已转） - 低 - 悲伤
ewan_lake_second = Melody("E5 - - - - - - - "
                          "A4 - B4 - C5 - D5 - "
                          "E5 - - - C5 - E5 - "
                          "- - C5 - E5 - - - "
                          "A4 - C5 - A4 - E4 - "
                          "C5 - A4 - - - - -".split())

# 8. 生日快乐歌 - C大调 - 中 - 欢乐
happy_birthday = Melody("G4 G4 A4 - G4 - C5 - "
                        "B4 - - - G4 G4 A4 - "
                        "G4 - D5 - C5 - - - "
                        "G4 G4 G5 - E5 - C5 - "
                        "B4 - A4 - F5 F5 E5 - "
                        "C5 - D5 - C5 - - - ".split())

# 9. night theme - PVZ - C大调（有点升降音） - 悲伤
night_theme_PVZ = Melody("C5 -  A4 - - - B4 - "
                         "A4 - E4 - F4 - F4 - "
                         "E4 - A4 - #D4 E4 #G4 - "
                         "A4 - - - - - - -".split())

# 10. 格兰瓦尔 - 塔雷加 - C大调 - 中 - 平静
gran_vals = Melody("G5 F5 A4 - B4 - E5 D5 "
                   "F4 - G4 - D5 C5 E4 - "
                   "G4 - C5 - - - - -".split())

# 11. 妈妈你听我说 - 德彪西 - C大调 - 中 - 平静
little_star = Melody(
    "C4 - C4 - G4 - G4 - "
    "A4 - A4 - G4 - - - "
    "F4 - F4 - E4 - E4 - "
    "D4 - D4 - C4 - - -".split()
)

# 12.  subconscious - maki - C大调 - 少 - 悲伤
subconscious = Melody(
    "A4 - - - E5 - D5 - "
    "C5 - B4 - A4 - - - "
    "- E5 D5 - C5 - B4 - "
    "A4 - - - E5 - D5 - "
    "C5 - B4 - A4 - - - "
    "- E5 D5 - C5 - B4 - "
    "A4 - - - - - - -".split()
)

# 13. geodash theme - GEODASH - C大调 - 高 - 欢乐
geodash_theme = Melody(
    "C4 G4 C4 G4 C4 G4 C4 G4 "
    "G3 D4 G3 D4 G3 D4 G3 D4 "
    "A3 E4 A3 E4 A3 E4 A3 E4 "
    "F3 C4 F3 C4 F3 C4 F3 C4 "
    "- - - -".split()
)

# 14. surfing down - unknown - C大调 - 高 - 欢乐
surfing_down = Melody(
    "G4 - G4 - G4 F4 E4 F4 "
    "G4 - A4 G4 - D4 - - "
    "C4 - C4 - C4 B3 C4 D4 "
    "E4 - F4 E4 - B3 - - "
    "A3 - A4 - G4 F4 E4 F4 "
    "G4 - - C4 C4 - - B3 "
    "A3 - B3 C4 D4 C4 B3 - "
    "C4 - - - - - - -".split()
)

# 15. undertale - Toby Fox - C大调 - 中 - 平静
undertale = Melody(
    "C4 - G4 - F4 - C4 - "
    "E4 - - E4 - - F4 - "
    "0 0 C4 - F4 - C4 - "
    "E4 - - E4 - - F4 - "
    "C4 - G4 - F4 - C4 - "
    "E4 - - E4 - - F4 - "
    "0 0 C4 - F4 - A4 - "
    "G4 - - F4 - - G4 - ".split()
)

# 16. snowy town - Toby Fox - C大调 - 中 - 平静
snowy_town = Melody(
    "G4 - G4 - G4 - G4 - "
    "F4 - E4 - F4 - G4 - "
    "- - C5 - - G4 - - "
    "- - - - - 0 0 0 "
    "G4 - G4 - G4 - G4 - "
    "F4 - E4 - F4 - G4 - "
    "D4 - B3 - C4 - - - "
    "- - - - - 0 0 0 ".split()
)

# 17. 菊次郎的夏天 - C大调 - 中 - 欢乐
summer = Melody(
    "G4 C5 D5 E5 D5 - C5 C5 "
    "- - - - 0 0 0 0 "
    "G4 C5 D5 E5 D5 - C5 D5 "
    "- - E5 - E5 - - - "
    "G4 C5 D5 E5 D5 - C5 C5 "
    "- - - - 0 0 0 0 "
    "G4 C5 D5 E5 D5 - C5 D5 "
    "- - G5 - E5 - - - ".split()
)

# 18. 梦中的婚礼 - C大调 - 高 - 平静
dreaming_wedding = Melody(
    "A4 A4 B4 B4 C5 C5 B4 B4 "
    "A4 A4 E4 E4 C4 C4 A3 A3 "
    "G4 G4 F4 F4 E4 F4 G4 F4 "
    "- - F4 F4 G4 G4 A4 A4 "
    "B4 B4 G4 G4 D4 D4 F4 F4 "
    "E4 E4 D4 E4 F4 E4 - - ".split()
)

# 19. 起风了前奏 - C大调 - 高 - 平静
wind_blowing = Melody(
    "B4 C5 D5 E5 - G4 G5 E5 "
    "- - - - 0 0 0 0 "
    "B4 C5 D5 E5 - G4 G5 E5 "
    "D5 E5 C5 D5 B4 C5 G4 - ".split()
)

# 20. 两只老虎 - C大调 - 中 - 欢乐
two_tigers = Melody(
    "C4 - D4 - E4 - C4 - "
    "C4 - D4 - E4 - C4 - "
    "E4 - F4 - G4 - - - "
    "E4 - F4 - G4 - - - "
    "G4 A4 G4 F4 E4 - C4 - "
    "G4 A4 G4 F4 E4 - C4 - "
    "D4 - G3 - C4 - - - "
    "D4 - G3 - C4 - - -".split()
)

# 21. 贝加尔胡畔 - C大调 - 中 - 悲伤
lake_bank = Melody(
    "0 0 A3 B3 C4 - G4 - "
    "F4 - - - - - - - "
    "0 0 G3 A3 B3 - F4 - "
    "E4 - - - - - - - "
    "0 0 E4 E4 A4 - G4 - "
    "F4 - D4 - - - D4 C4 "
    "B3 - E4 D4 - - C4 - "
    "A3 - - - - - - - ".split()
)

# 22. 圣诞快乐，劳伦斯先生 - C大调 - 中 - 悲伤
merry_christmas_mr_lawrence = Melody(
    "D4 E4 D4 A3 D4 - - - "
    "0 0 D4 E4 D4 E4 G4 E4 "
    "D4 E4 D4 A3 C4 - - - "
    "0 0 C5 - B4 G4 E4 - ".split()
)

# 23. river flows in you - C大调 - 中 - 悲伤
river_flows_in_you = Melody(
    "C5 - B4 C5 - C4 B4 C5 "
    "- C4 G4 C5 - C4 F4 C4 "
    "E4 - F4 - G4 - E4 - "
    "D4 - - - - - C4 B3 "
    "C4 - - - - G3 C4 D4 "
    "E4 - - - - - E4 F4 "
    "G4 - - - - - F4 E4 "
    "D4 - - - - - - -".split()
)

# 24. 漠河舞厅 - C大调 - 中 - 悲伤
desert_river_hall = Melody(
    "G4 - G4 - G4 - A4 B4 "
    "0 0 E4 - E4 - B4 - "
    "D5 - C5 - C5 - B4 C5 "
    "0 0 C5 - C5 - C5 - "
    "D5 - G4 - D5 - G4 D5 "
    "0 0 D5 - D5 - F5 - "
    "F5 - E5 - E5 - D5 E5 "
    "- - - - 0 0 0 0".split()
)

# 25. 富士山下前奏 - C大调 - 中 - 平静
under_Fuji = Melody(
    "C5 B4 A4 G4 A4 G4 E4 D4 "
    "E4 D4 C4 B3 C4 B3 A3 G3 "
    "A3 - B3 C4 D4 - E4 G4 "
    "G4 - E4 - - - - -".split()
)

if __name__ == '__main__':
    midi = american_patrol
    save_midi(midi, "./tmp.mid")
    play_midi("./tmp.mid")
