import os
import logging
logging.basicConfig(level=logging.INFO)

# Make a folder structure
folders=[
    os.path.join("Data","raw"),
    os.path.join("Data","process"),
    os.path.join("src","components"),
    os.path.join("src","model-training"),    
]

for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder,exist_ok=True)

        # Now make a git keefile inside the each folder
        git_keep=os.path.join(folder,".gitkeep")
        with open(git_keep,"w")as f:
            pass

    else:
        logging.info(f"{folder} already present")


# Now inject the files for each folder
folder_files=[
    os.path.join("src","__init__.py"),
    os.path.join("src","utils.py"),
    os.path.join("src/components","__init__.py"),
    os.path.join("src/components","data_loader.py"),
    os.path.join("src/components","data_processor.py"),
    os.path.join("src/components","data_visulization.py"),
    os.path.join("src/components","feature_engnering.py"),
    "setup.py",
    "test_environment.py",
    "requirements.txt",
    "app.py"
]

for file in folder_files:
    if not os.path.exists(file) or os.path.getsize(file) == 0:
        with open(file,"w") as f:
            pass
        logging.info(f"{file} created successfully")
    else:
        logging.info(f"{file} already present")