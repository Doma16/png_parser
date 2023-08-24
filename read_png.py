from chunks.chunk import chunk
from chunks.idat import idat
from chunks.iend import iend
from chunks.ihdr import ihdr
from chunks.plte import plte

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
        type:bytes = look[4:8].decode()
        
        if type in chunks:
            parsed.append(chunks[type](data[pos: pos+12+length]))
        else:
            parsed.append(chunk(data[pos: pos+12+length]))

        pos += 12 + length
    
    return parsed
    

def main():

    image_name = 'MB_original.png'
    with open(image_name, 'rb') as f:
        data = f.read()

    parsed = parse(data)

    print(f'w: {parsed[0].width}, h: {parsed[0].height}, {parsed}')

if __name__ == '__main__':
    main()