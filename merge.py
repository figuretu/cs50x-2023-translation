import deepl

# 原始的每一条字幕作为cell
class cell:
    def __init__(self, index, time, content):
        self.index = index
        self.time = time
        self.content = content

    def __str__(self):
        return self.index + '\n' + self.time + '\n' + self.content + '\n'

    def __repr__(self):
        return self.__str__()

# 打开srt字幕文件
with open('original - CS50x 2023 - Lecture 0 - Scratch.srt') as f:
    # 读取文件内容
    content = f.read()

    # 以换行符分割字符串
    content = content.split('\n')
    # print(len(content))

    count = 0
    # 步进为4，每4个元素为一组，分别为index, time, content, ''
    for i in range(0, len(content), 4):
        # 将每一组元素作为一个cell对象
        now_cell = cell(content[i], content[i+1], content[i+2])
        print(now_cell)
        count += 1
        if count == 5:
            break
