import os

path = 'C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/Melodify.ico/images'

# check whether directory already exists
if not os.path.exists(path):
    os.makedirs(path)
    print("Folder %s created!" % path)
else:
    print("Folder %s already exists" % path)
