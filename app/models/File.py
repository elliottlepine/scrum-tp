from adapters.FileSystemAdapter import FileSystemAdapter
import re

class File:
    def __init__(self, path: str, file):
        self.file = file
        self.path = path
        self.content = self.file.read()

    def create(self):
        FileSystemAdapter.getInstance().create(self)

    @staticmethod
    def read(path: str):
        return File(path, FileSystemAdapter.getInstance().read(path))

    def delete(self):
        FileSystemAdapter.getInstance().delete(self.path)

    def get_title(self):
        block_regex = r'\<block[\s\S]+?\>[\s\S]+?\<\/block\>'
        blocks = re.findall(block_regex, self.content)
        max_height_block = 0
        title_block = blocks[0]

        for block in blocks[:3]:
            block_max_height = self.get_max_height(block)
            if max_height_block < block_max_height:
                max_height_block = block_max_height
                title_block = block

        words = re.sub(r'<[\s\S]+?>', '', title_block)
        return  ' '.join(words.split())

    def get_max_height(self, block: str) -> int:
        word_regex = r'\<word[\s\S]+?\>[\s\S]+?\<\/word\>'
        max_height = 0

        for word in re.findall(word_regex, block):
            word_height_min = self.get_word_height(word, min=True)
            word_height_max = self.get_word_height(word, min=False)
            word_height = word_height_max - word_height_min
            if word_height > max_height:
                max_height = word_height

        return max_height

    def get_word_height(self, word, *, min = True):
        decimal_regex = r'(\d*[\.]\d*)'
        height_max_regex = r'yMax=\"'
        height_min_regex = r'yMin=\"'
        regex = height_min_regex if min == True else height_max_regex
        try:
            height_tag = re.findall(regex + decimal_regex, word)
            height = re.findall(decimal_regex, height_tag[0])
        except Exception as e:
            print(e)
            return 0

        return float(height[0])

