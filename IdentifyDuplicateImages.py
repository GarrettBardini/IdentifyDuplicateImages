###############################################################
#####     IDENTIFY DUPLICATE IMAGES                       #####
#####     AUTHOR: GARRETT PETER BARDINI (GPB)             #####
#####     CREATE_DATE: 2022/09/15                         #####
#####     LAST_MODIFIED: 2022/09/22                       #####
###############################################################
# FIX HOW YOU NAME YOUR VARS # 
import os
import time
import hashlib
import cv2
import shutil
from imageio.v2 import imread
import matplotlib.pyplot as plt
### USER INPUT | FOLDERS TO IDENTIFY DUPLICATES IN ### 
FolderList= []
Path = input('Input a Folder Path with images you would like to check for duplicates: ')
FolderList.append(Path) 
while Path != '': 
    Path = input('Input an additional Folder Path with images you would like to check for duplicates OR press ENTER to Continue: ') 
    if Path == '':
        continue 
    FolderList.append(Path)
### USER INPUT | PATH TO MOVE DUPLICATES TO ### 
DupPath = input('Input a Path for the duplicates to be moved to: ') 
if not os.path.exists(DupPath): # Remove This before start 
    os.makedirs(DupPath)
### IDENTIFY DUPLICATES ### 
start_time = time.time()
duplicates = []
hash_keys = dict()
for folder in FolderList:
    for dir_, _, files in os.walk(folder):
        for file_name in files:
            file_path = os.path.join(dir_, file_name)
            try:
                image = cv2.imread(file_path)
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                histogram = cv2.calcHist([gray_image], [0],None, [256], [0, 256])
                filehash = hashlib.md5(histogram).hexdigest()
                if filehash not in hash_keys.values(): 
                    hash_keys[file_name] = filehash
                else:
                    duplicates.append((file_path)) 
                    print(f"Duplicate Detected: {file_path}") # store this as a log? 
                    # plt.plot(121),plt.imshow(imread(os.path.join(Folder,filename))) # prompt the user of they want these plots ? 
                    # plt.title(os.path.join(Folder,filename)), plt.xticks([]), plt.yticks([]) # I dont really like this slows things down 
                    # plt.show() # I want to make life easier 
                    shutil.move(file_path,os.path.join(DupPath,file_name)) # MOVE DUPLICATES TO THE SPECIFIED FOLDER 
            except:
                continue

for folder in FolderList:
    for path, _, _ in os.walk(folder, topdown=False):
        if len(os.listdir(path)) == 0:
            print(f"Removing Folder: {path}")
            os.rmdir(path)

execution_time = (time.time() - start_time)
print('Executed in: ' + execution_time + '  seconds.') 