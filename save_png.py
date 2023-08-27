import sys

from read_png import parse
from chunks.chunk import chunk
from chunks.idat import idat
from chunks.iend import iend
from chunks.ihdr import ihdr
from chunks.plte import plte



def write(nodes, name):

    with open(name, 'wb') as f:
        signature = (9894494448401390090).to_bytes(8,'big')
        f.write(signature)

        types = {
            idat,
            iend,
            ihdr,
            plte
        }

        for node in nodes:
            if type(node) in types:
                f.write(node.write())
 
def main():
    
    if len(sys.argv) == 3:
        image_name = sys.argv[-2]
        new_image_name = sys.argv[-1]

    with open(image_name, 'rb') as f:
        data = f.read()

    nodes = parse(data, ret_nodes=True)
    write(nodes, new_image_name)

if __name__ == '__main__':
    main()