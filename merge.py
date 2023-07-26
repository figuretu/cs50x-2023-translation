'''
youtube的英文翻译大多断句非常短，不利于翻译以及理解。
这个脚本用来把srt字幕中的短句合成完整的句子，具体策略为：

0. 字幕文件的格式为srt，字幕内容为单独一行
1. 如果本条字幕与后面一条字幕同属于一句话，且合并后长度不超过200个字符，则合并

'''

import deepl
from constants import DEEPL_API_KEY

INPUT_FILE = 'test.srt'

translator = deepl.Translator(DEEPL_API_KEY)
MAX_CONTENT_LENGTH = 200 # 每条字幕最长字符，超过即使同属一句也不合并

# 原始的每一条字幕作为cell
class cell:
    # deepl的tranlator, 所有cell共用

    def __init__(self, index, time, content):
        self.index = index
        self.time = time
        self.content = content # 需要保证只有单行

    def get_content_length(self):
        # 获取字幕长度
        return len(self.content)

    def get_begin_time(self):
        # 获取开始时间
        return self.time.split(' --> ')[0]
    
    def set_begin_time(self, time):
        # 设置开始时间
        self.time = time + ' --> ' + self.get_end_time()

    def get_end_time(self):
        # 获取结束时间
        return self.time.split(' --> ')[1]
    
    def set_end_time(self, time):
        # 设置结束时间
        self.time = self.get_begin_time() + ' --> ' + time

    def merge(self, cell):
        # 与下一条cell合并
        self.content += ' ' + cell.content
        self.set_end_time(cell.get_end_time())

    def is_begin(self):
        # 不是以小写字符开头就是句首
        return not self.content[0].islower()
        
    def __str__(self):
        return self.index + '\n' + self.time + '\n' + self.content + '\n'

def merge(cells) -> list:
    # 根据策略合并cell组成完整的句子
    # 策略为：如果下一条字幕以大写字母或者特殊字符开头，则本条字幕为完整句子
    output_cells = []

    index = 0
    while index < len(cells):
        # 确定句首
        base_cell = cells[i]
        i = i + 1
        while i < len(cells) and not cells[i].is_begin() and base_cell.get_content_length() + cells[i].get_content_length() <= MAX_CONTENT_LENGTH:
            # 如果下一条字幕不是句首，且合并后长度不超过最大长度，则合并
            base_cell.merge(cells[i])
            i = i + 1
        output_cells.append(base_cell)

    # 设置index
    for i, cell in enumerate(output_cells):
        cell.index = str(i + 1)
            
    return output_cells


if __name__ == '__main__':
    content = []
    # 打开srt字幕文件
    with open(INPUT_FILE) as f:
        # 读取文件内容
        content = f.read()

    # 以换行符分割字符串
    content = content.split('\n')
    # print(len(content))

    # 每4个元素为一组，分别为index, time, content, '', 组成cell
    cells = []
    for i in range(0, len(content), 4):
        # 将每一组元素作为一个cell对象
        cells.append(cell(content[i], content[i+1], content[i+2]))

    output_cells = merge(cells)

    # 输出到文件
    with open(INPUT_FILE[:-4] + '-output.srt', 'w') as f:
        for cell in output_cells:
            f.write(cell.index + '\n' + cell.time + '\n' + cell.content + '\n\n')
