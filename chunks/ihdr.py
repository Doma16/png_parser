from .chunk import chunk

class ihdr(chunk):

    def __init__(self, bytes):
        super().__init__(bytes)

        if self.length != 13:
            raise ValueError

        self.width = int(self.ch_data[0:4].hex(), base=16)
        self.height = int(self.ch_data[4:8].hex(), base=16)

        self.bit_depth = int(self.ch_data[8:9].hex(), base=16)
        self.color_type = int(self.ch_data[9:10].hex(), base=16)
        self.compression_method = int(self.ch_data[10:11].hex(), base=16)
        self.filter_method = int(self.ch_data[11:12].hex(), base=16)
        self.interlace_method = int(self.ch_data[12:13].hex(), base=16)


    def __str__(self) -> str:

        out = f'IHDR chunk: \n' \
            f' Width: {self.width} \n' \
            f' Heigth: {self.height} \n' \
            f' Bit depth: {self.bit_depth} \n' \
            f' Color type: {self.color_type} \n' \
            f' Compression method: {self.compression_method} \n' \
            f' Filter method: {self.filter_method} \n' \
            f' Interlace method: {self.interlace_method}'
        return out

    def __repr__(self) -> str:
        return 'ihdr'