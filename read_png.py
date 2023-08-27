from chunks.chunk import chunk
from chunks.idat import idat
from chunks.iend import iend
from chunks.ihdr import ihdr
from chunks.plte import plte

import zlib
import sys

import numpy as np
import matplotlib.pyplot as plt

def parse(data, ret_nodes=False):

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

    if ret_nodes:
        return parsed

    ihdr_chunk:ihdr = parsed[0]
    return ihdr_chunk, stream_idat

def none_unfilter(row, _, bpp):
    return row

def sub_unfilter(row, _, bpp):
    new_row = b''

    for x in range(len(row)):
        if x - bpp < 0:
            raw_b = 0
        else:
            raw_b = new_row[x-bpp]
        sub = row[x]
        
        raw = (sub + raw_b) % 256
        raw = raw.to_bytes(1, 'big')
        
        new_row += raw
    return new_row

def up_unfilter(row, prev_row, _):
    new_row = b''

    for x in range(len(row)):
        if len(prev_row) == 0:
            prior = 0
        else:
            prior = prev_row[x]
        up = row[x]

        raw = (up + prior) % 256
        raw = raw.to_bytes(1, 'big')
        
        new_row += raw
    return new_row

def average_unfilter(row, prev_row, bpp):
    new_row = b''

    for x in range(len(row)):
        if len(prev_row) == 0:
            prior = 0
        else:
            prior = prev_row[x]
        if x - bpp < 0:
            raw_b = 0
        else:
            raw_b = new_row[x-bpp]

        raw = (row[x] + (raw_b + prior) // 2) % 256
        raw = raw.to_bytes(1, 'big')

        new_row += raw
    return new_row

def paethe_predictor(a, b, c):
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc: return a
    elif pb <= pc: return b
    else: return c

def paethe_unfilter(row, prev_row, bpp):
    new_row = b''

    for x in range(len(row)):
        if x - bpp < 0:
            raw_b = 0
        else:
            raw_b = new_row[x-bpp]
        if len(prev_row) == 0:
            prior = 0
        else:
            prior = prev_row[x]
        if x - bpp < 0 or len(prev_row) == 0:
            prior_b = 0
        else:
            prior_b = prev_row[x-bpp]

        pp = paethe_predictor(raw_b, prior, prior_b)
        raw = (row[x] + pp) % 256
        raw = raw.to_bytes(1, 'big')

        new_row += raw
    return new_row

def unfilter_row(bit, scanrow, prevrow):
    
    type = int(bit.hex(), base=16)

    type_name = {
        0: none_unfilter,
        1: sub_unfilter,
        2: up_unfilter,
        3: average_unfilter,
        4: paethe_unfilter
    }
    method = type_name[type]
    bpp = 4
    return method(scanrow, prevrow, bpp)

def uncompress(ihdr_chunk, stream_idat):
    print(f'Color type: {ihdr_chunk.color_type}, Bit depth: {ihdr_chunk.bit_depth}')

    filtered_image = zlib.decompress(stream_idat)
    width = ihdr_chunk.width
    height = ihdr_chunk.height

    if ihdr_chunk.color_type != 6:
        raise NotImplementedError

    if ihdr_chunk.bit_depth != 8:
        raise NotImplementedError
    
    reading = (1, 1+4*width)
    line_len = sum(reading) - 1

    rows = []
    prev_scanrow = b''

    for i in range(height):
        bit = filtered_image[0+line_len*i:reading[0]+line_len*i]
            
        scanrow = filtered_image[reading[0]+line_len*i:reading[1]+line_len*i]
        decoded_row = unfilter_row(bit, scanrow, prev_scanrow)

        rows.append(decoded_row)
        prev_scanrow = decoded_row
    
    for id, row in enumerate(rows):
        new_row_val = []
        for i in range(0, len(row), 4):
            r = row[i]
            g = row[i+1]
            b = row[i+2]
            a = row[i+3]
            
            pix = np.array([r,g,b,a])
            new_row_val.append(pix)

        rows[id] = np.stack(new_row_val)

    
    img = np.stack(rows)
    return img

def main():

    image_name = 'sal4.png'
    if len(sys.argv) == 2:
        image_name = sys.argv[-1]

    with open(image_name, 'rb') as f:
        data = f.read()

    ihdr_chunk, stream_idat = parse(data)
    image = uncompress(ihdr_chunk, stream_idat)
   
    plt.imshow(image)
    plt.show()


if __name__ == '__main__':
    main()