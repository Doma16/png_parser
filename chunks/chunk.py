class chunk:
    # length, chunk type, chunk data, crc
    def __init__(self, bytes):
        
        self.length = int(bytes[0:4].hex(), base=16)
        self.ch_type = bytes[4:8]
        self.ch_data = bytes[8: 8+self.length]
        self.crc = bytes[8+self.length: 12+self.length]

    def __str__(self) -> str:
        return 'chunk'

    __repr__ = __str__

    def write(self):
        data = self.length.to_bytes(4, 'big') + \
               self.ch_type + \
               self.ch_data + \
               self.crc
        
        return data
    
    def size(self):
        return self.length + 12
