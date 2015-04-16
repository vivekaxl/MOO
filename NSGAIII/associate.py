from __future__ import division

def perpendicular_distance(pointa, pointb):
    def dotproduct(pointa, pointb):
        ret = 0
        for i, j in zip(pointa, pointb):
            ret += (i*j)
        return ret
    def magnitude(pointa):
        sum = 0
        for i in pointa:
            sum += i ** 2
        return sum ** 0.5
    mag = dotproduct(pointa, pointb)/(magnitude(pointb) ** 2)
    lengthb = magnitude(pointb) # hypotenuse
    lengtha = magnitude(pointa)
    base = lengtha * mag
    return (lengthb ** 2 - base ** 2) ** 0.5


if __name__ == "__main__":
    a = [1, -2, 3]
    b = [2, 4, 3]
    print perpendicular_distance(a, b)