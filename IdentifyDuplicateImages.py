###############################################################
#####     IDENTIFY DUPLICATE IMAGES                       #####
#####     AUTHOR: GARRETT PETER BARDINI (GPB)             #####
#####     CREATE_DATE: 2022/09/15                         #####
#####     LAST_MODIFIED: 2022/09/15                       #####
###############################################################
import hashlib, os
import cv2
import shutil
from imageio.v2 import imread
import matplotlib.pyplot as plt
### USER INPUT | FOLDERS TO IDENTIFY DUPLICATES IN ### 
FolderList= []
Path = input('Input a Folder Path with images you would like to check for duplicates: ')
FolderList.append(Path) 
while Path != '': 
    Path = input('Input an additional Folder Path with images you would like to check for duplicates: ') 
    if Path == '':
        continue 
    FolderList.append(Path)
### USER INPUT | PATH TO MOVE DUPLICATES TO ### 
DupPath = input('Input a Path for the duplicates to moved to: ') 
if not os.path.exists(DupPath): # Remove This before start 
    os.makedirs(DupPath)
### IDENTIFY DUPLICATES ### 
duplicates = []
hash_keys = dict()
for Folder in FolderList:
    os.chdir(Folder)
    for index, filename in  enumerate(os.listdir('.')):
        if os.path.isfile(filename):
            try:
                image = cv2.imread(filename)
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                histogram = cv2.calcHist([gray_image], [0],None, [256], [0, 256])
                filehash = hashlib.md5(histogram).hexdigest()
                if filehash not in hash_keys: 
                    hash_keys[filehash] = index 
                else:
                    duplicates.append((index,hash_keys[filehash])) 
                    print(f"Duplicate Detected: {os.path.join(Folder,filename)}") # store this as a log? 
                    # plt.plot(121),plt.imshow(imread(os.path.join(Folder,filename))) # prompt the user of they want these plots ? 
                    # plt.title(os.path.join(Folder,filename)), plt.xticks([]), plt.yticks([]) # I dont really like this slows things down 
                    # plt.show() # I want to make life easier 
                    shutil.move(os.path.join(Folder,filename),os.path.join(DupPath,filename)) # MOVE DUPLICATES TO THE SPECIFIED FOLDER 
            except:
                continue