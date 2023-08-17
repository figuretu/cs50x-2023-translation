'''
调用deepl翻译API
使用多线程加快速度

策略：
* 不用翻译的内容：
- 十个字符以内的
- AUDIENCE: [INAUDIBLE]
- 以[开头,并且]结尾

* 翻译字幕放在英文字幕的后面
在aegishub中, 按照时间排序可以让中英对应排布

'''

import deepl
import threading
from cell import *
from constants import DEEPL_API_KEY

INPUT_FILE = 'srt_en/CS50x 2023 - Lab 1 Walkthrough_output.srt'
THREADS_NUM = 20

translator = deepl.Translator(DEEPL_API_KEY)

def translate_cell(cell) -> cell:
    ret_cell = cell.copy()
    # 翻译
    ret_cell.content = str(translator.translate_text(cell.content, source_lang=deepl.Language.ENGLISH, target_lang=deepl.Language.CHINESE))
    return ret_cell

def translate_cells(cells: list, num_threads: int) -> list:
    # 翻译cells
    ret_cells = []
    lock = threading.Lock()
    threads = []

    def translate_task(start, step):
        for i in range(start, len(cells), step):
            cell = cells[i]
            # 添加策略
            if cell.content.startswith('[') and cell.content.endswith(']'):
                continue
            if cell.get_content_length() <= 10:
                continue
            if cell.content.startswith('AUDIENCE: [INAUDIBLE]'):
                continue
            translated_cell = translate_cell(cell)
            with lock:
                ret_cells.append(translated_cell)

    # 创建并启动多个线程
    for i in range(num_threads):
        thread = threading.Thread(target=translate_task, args=(i, num_threads))
        thread.start()
        threads.append(thread)

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    return ret_cells

if __name__ == '__main__':
    cells = load_cells(INPUT_FILE)
    output_cells = translate_cells(cells, THREADS_NUM)

    # 因为是多线程，需要重新排序
    output_cells.sort(key=lambda cell: int(cell.index))

    # 输出到文件
    save_cells(output_cells, INPUT_FILE[:-4] + '_zh.srt')
