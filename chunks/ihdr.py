from .chunk import chunk

class ihdr(chunk):

    def __init__(self, bytes):
        super().__init__(bytes)

        if self.len != 13:
            raise ValueError

        self.width = int(self.ch_data[0:4].hex(), base=16)
        self.height = int(self.ch_data[4:8].hex(), base=16)

        self.bit_depth = self.ch_data[8:9]
        self.color_type = self.ch_data[9:10]
        self.compression_method = self.ch_data[10:11]
        self.filter_method = self.ch_data[11:12]
        self.interlace_method = self.ch_data[12:13]


    def __str__(self) -> str:
        return 'ihdr'

    __repr__ = __str__