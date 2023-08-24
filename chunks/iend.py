from .chunk import chunk

class iend(chunk):

    def __init__(self, bytes):
        super().__init__(bytes)


    def __str__(self) -> str:
        return 'iend'

    __repr__ = __str__