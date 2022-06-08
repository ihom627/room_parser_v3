import os
import json
import products
import rooms
import triangulate

def main(path):
    with open(path) as file_in:
        data = json.load(file_in)
        prod_array = products.parse_json(data)
        room_array, window_array, door_array = rooms.parse_json(data)
        
        room_dictionary = {}
        for prod in prod_array:
            brand = prod["brand"]
            sku = prod["sku"]
            
            # IGNORE NON-FURNITURE
            if prod["fabric"] != "missing" and prod["width"] and prod["depth"]:
                pos = prod["pos"][:2]
                rot = prod["rot"]
                width = prod["width"]
                depth = prod["depth"]
                if pos[0] == None or pos[1] == None:
                    continue
                    
                # FIND THE ROOM NUMBER
                tris_best, index_best = triangulate.models_inside_best(pos, room_array)
                if index_best != -1:
                    room_id = index_best

                    if room_id not in room_dictionary:  
                        room_dictionary[room_id] = []
                        
                    room_dictionary[room_id].append([brand,sku, pos[0], pos[1], rot, width, depth])
        
        # ADD WINDOWS
        for window in window_array:
            room_id = window["room_id"]
            pos = window["pos"]
            length = window["length"]
            
            if room_id not in room_dictionary:  
                room_dictionary[room_id] = []
                
            room_dictionary[room_id].append(["arch", "window", pos[0], pos[1], length])
        
        # ADD DOORS
        for door in door_array:
            room_id = door["room_id"]
            pos = door["pos"]
            length = door["length"]
            
            if room_id not in room_dictionary:  
                room_dictionary[room_id] = []
                
            room_dictionary[room_id].append(["arch", "door", pos[0], pos[1], length])
        
        with open(path.replace(".json","-out.json"),"w") as file_out:
            json.dump(room_dictionary, file_out, sort_keys=True, indent=4, separators=(',', ': '))

if __name__ == '__main__':
#    main("example.json")
    main("121045.json")
            
            
