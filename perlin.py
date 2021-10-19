import sys
import qrng
import os
from dotenv import load_dotenv

load_dotenv()

filer = open(r"C:\Users\pragy\Documents\qiskit\QC_Hackathon\state.txt", 'r')
a = filer.read()
filer.close()

if a == '0':
    with open(r"C:\Users\pragy\Documents\qiskit\QC_Hackathon\permut.txt", "r") as permutat:
	    permutation = permutat.readlines()

    for i in range(len(permutation)):
        k = permutation[i]
        permutation[i] = int(k)
    permutat.close()

    qrng.set_provider_as_IBMQ(os.environ.get('MY_TOKEN'))
    qrng.set_backend('ibmq_santiago')

    for i in range(255, 0, -1):
        j = qrng.get_random_int32()
        j %= i
        k = permutation[i]
        permutation[i] = permutation[j]
        permutation[j] = k
    
    filer = open(r"C:\Users\pragy\Documents\qiskit\QC_Hackathon\list.txt", 'w')
    for i in permutation:
        filer.write(str(i)+"\n")
    filer.close()

    filer = open(r"C:\Users\pragy\Documents\qiskit\QC_Hackathon\state.txt", "w")
    filer.write("1")
    filer.close()

with open(r"C:\Users\pragy\Documents\qiskit\QC_Hackathon\list.txt", "r") as permutat:
	    permutation = permutat.readlines()

for i in range(len(permutation)):
    k = permutation[i]
    permutation[i] = int(k)
permutat.close()

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
