'''
重新编号srt文件
'''

import os
from cell import *

cells = load_cells('srt_zh/CS50x 2023 - Lecture 0 - Scratch_zh.srt')

# 编号从1开始
for i, cell in enumerate(cells):
    cell.index = str(i + 1)

save_cells(cells, 'srt_zh/CS50x 2023 - Lecture 0 - Scratch_zh.srt')
