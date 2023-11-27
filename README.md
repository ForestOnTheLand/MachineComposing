# 音乐与数学 大作业

## `Python`环境配置

本项目需要`mido`库与`pygame`库的安装。环境配置如下：

```ps
conda create -n music python=3.10
conda activate music
pip install mido
pip install pygame
```

## 文件结构

其他文件/文件夹功能如下：

- `./resource`: 内含多个`.pdf`文件，均是与本项目相关的内容，可做参考文献。**强烈建议**将有用的文章加入其中！
- `./src`: 代码位置。会在代码结构一节详细说明
- `./.gitignore`: `git`提交时忽略什么文件
- `./README.md`: 本文件

## 代码结构

在`./src`目录下，各文件/文件夹功能如下：

- `./src/algorithm`: 遗传算法所在文件夹。

    ```py
    from algorithm import RandomGenerator, GeneticAlgorithm, operation, fitness
    ```

  - `./src/algorithm/fitness.py`: 适应度函数。**推荐增加内容**。
  - `./src/algorithm/operation.py`: 交叉、变异函数。**推荐增加内容**。
  - `./src/algorithm/initial.py`: 初始种群生成。现在只有随机生成初始种群，未来有需要可以增加从`.json`文件导入。
  - `./src/algorithm/genetic_algorithm.py`: 遗传算法框架。

- `./src/melody`: 主要工作是实现`midi`文件的保存，播放与`Note`, `Melody`类。

    ```py
    from melody import Note, Melody, save_midi, play_midi
    ```

- `./src/util`: 一些小工具，但与代码框架无关。必要时可以自行增加，并在此处简要描述。小工具罗列如下：
  - `RouletteSelection`类：轮盘赌算法。

## 注意事项

1. 组员编写函数需要在函数前加上自己的名字。（不加就默认是组长写的了）
2. 尽量不要大幅改动框架，或删除已有函数（除非必要）。
3. 遇到`bug`或有新的提议（关于新功能、对框架的意见），可以直接在群里交流。
4. 命名最好看到函数就知道什么意思，特别之处要加注释。

## 待办事项

可以根据下面的描述找一点任务做：

- （必做）增加移调、倒影、逆行函数：加入文件`./src/algorithm/operation.py`中即可，效果可以自行验证。可以在`./src/melody/music.py`中找到注释部分，作为参考（注释部分代码实现可能有一些问题）。
- （选做）找一些音乐片段，写成数组的形式（具体见`./src/melody/music.py`中`Note.id`的描述）。之后也许会增加导入的方式。
- （长期）增加变异函数：加入文件`./src/algorithm/operation.py`中即可，效果可以自行验证。
- （长期）增加适应度函数：加入文件`./src/algorithm/fitness.py`中即可，效果可以自行验证。
