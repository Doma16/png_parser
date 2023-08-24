class chunk:
    # length, chunk type, chunk data, crc
    def __init__(self, bytes):
        
        self.len = int(bytes[0:4].hex(), base=16)
        self.ch_type = bytes[4:8]
        self.ch_data = bytes[8: 8+self.len ]
        self.crc = bytes[8+self.len, 12+self.len]

    def __str__(self) -> str:
        return 'chunk'

    __repr__ = __str__