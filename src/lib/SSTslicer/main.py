'''
Main functionality of ``image_slicer``.
'''
import os
from io import BytesIO
from math import sqrt, ceil, floor
from PIL import Image


from .helpers import get_basename


class Tile(object):
    """Represents a single tile."""

    def __init__(self, image, number, position, coords, filename=None):
        self.image = image
        self.number = number
        self.position = position
        self.coords = coords
        self.filename = filename

    @property
    def row(self):
        return self.position[0]

    @property
    def column(self):
        return self.position[1]

    @property
    def basename(self):
        """Strip path and extension. Return base filename."""
        return get_basename(self.filename)

    def generate_filename(self, directory=os.getcwd(), prefix='tile', format='png', path=True, reversed=False):
        """Construct and return a filename for this tile."""
        if reversed:
            xT, yT = self.row, self.column
        else:
            xT, yT = self.column, self.row
        filename = prefix + '_{col:01d}_{row:01d}.{ext}'.format(
                      col=xT, row=yT, ext=format.lower().replace('jpeg', 'jpg'))
        if not path:
            return filename
        return os.path.join(directory, filename)

    def save(self, filename=None, format='png'):
        if not filename:
            filename = self.generate_filename(format=format)
        self.image.save(filename, format)
        self.filename = filename    

    def get_bytes(self, format='tga'):
        bTile = BytesIO()
        self.image.save(bTile, format)
        return bTile.getvalue()[:-26] # cut the last 26 bytes, because PIL adds some useless metadata, which fuck up SSTviewer

    def __repr__(self):
        """Show tile number, and if saved to disk, filename."""
        if self.filename:
            return '<Tile #{} - {}>'.format(self.number,
                                            os.path.basename(self.filename))
        return '<Tile #{}>'.format(self.number)


def calc_columns_rows(n):
    """
    Calculate the number of columns and rows required to divide an image
    into ``n`` parts.

    Return a tuple of integers in the format (num_columns, num_rows)
    """
    num_columns = int(ceil(sqrt(n)))
    num_rows = int(ceil(n / float(num_columns)))
    return (num_columns, num_rows)

def get_combined_size(tiles):
    """Calculate combined size of tiles."""
    # TODO: Refactor calculating layout to avoid repetition.
    columns, rows = calc_columns_rows(len(tiles))
    tile_size = tiles[0].image.size
    return (tile_size[0] * columns, tile_size[1] * rows)

def join(tiles, width=0, height=0):
    """
    @param ``tiles`` - Tuple of ``Image`` instances.
    @param ``width`` - Optional, width of combined image.
    @param ``height`` - Optional, height of combined image.
    @return ``Image`` instance.
    """
    # Don't calculate size if width and height are provided
    # this allows an application that knows what the
    # combined size should be to construct an image when
    # pieces are missing.

    if width > 0 and height > 0:
        im = Image.new('RGB',(width, height), None)
    else:
        im = Image.new('RGB', get_combined_size(tiles), None)
    columns, rows = calc_columns_rows(len(tiles))
    for tile in tiles:
        try:
            im.paste(tile.image, tile.coords)
        except IOError:
            #do nothing, blank out the image
            continue
    return im

def validate_image(image, number_tiles):
    """Basic sanity checks prior to performing a split."""
    TILE_LIMIT = 99 * 99

    try:
        number_tiles = int(number_tiles)
    except:
        raise ValueError('number_tiles could not be cast to integer.')

    if number_tiles > TILE_LIMIT or number_tiles < 2:
        raise ValueError('Number of tiles must be between 2 and {} (you \
                          asked for {}).'.format(TILE_LIMIT, number_tiles))

def validate_image_col_row(image , col , row):
    """Basic checks for columns and rows values"""
    SPLIT_LIMIT = 99

    try:
        col = int(col)
        row = int(row)
    except:
        raise ValueError('columns and rows values could not be cast to integer.')

    if col < 1 or row < 1\
        or col > SPLIT_LIMIT or row > SPLIT_LIMIT:
        raise ValueError('Number of columns and rows must be between 1 and {} (you \
                          asked for rows: {} and col: {}).'.format(SPLIT_LIMIT, row, col))
    if col == 1 and row == 1:
        raise ValueError('There is nothing to divide. You asked for the entire image.')

def slice(filename_or_bytesIO, name: str, number_tiles=None, col=None, row=None, 
          save=True, DecompressionBombWarning=True, reversed=False):
    """
    Split an image into a specified number of tiles.

    Args:
       filename_or_bytesIO (string/BytesIO): the image file as BytesIO object
       number_tiles (int):  The number of tiles required.

    Kwargs:
       save (bool): Whether or not to save tiles to disk.
       DecompressionBombWarning (bool): Whether to suppress Pillow DecompressionBombWarning

    Returns:
        List of :class:`Tile` instances.
    """
    if DecompressionBombWarning is False:
        Image.MAX_IMAGE_PIXELS = None
    
    im = Image.open(filename_or_bytesIO)
    im_w, im_h = im.size

    columns = 0
    rows = 0
    if number_tiles:
        validate_image(im, number_tiles)
        columns, rows = calc_columns_rows(number_tiles)
#        extras = (columns * rows) - number_tiles # TODO: not used
    else:
        validate_image_col_row(im, col, row)
        columns = col
        rows = row


    tile_w, tile_h = int(floor(im_w / columns)), int(floor(im_h / rows))

    tiles = []
    number = 1
    for pos_y in range(0, im_h - rows, tile_h): # -rows for rounding error.
        for pos_x in range(0, im_w - columns, tile_w): # as above.
            area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)
            image = im.crop(area)
            position = (int(floor(pos_x / tile_w)) + 1,
                        int(floor(pos_y / tile_h)) + 1)
            coords = (pos_x, pos_y)
            tile = Tile(image, number, position, coords)
            tiles.append(tile)
            number += 1
    if save:
        save_tiles(tiles, prefix=name, directory=os.getcwd(), reversed=reversed)
    return tiles

def save_tiles(tiles, prefix='', directory=os.getcwd(), format='tga', reversed=False):
    """
    Write image files to disk. Create specified folder(s) if they
       don't exist. Return list of :class:`Tile` instance.

    Args:
       tiles (list):  List, tuple or set of :class:`Tile` objects to save.
       prefix (str):  Filename prefix of saved tiles.

    Kwargs:
       directory (str):  Directory to save tiles. Created if non-existant.

    Returns:
        Tuple of :class:`Tile` instances.
    """
#    Causes problems in CLI script.
#    if not os.path.exists(directory):
#        os.makedirs(directory)
    for tile in tiles:
        tile.save(filename=tile.generate_filename(prefix=prefix,
                                                  directory=directory,
                                                  format=format,
                                                  reversed=reversed),
                                                  format=format)
    return tuple(tiles)


def get_image_column_row(filename):
    """Determine column and row position for filename."""
    filename = filename.split('.')[-2].split('_')
    row = int(filename[-2])
    column = int(filename[-1])

    return (column-1, row-1)

def get_tiles(files: list):

    tiles = []
    if len(files) > 0:        
        for i, file in enumerate(files):
            pos = get_image_column_row(file[0])
            im = Image.open(file[1])

            position_xy=[0,0]
            count=0
            for a,b in zip(pos,im.size):
                position_xy[count] = a*b
                count = count + 1
            tiles.append(Tile(image = im, position = pos, number = i+1, coords = position_xy, filename = file[0]))
    return tiles
