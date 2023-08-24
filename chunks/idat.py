from .chunk import chunk

class idat(chunk):
    
    def __init__(self, bytes):
        super().__init__(bytes)

        self.img_data = self.ch_data


    def __str__(self) -> str:
        return 'idat'

    __repr__ = __str__