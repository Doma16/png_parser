from .chunk import chunk

class plte(chunk):

    def __init__(self, bytes):
        super().__init__(bytes)

        if self.len % 3 != 0:
            raise ValueError
        
        self.palette = []

        for i in range(0, self.len, 3):
            self.palette.append(self.ch_data[i:i+3])
        

    def __str__(self) -> str:
        return 'plte'

    __repr__ = __str__