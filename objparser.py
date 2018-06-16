"""
This module implements a parser for Analyze spatial maps (.obj files).

Author: Petro Kostandy
"""
import struct
import numpy as np


class SpatialObject(object):
    """Data class storing header information about every object in the spatial map."""
    def __init__(self):
        self.name = ''  # null-terminated char32 string
        self.display_flag = 0  # int, 0 or 1
        self.copy_flag = 0  # uint8, 0 or 1
        self.mirror = 0  # uint8, 1-7
        self.status = 0  # uint8, unused
        self.n_used = 0  # uint8,
        self.shades = 0  # uint8

        self.s_red = 0  # int32
        self.s_green = 0  # int32
        self.s_blue = 0  # int32

        self.e_red = 0  # int32
        self.e_green = 0  # int32
        self.e_blue = 0  # int32

        self.x_rot = 0  # int32
        self.y_rot = 0  # int32
        self.z_rot = 0  # int32

        self.x_shift = 0  # int32
        self.y_shift = 0  # int32
        self.z_shift = 0  # int32

        self.x_center = 0  # int32
        self.y_center = 0  # int32
        self.z_center = 0  # int32

        self.i_xrot = 0  # int32
        self.i_yrot = 0  # int32
        self.i_zrot = 0  # int32

        self.i_xshift = 0  # int32
        self.i_yshift = 0  # int32
        self.i_zshift = 0  # int32

        self.min_x = 0  # int16
        self.min_y = 0  # int16
        self.min_z = 0  # int16

        self.max_x = 0  # int16
        self.max_y = 0  # int16
        self.max_z = 0  # int16

        self.opacity = 0.0  # float32
        self.opacity_thick = 0  # int32
        self.blendfactor = 0.0  # float32


class AnalyzeSpatialMap(object):
    """Describes an object that can fully capture the contents of an Analayze spatial map. This
    class can be initalized with an optional ``file`` argument.

    Args:
        file (str): Analyze spatial map file path. Optional.

    The following attributes are initialized and populated once `from_file` is called:
        version_code (int): File format revision number
        version (int): .obj file version
        width (int): Width of map in pixels
        height (int): Height of map in pixels
        depth (int): Depth of map in pixels
        n_objects (int): Number of objects (up to 256)
        n_vols (int): Number of object volumes

        objects (list): List of objects included in the spatial map
        vols (list): List of volumes contained within the spatial map;
            where each map is a 3 dimensional array.

    Usage::
        # Create instance with file argument
        s_map = AnalayzeSpatialMap(file='path/to/file.obj')

        # Alternatively, initialize instance and then call from_file method
        s_map = AnalyzeSpatialMap()
        s_map.from_file('path/to/file.obj')

        # Get numpy array representing the first volume
        s_map.get_data(0)
    """
    def __init__(self, file=None):
        self.version_code = 0
        self.version = 0
        self.width = 0
        self.height = 0
        self.depth = 0
        self.n_objects = 0
        self.n_vols = 1

        self.objects = []
        self.vols = []

        if file:
            self.from_file(file)


    @staticmethod
    def _read_nts(bytecode):
        """Reads one byte at a time from file buffer until a null character is encountered."""
        return bytecode.split(b'\x00')[0].decode('utf-8')


    def from_file(self, filename, verbose=0):
        """Parses the .obj file that is passed preserving its header information and casting
        the spatial maps as numpy arrays.

        Args:
            filename (str): Full .obj file path
            verbose (int, optional): Defaults to 0. Controls output verbosity.
        """
        with open(filename, 'rb') as f:
            self.version_code = int.from_bytes(
                f.read(4), byteorder='big', signed=False)

            # Set header_ints and version based on version_code
            if self.version_code < 20050829:
                self.version = 6
                header_ints = 4
            else:
                self.version = 7
                header_ints = 5

            header = []

            for i in range(header_ints):
                header.append(
                    int.from_bytes(f.read(4), byteorder='big', signed=False))

            self.width, self.height, self.depth = header[0:3]
            self.n_objects = header[3]

            if self.version > 7:
                self.n_vols = header[4]

            # Read in each object's parameters sequentially from spatial map header
            # Numerics bytes are stored by Analyze in big-endian order
            for i in range(self.n_objects):
                obj = SpatialObject()

                obj.name = self._read_nts(f.read(32))
                obj.display_flag = int.from_bytes(f.read(4), byteorder='big')
                obj.copy_flag = int.from_bytes(f.read(1), byteorder='big')
                obj.mirror = int.from_bytes(f.read(1), byteorder='big')
                obj.status = int.from_bytes(f.read(1), byteorder='big')
                obj.n_used = int.from_bytes(f.read(1), byteorder='big')
                obj.shades = int.from_bytes(f.read(4), byteorder='big')

                obj.s_red = int.from_bytes(f.read(4), byteorder='big')
                obj.s_green = int.from_bytes(f.read(4), byteorder='big')
                obj.s_blue = int.from_bytes(f.read(4), byteorder='big')

                obj.e_red = int.from_bytes(f.read(4), byteorder='big')
                obj.e_green = int.from_bytes(f.read(4), byteorder='big')
                obj.e_blue = int.from_bytes(f.read(4), byteorder='big')

                obj.x_rot = int.from_bytes(f.read(4), byteorder='big')
                obj.y_rot = int.from_bytes(f.read(4), byteorder='big')
                obj.z_rot = int.from_bytes(f.read(4), byteorder='big')

                obj.x_shift = int.from_bytes(f.read(4), byteorder='big')
                obj.y_shift = int.from_bytes(f.read(4), byteorder='big')
                obj.z_shift = int.from_bytes(f.read(4), byteorder='big')

                obj.x_center = int.from_bytes(f.read(4), byteorder='big')
                obj.y_center = int.from_bytes(f.read(4), byteorder='big')
                obj.z_center = int.from_bytes(f.read(4), byteorder='big')

                obj.i_xrot = int.from_bytes(f.read(4), byteorder='big')
                obj.i_yrot = int.from_bytes(f.read(4), byteorder='big')
                obj.i_zrot = int.from_bytes(f.read(4), byteorder='big')

                obj.i_xshift = int.from_bytes(f.read(4), byteorder='big')
                obj.i_yshift = int.from_bytes(f.read(4), byteorder='big')
                obj.i_zshift = int.from_bytes(f.read(4), byteorder='big')

                obj.min_x = int.from_bytes(f.read(2), byteorder='big')
                obj.min_y = int.from_bytes(f.read(2), byteorder='big')
                obj.min_z = int.from_bytes(f.read(2), byteorder='big')

                obj.max_x = int.from_bytes(f.read(2), byteorder='big')
                obj.max_y = int.from_bytes(f.read(2), byteorder='big')
                obj.max_z = int.from_bytes(f.read(2), byteorder='big')

                obj.opacity = struct.unpack('f', f.read(4))
                obj.opacity_thick = int.from_bytes(f.read(4), byteorder='big')
                obj.blendfactor = struct.unpack('f', f.read(4))

                self.objects.append(obj)

            # Read in the reminader of the file, which happens to be run-length encoded
            maps_rle = np.frombuffer(f.read(), dtype='uint8').reshape((-1, 2))
            i = 0

            # Iterate over each volume (relevant for 4-D data)
            for _ in range(self.n_vols):
                slice_num = 0
                temp_vol = np.zeros((self.height, self.width, self.depth))

                # Iterate over every slice separately
                while slice_num < self.depth:
                    pixel_num = 0
                    temp_slice = np.zeros((self.width * self.height))

                    while pixel_num < self.width * self.height:
                        mult, num = maps_rle[i, :]

                        temp_slice[pixel_num:pixel_num+mult] = np.repeat(num, mult)
                        pixel_num += mult
                        i += 1

                    temp_vol[:, :, slice_num] = temp_slice.reshape(self.height, self.width)
                    slice_num += 1

                self.vols.append(temp_vol.copy())

            if verbose > 0:
                print('Successfully imported {0}'.format(filename))
                print('Spatial map shape: {0}'.format(self.vols[0].shape))
                print('Number of objects (includes background): {0}'.format(self.n_objects))
                print('Number of volumes: {0}'.format(self.n_vols))
                print()


    def get_data(self, idx=0):
        """Returns a numpy array representing the spatial map."""
        return self.vols[idx]
