from chunks.chunk import chunk
from chunks.idat import idat
from chunks.iend import iend
from chunks.ihdr import ihdr
from chunks.plte import plte

import zlib

def parse(data):

    signature = data[0:8]
    if int(signature.hex(), base=16) != 9894494448401390090:
        raise ValueError

    chunks = {'IDAT': idat,
              'IEND': iend,
              'IHDR': ihdr,
              'PLTE': plte}
    
    pos = 8

    
    parsed = []
    while pos < len(data):

        look = data[pos:pos+8]
        length = int(look[0:4].hex(), base=16)
        type_:bytes = look[4:8].decode()
        
        if type_ in chunks:
            parsed.append(chunks[type_](data[pos: pos+12+length]))
        else:
            parsed.append(chunk(data[pos: pos+12+length]))

        pos += 12 + length

    stream_idat = b''
    for item in parsed:
        if type(item) == idat:
            stream_idat += item.img_data

    ihdr_chunk:ihdr = parsed[0]
    return ihdr_chunk, stream_idat
    

def main():

    image_name = 'MB_original.png'
    with open(image_name, 'rb') as f:
        data = f.read()

    ihdr_chunk, stream_idat = parse(data)

    print(ihdr_chunk)
    print(len(stream_idat))

    out = zlib.decompress(stream_idat)
    breakpoint()

if __name__ == '__main__':
    main()