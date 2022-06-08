""" This code creates a curve between two points """
import numpy as np
import math

def rotate_origin_array(xy, radians):
    """Only rotate a point around the origin (0, 0)."""
    radians *= -1.0
    x, y = xy
    xx = x * math.cos(radians) + y * math.sin(radians)
    yy = -x * math.sin(radians) + y * math.cos(radians)

    return [xx, yy]
    
def curve_data(center, radius, start, end, clockwise):
    """ create arc of points from inputs """
    step = np.pi / 30.0
    
    if clockwise:
        step *= -1.0
        if end > start:
            end -= np.pi * 2.0
    else:
        step *= 1.0
        if end < start: 
            end += np.pi * 2.0
        
    array = []
    last = cur = start
    cur += step
    while (last - end) * (cur - end) > 0.0:
        last = cur
        x = math.cos(cur) * radius + center[0]
        y = math.sin(cur) * radius + center[1]
        array.append([x,y])
        cur += step
    
    return array

def get_intersection(a1, a2, b1, b2):
    """ find the intersection of two rays """
    av = [ (a2[0] - a1[0]), (a1[1] - a2[1]) ]
    a3 = av[1] * a1[0] + av[0] * a1[1]

    bv = [ (b2[0] - b1[0]), (b1[1] - b2[1]) ]
    b3 = bv[1] * b1[0] + bv[0] * b1[1]

    determinant = av[1] * bv[0] - bv[1] * av[0]

    if determinant != 0:
        x = (bv[0] * a3 - av[0] * b3) / determinant
        y = (av[1] * b3 - bv[1] * a3) / determinant
        point = [ x, y ]
        return point
    return None
    
def cross(vec):
    """ return tangent to this vector """
    return np.array([-vec[1],vec[0]])
    
def main(starting, ending, radian):
    """ calculate the curve, translated from Ensemble Javascript to Python """
    
    if radian == 0.0:
        # 0 degrees for 
        return [ ], 0.0 # EARLY EXIT!

    radian *= -1.0

    start = np.array(starting)
    end = np.array(ending)
    vec = end - start
    distance = np.linalg.norm(vec)
    normal = vec / distance
    crossy = cross(normal)
    
    tangent1 = rotate_origin_array(crossy, -np.pi/2.0 - radian)
    tangent2 = rotate_origin_array(crossy, -np.pi/2.0 + radian)
    bisectorNormal1 = cross(tangent1);
    bisectorNormal2 = cross(tangent2);

    # If our arc is inverted, reverse our bisector vectors.
    if radian < 0:
        bisectorNormal1 = bisectorNormal1 * -1.0
        bisectorNormal2 = bisectorNormal2 * -1.0

    # draw a partial circle at this point
    bisectorNormal1 *= 999999.0
    bisectorNormal2 *= 999999.0
    bisectorNormal1 += start
    bisectorNormal2 += end
    center = start
    if abs(abs(radian) - np.pi * 0.5) < 0.001:
        # 90 degrees or -90
        center = start + distance * 0.5 * normal
    else:
        center = get_intersection(start, bisectorNormal1, end, bisectorNormal2)

    radius = abs(np.linalg.norm(center-start))
    start_rad = math.atan2(bisectorNormal1[1], bisectorNormal1[0]) + np.pi
    end_rad = math.atan2(bisectorNormal2[1], bisectorNormal2[0]) + np.pi
    clockwise = radian < 0

    out_array = curve_data( center, radius, start_rad, end_rad, clockwise)
    
    if len(out_array) > 2:
        # reverse the array, if the first element is further away from the start than the last
        first_delta = abs(np.linalg.norm(out_array[0] - start))
        last_delta = abs(np.linalg.norm(out_array[-1] - start))
            
        delta = [ out_array[0][0] - out_array[1][0], out_array[0][1] - out_array[1][1] ]
        out_length = math.sqrt(delta[0] * delta[0] + delta[1] * delta[1]) * len(out_array)
        
        if first_delta > last_delta:
            out_array.reverse()
            
        return out_array, out_length
    else:
        return [], 0.0 # EARLY EXIT!

if __name__ == '__main__':
    print(main([205,-213],[305,-113.5],45.0/180.0*np.pi))