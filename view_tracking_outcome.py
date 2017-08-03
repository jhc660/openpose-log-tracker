import numpy as np
import string
import cv2
import math
import json

def main():
    number = 0
    while True:
        name = "video_"+str("%012d" % (number,))+"_pose_keypoints.json"
        try:
            json_data=open(name).read()
            data = json.loads(json_data)

            img = cv2.imread("video/"+str("%05d" % (number+1,))+".jpg")

            for person in data["people"]:
                x_values = person["pose_keypoints"][0::3]
                y_values = person["pose_keypoints"][1::3]
                x_values = np.array( [ num for num in x_values if num > 0 ] )
                y_values = np.array( [ num for num in y_values if num > 0 ] )

                x_lower = int(np.amin(x_values))
                x_higher = int(np.amax(x_values))
                y_lower = int(np.amin(y_values))
                y_higher = int(np.amax(y_values))
                
                cv2.rectangle(img,(x_lower,y_lower),(x_higher,y_higher),(0,255,0),2)
                
                cv2.putText(img, "ID: "+str(person["id"]),(x_lower,y_lower), 0, 1, (255, 255, 255), 3)

                cv2.putText(img, "ID: "+str(person["id"]),(x_lower,y_lower), 0, 1, (0,0,0), 2)
            cv2.imshow('image',img)
            key = cv2.waitKey(0)
            if key == 27:
                break
            elif key == 100:
                number -= 2
                print(number)    
            cv2.destroyAllWindows()    
        except FileNotFoundError:
            print("finished")
            break
        number += 1
    
if __name__ == "__main__":
    main()
