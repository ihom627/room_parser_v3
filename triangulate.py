""" This code converts a polygon into triangles """
import sys

indices = []

def create_points(points, indices):
    """ converts indexes and points into a polygon """
    array = []
    for index in indices:
        array.append(points[index])
    return array

def create_triangles(points,u,v,w,v_array,nv,count):
    """ adds more triangles to the indices """
    global indices
    if snip_triangle(points, u, v, w, nv, v_array):
        a = v_array[u]
        b = v_array[v]
        c = v_array[w]
        indices.append(a)
        indices.append(b)
        indices.append(c)
        s = v
        t = v + 1
        while t < nv:
            v_array[s] = v_array[t]
            s += 1
            t += 1
        nv -= 1
        count = 2 * nv
    return nv, count

def remove_duplicates(wall):
    """" remove dupicates from an array of 2D points """
    if len(wall) != 0:
        # remove duplicates
        corner_prev = wall[0]
        i = 1
        while i < len(wall):
            corner = wall[i]
            if corner[0] == corner_prev[0] and corner[1] == corner_prev[1]:
                wall = wall[:i] + wall[i+1:]
            else:
                i += 1
            corner_prev = corner
    return wall

def triangulate(points):
    """ converts a polygon into triangles """
    global indices

    points = remove_duplicates(points) # This must happen!

    indices = []
    n = len(points)
    if n < 3:
        return points


    v_array = list(range(n))
    if get_area(points) < 0:
        v_array.reverse()

    nv = n
    count = 2 * nv
    v = nv - 1
    while nv > 2:
        count -= 1
        if count <= 0:
            return create_points(points, indices)

        u = v
        if nv <= u:
            u = 0
        v = u + 1
        if nv <= v:
            v = 0
        w = v + 1
        if nv <= w:
            w = 0

        nv, count = create_triangles(points,u,v,w,v_array,nv,count)

    indices.reverse()
    return create_points(points, indices)

def get_area(points):
    """ calculate the area of these points """
    n = len(points)
    area = 0.0
    p = n - 1
    for q in range(n):
        pval = points[p]
        qval = points[q]
        area += pval[0] * qval[1] - qval[0] * pval[1]
        p = q
    return (area * 0.5)

def snip_triangle(points, u, v, w, n, v_array):
    """ remove an ear """
    A = points[v_array[u]]
    B = points[v_array[v]]
    C = points[v_array[w]]
    epsilon_test = (((B[0] - A[0]) * (C[1] - A[1])) - ((B[1] - A[1]) * (C[0] - A[0])))
    if sys.float_info.epsilon > epsilon_test:
        return False
    for p in range(n):
        if ((p == u) or (p == v) or (p == w)):
            continue
        P = points[v_array[p]]
        if inside_triangle(A, B, C, P):
            return False
    return True

def inside_triangle(A, B, C, P):
    """ is this point inside of the triangle? """
    ax = C[0] - B[0]
    ay = C[1] - B[1]
    
    bx = A[0] - C[0]
    by = A[1] - C[1]
    
    cx = B[0] - A[0]
    cy = B[1] - A[1]
    
    apx = P[0] - A[0]
    apy = P[1] - A[1]
    
    bpx = P[0] - B[0]
    bpy = P[1] - B[1]
    
    cpx = P[0] - C[0]
    cpy = P[1] - C[1]

    a_cross_bp = ax * bpy - ay * bpx
    c_cross_ap = cx * apy - cy * apx
    b_cross_cp = bx * cpy - by * cpx

    return ((a_cross_bp >= 0.0) and (b_cross_cp >= 0.0) and (c_cross_ap >= 0.0))

def models_inside_best(offset, rooms):
    """ Find the triangulated room this offset is inside """
    tris_best = None
    index_best = -1
    index_cur = 0
    for floor in rooms:
        i = 0
        if [ None, None ] in floor:
            index_cur += 1
            continue
        tris = triangulate(floor)
        while i < len(tris) - 2:
            vertA = tris[i]
            i += 1
            vertB = tris[i]
            i += 1
            vertC = tris[i]
            i += 1
            if inside_triangle(vertC, vertB, vertA, offset):
                tris_best = tris
                index_best = index_cur
                break
        index_cur += 1
    return tris_best, index_best

def models_inside(offset, rooms, json_models):
    """ only show models that are inside the same room as the offset """
    
    # only render current room if there is a room.
    if len(rooms) == 0:
        return json_models, -1
        
    tris_best, index_best = models_inside_best(offset, rooms)
    
    if tris_best != None:
        tris = tris_best
        j = 0
        while j < len(json_models):
            model = json_models[j]
            i = 0
            is_inside = False
            while i < len(tris):
                vertC = tris[i]
                i += 1
                vertB = tris[i]
                i += 1
                vertA = tris[i]
                i += 1
                if inside_triangle(vertA, vertB, vertC, model["pos"]):
                    is_inside = True
                    break
            if not is_inside:
                del json_models[j]
            else:
                j += 1
    
    return json_models, index_best
