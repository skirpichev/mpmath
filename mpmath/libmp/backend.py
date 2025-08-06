import fractions
import os


#----------------------------------------------------------------------------#
# Support GMPY for high-speed large integer arithmetic.                      #
#                                                                            #
# To allow an external module to handle arithmetic, we need to make sure     #
# that all high-precision variables are declared of the correct type. MPZ    #
# is the constructor for the high-precision type. It defaults to Python's    #
# long type but can be assinged another type, typically gmpy.mpz.            #
#                                                                            #
# MPZ must be used for the mantissa component of an mpf and must be used     #
# for internal fixed-point operations.                                       #
#                                                                            #
# Side-effects:                                                              #
# * "is" cannot be used to test for special values.  Must use "==".          #
#----------------------------------------------------------------------------#

gmpy = None
BACKEND = 'python'
MPZ = int
MPQ = fractions.Fraction
import collections
stats = collections.defaultdict(int)

if 'MPMATH_NOGMPY' not in os.environ:
    try:
        import gmpy2 as gmpy
        BACKEND = 'gmpy'
        MPQ = gmpy.mpq
    except ImportError:
        try:
            import gmp as gmpy
            BACKEND = 'gmp'
        except ImportError:
            pass

    if gmpy:
        def MPZ(*args):
            global stats
            if len(args) != 1:
                return gmpy.mpz(*args)
            x = args[0]
            bc = int(x).bit_length()
            if bc <= 10:
                stats['<=10'] += 1
            elif bc <= 24:
                stats['<=24'] += 1
            elif bc <= 53:
                stats['<=53'] += 1
            elif bc <= 113:
                stats['<=113'] += 1
            elif bc <= 237:
                stats['<=237'] += 1
            elif bc <= 1000:
                stats['<=1000'] += 1
            elif bc <= 3000:
                stats['<=3000'] += 1
            else:
                stats['other'] += 1
            return gmpy.mpz(x)

MPZ_ZERO = MPZ(0)
MPZ_ONE = MPZ(1)
MPZ_TWO = MPZ(2)
MPZ_THREE = MPZ(3)
MPZ_FIVE = MPZ(5)

int_types = (int,) if BACKEND == 'python' else (int, type(MPZ(1)))
