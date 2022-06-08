""" Parses the Ensemble room data """ 
import json
import math
import numpy as np
import sys
try:
    import convert.curve as curve
except:
    import curve

floor_array = []
window_array = []
door_array = []

def add_door(pos, length):
    """ add a door to the array """ 
    global floor_array
    global door_array
    door_array.append({
        "pos": pos,
        "length": length, 
        "room_id": len(floor_array)
        })

def get_door():
    """ get the window array""" 
    global door_array
    return door_array
    
def add_window(pos, length):
    """ add a window to the array """ 
    global floor_array
    global window_array
    window_array.append({
        "pos": pos,
        "length": length, 
        "room_id": len(floor_array)
        })

def get_window():
    """ get the window array""" 
    global window_array
    return window_array
        
def reset():
    """ reset all arrays """
    global floor_array
    global window_array
    global door_array
    floor_array = []
    window_array = []
    door_array = []

def middle_arch(corner, corner_prev, pos, length, delta, dist):
    """ find the middle of the arch """ 
    norm = [ delta[0]/dist, delta[1]/dist ]
    middle_dist = pos * dist + length / 2
    middle_vec = [ norm[0]*middle_dist+corner_prev[0], norm[1]*middle_dist+corner_prev[1] ]
    return middle_vec
    
def parse_arch_one(arch, corner, corner_prev):
    """ Parse ONE architecture (walls,windows,doors,etc) """ 
    corner_delta = [corner[0]-corner_prev[0],corner[1]-corner_prev[1]]
    corner_dist = math.sqrt(corner_delta[0]*corner_delta[0] + corner_delta[1]*corner_delta[1])
    
    class_name = arch["className"]
    if "Door" in class_name:
        pos = middle_arch(corner, corner_prev, arch["pos"], arch["length"], corner_delta, corner_dist)
        add_door(pos, arch["length"])
    elif "Window" in class_name:
        pos = middle_arch(corner, corner_prev, arch["pos"], arch["length"], corner_delta, corner_dist)
        add_window(pos, arch["length"])
    
def parse_arch(arch_array, i, corner, corner_prev):
    """ Parse architectures (walls,windows,doors,etc) """ 
    for arch in arch_array:
        if arch["wall"] == i:
            parse_arch_one(arch, corner, corner_prev)

def add_floor(corner_array, arch_array):
    """ parse the entire floor """ 
    global floor_array
    out = []
    corner_prev = corner_array[-1]
    i = 0
    for corner in corner_array:
        if is_corner_curve(corner):
            radians = corner["wallCurve"] / 180.0 * np.pi
            corner_prev_pt = parse_corner(corner_prev)
            corner_pt = parse_corner(corner)
            curve_array, curve_length = curve.main(corner_prev_pt,corner_pt,radians)
            for cur in curve_array:
                out.append(cur)
        else:
            parse_arch(arch_array, i, parse_corner(corner), parse_corner(corner_prev))
        out.append(parse_corner(corner))
        corner_prev = corner
        i += 1
    floor_array.append(out)

def get_floor():
    """ get the entire parsed floor array """ 
    global floor_array
    return floor_array

def is_corner_curve(corner):
    """ is the corner curved? """
    is_curve = "wallIsCurved" in corner and corner["wallIsCurved"]
    safe_curve = "wallCurve" in corner and abs(corner["wallCurve"]) < 180
    return is_curve and safe_curve
                
def parse_corner(corner):
    """ Parse a single corner """ 
    return [ corner["pos"]["x"], corner["pos"]["y"] ] # all y-values reversed
    
def parse_json_room(room_array):
    """ Parse a single room """ 
    for room in room_array:
        try:
            arch_array = []
            if "architectures" in room:
                arch_array = room["architectures"]
            if "corners" in room:
                corner_array = room["corners"]
                add_floor(corner_array, arch_array)
        except:
            pass

        
def parse_json(data):
    """ Parse an entire JSON from Ensemble """ 
    global arch_array
    reset()
    if "rooms" in data:
        version_array = data["rooms"]
        supported = ["1.0.4", "1.0.7", "1.0.8" ]
        if version_array["version"] in supported and "rooms" in version_array:
                room_array = version_array["rooms"]
                parse_json_room(room_array)
        
    return get_floor(), get_window(), get_door()
     
if __name__ == '__main__':
    with open("example.json") as file:
        data = json.load(file)
        out_floor, out_window, out_door = parse_json(data)
        print(out_floor)
        print(out_wall)
        print(out_door)