# Function to left
# rotate number by  bits
def leftRotate(number, bits, INT_BITS ):
 
    # In n<<d, last d bits are 0.
    # To put first 3 bits of n at 
    # last, do bitwise or of n<<d
    # with n >>(INT_BITS - d) 
    x= (number << bits)|(number >> (INT_BITS - bits))
    y = x &  ((1<<INT_BITS)-1 )
    return y

def leftRotateInt16(number, bits):
    return leftRotate(number,bits,16)

def takeFromRight(number,bits):
    y =number &  ((1<<bits)-1 )
    return y

