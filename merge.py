'''
youtube的英文翻译大多断句非常短,不利于翻译以及理解。
这个脚本用来把srt字幕中的短句合成完整的句子,具体策略为:

0. 字幕文件的格式为srt,字幕内容为单独一行
1. 如果本条字幕与后面一条字幕同属于一句话,且合并后长度不超过200个字符,则合并

'''


from cell import *

INPUT_FILE = 'test.srt'
MAX_CONTENT_LENGTH = 200 # 每条字幕最长字符，超过即使同属一句也不合并

def merge(cells) -> list:
    # 根据策略合并cell组成完整的句子
    # 策略为：如果下一条字幕以大写字母或者特殊字符开头，则本条字幕为完整句子
    ret_cells = []

    i = 0
    while i < len(cells):
        # 确定句首
        base_cell = cells[i]
        i = i + 1
        while i < len(cells) and not cells[i].is_begin() and base_cell.get_content_length() + cells[i].get_content_length() <= MAX_CONTENT_LENGTH:
            # 如果下一条字幕不是句首，且合并后长度不超过最大长度，则合并
            base_cell.merge(cells[i])
            i = i + 1
        ret_cells.append(base_cell)

    # 设置index
    for i, cell in enumerate(ret_cells):
        cell.index = str(i + 1)
            
    return ret_cells


if __name__ == '__main__':
    cells = load_cells(INPUT_FILE)
    output_cells = merge(cells)

    # 输出到文件
    with open(INPUT_FILE[:-4] + '-output.srt', 'w') as f:
        for cell in output_cells:
            f.write(str(cell) + '\n')
