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
        
    # 重载copy方法
    def copy(self):
        return cell(self.index, self.time, self.content)

    def __str__(self):
        return self.index + '\n' + self.time + '\n' + self.content + '\n'
    

def load_cells(file_name) -> list:
    content = []
    # 打开srt字幕文件
    with open(file_name) as f:
        # 读取文件内容
        content = f.read()

    # 以换行符分割字符串
    content = content.split('\n')
    print('load lines: ' + str(len(content)))

    ret_cells = []
    for i in range(0, len(content)-1, 4):
        # 将每一组元素作为一个cell对象
        ret_cells.append(cell(content[i], content[i+1], content[i+2]))
    return ret_cells

def save_cells(cells: list, file_name):
    # 保存cells到文件
    with open(file_name, 'w') as f:
        for cell in cells:
            f.write(str(cell) + '\n')