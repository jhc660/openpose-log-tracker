import json
import glob
import numpy as np
import math
import CenterOfMassDifference as cmd

def get_threshold():
    return 50

def get_width():
    return 1280

def get_height():
    return 720

def main():
    number = 0
    ids_issued = 0
    while True:
        #Formulate name of next data frame file
        name = "video_"+str("%012d" % (number,))+"_keypoints.json"
        print(name)
    
        #Attempt to open next data frame data.
        try:
            with open(name) as data_file:    
                output_file  = open("video_"+str("%012d" % (number,))+"_pose_keypoints.json", 'w')
                if not number == 0:
                    prev_data = cur_data

                cur_data = json.load(data_file)

                if number == 0:
                    cur_data["people"], ids_issued = initialize_ids(cur_data["people"], ids_issued)
                else:
                    cur_data["people"], ids_issued = compare_people(cur_data["people"], prev_data["people"], ids_issued)
                
                json.dump(cur_data, output_file, indent = 6)

        except FileNotFoundError:
            print("finished")
            break
        
        output_file.close()
        number+=1

def compare_people(current, previous, ids_issued): 
    difference_mat = np.zeros((len(current),len(previous)))

    for x in range(len(current)):
        for y in range(len(previous)):
            difference_mat[x][y] = cmd.com_difference(current[x]["pose_keypoints"],previous[y]["pose_keypoints"],get_threshold())

    for y in range(len(previous)):
        choose_best_candidate(y , difference_mat, current, previous)

    for x in range(len(current)):
        if not ("id" in current[x]):
            current[x]["id"] = ids_issued
            ids_issued+=1
    return current, ids_issued

def choose_best_candidate(candidate, matrix, current, previous):
    minimum_index = np.argmin(matrix[:,candidate])
    if (matrix[minimum_index][candidate] < get_threshold()):
        if "id" in current[minimum_index]:
            matrix[minimum_index] = get_threshold()
            choose_best_candidate(candidate, matrix, current, previous)
        else:
            current[minimum_index]["id"] = previous[candidate]["id"]


def initialize_ids(current, ids_issued):
    for x in range(len(current)):
        current[x]["id"] = ids_issued
        ids_issued += 1
    return current, ids_issued

if __name__ == "__main__":
    main()
