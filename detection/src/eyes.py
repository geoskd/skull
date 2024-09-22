
import time
import smbus
import numpy

class eyes:

    def __init__(self):
        self.i2cbus = smbus.SMBus(1)
        self.addresses = [0x28,0x29,0x2a,0x2b]
        for address in self.addresses:
            self.i2cbus.write_byte_data(address, 0x00, 0x40 )
            self.i2cbus.write_byte_data(address, 0x02, 0x00 )
        self.left_buffer = numpy.zeros((6,8), dtype=int)
        self.right_buffer = numpy.zeros((6,8), dtype=int)

    def test(self):
        for address in self.addresses:
            for i in range( 0x0f, 0x27 ):
                self.i2cbus.write_byte_data(address, i, 0xff )
                time.sleep(0.1)

    def render(self):
        for x in range( 0, 6 ):
            for y in range( 0, 8 ):
                #draw each of the eyes
                # translate x and y into the left and right address'
                if( x < 3 ):
                    left_chip = 0x28;
                    right_chip = 0x2a;
                    address = ( x * 8 ) + y + 0x0f
                else:
                    left_chip = 0x29;
                    right_chip = 0x2b;
                    address = ( (x - 3 ) * 8 ) + y + 0x0f
                self.i2cbus.write_byte_data( left_chip, address, self.left_buffer[x][y] )
                self.i2cbus.write_byte_data( right_chip, address, self.right_buffer[x][y] )
        
    def reset_buffer(self):
        self.left_buffer = numpy.zeros((6,8), dtype=int)
        self.right_buffer = numpy.zeros((6,8), dtype = int)


    def draw_pixel( self, side, x, y, value ):
        if x < 6 and x >= 0 and side < 2 and side >= 0:
            if side == 0:
                self.left_buffer[x][y] = value * 0xff
            else:
                self.right_buffer[x][y] = value * 0xff
            
