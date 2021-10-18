import sys
permutation = [151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,88,237,149,56,87,174,20,125,136,171,168, 68,175,74,165,71,134,139,48,27,166,77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,102,143,54, 65,25,63,161, 1,216,80,73,209,76,132,187,208, 89,18,169,200,196,135,130,116,188,159,86,164,100,109,198,173,186, 3,64,52,217,226,250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,223,183,170,213,119,248,152, 2,44,154,163, 70,221,153,101,155,167, 43,172,9,129,22,39,253, 19,98,108,110,79,113,224,232,178,185, 112,104,218,246,97,228,251,34,242,193,238,210,144,12,191,179,162,241, 81,51,145,235,249,14,239,107,49,192,214, 31,181,199,106,157,184, 84,204,176,115,121,50,45,127, 4,150,254,138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180]

p_ove = []
for i in range(512):
    p_ove.append(permutation[i%256])



def fade(t:float):
    return t * t * t * (t * (t * 6 - 15) + 10)
    # Perlin's Fade Function

def inc(x: int):
    x += 1
    return x

def grad(hash:int, x:float, y:float, z:float):
    dict={
        0x0:   x + y,
        0x1:  -x + y,
        0x2:   x - y,
        0x3:  -x - y,
        0x4:   x + z,
        0x5:  -x + z,
        0x6:   x - z,
        0x7:  -x - z,
        0x8:   y + z,
        0x9:  -y + z,
        0xA:   y - z,
        0xB:  -y - z,
        0xC:   y + x,
        0xD:  -y + z,
        0xE:   y - x,
        0xF:  -y - z
    }
    return dict.get(hash&0xF, 0)

def interpolate(a1:float, a0:float, w:float):
    return (a1 - a0) * ((w * (w * 6.0 - 15.0) + 10.0) * w * w * w) + a0



def perlin(x:float, y:float, z:float):
    xi = int(x) & 255
    yi = int(y) & 255
    zi = int(z) & 255

    xf = x-xi
    yf = y-yi
    zf = z-zi
    u = fade(xf)
    v = fade(yf)
    w = fade(zf)
    # using perlin hash function for random gradeint vector generation
    aaa = p_ove[p_ove[p_ove[    xi ]+    yi ]+    zi ]
    aba = p_ove[p_ove[p_ove[    xi ]+inc(yi)]+    zi ]
    aab = p_ove[p_ove[p_ove[    xi ]+    yi ]+inc(zi)]
    abb = p_ove[p_ove[p_ove[    xi ]+inc(yi)]+inc(zi)]
    baa = p_ove[p_ove[p_ove[inc(xi)]+    yi ]+    zi ]
    bba = p_ove[p_ove[p_ove[inc(xi)]+inc(yi)]+    zi ]
    bab = p_ove[p_ove[p_ove[inc(xi)]+    yi ]+inc(zi)]
    bbb = p_ove[p_ove[p_ove[inc(xi)]+inc(yi)]+inc(zi)]
    # grad function calculates the dot product accordingly at the 8 vertices of the cube
    x1 = interpolate(grad (aaa, xf  , yf  , zf), grad (baa, xf-1, yf  , zf), u)                                     
    x2 = interpolate(grad (aba, xf  , yf-1, zf), grad (bba, xf-1, yf-1, zf), u)
    y1 = interpolate(x1, x2, v)
    x1 = interpolate(grad (aab, xf  , yf  , zf-1),grad (bab, xf-1, yf  , zf-1), u)
    x2 = interpolate(grad (abb, xf  , yf-1, zf-1), grad (bbb, xf-1, yf-1, zf-1), u)
    y2 = interpolate (x1, x2, v)
    return (interpolate(y1, y2, w)+1)/2   

# print(perlin(4.56, 7.89, 7.89434))

# print(sys.argv)
print(perlin(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])))
