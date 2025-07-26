#from textnode import *
import os
import shutil

LOG_FILE = "static.log"

def copy_dir(dir, log=None):
    dst = dir.replace("static", "public", 1)
    if log:
        log.write(f"mkdir {dst}\n")
    os.mkdir(f"{dst}")
    for i in os.listdir(dir):
        i_path = f"{dir}/{i}"
        if os.path.isfile(i_path):
            if log:
                log.write(f"cp {i_path} to {dst}\n")
            shutil.copy(i_path, f"{dst}")
        else:
            copy_dir(i_path, log)

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    with open(LOG_FILE, 'w') as f:
        copy_dir("static", f)

if __name__ == "__main__":
    main()
