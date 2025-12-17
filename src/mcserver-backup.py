#!/usr/bin/python3
from pathlib import Path
import argparse
from datetime import datetime
from subprocess import run
import time
from shutil import copytree, rmtree, Error
import random

# main logic of the code 
def main():
    # Parse the argument from the command line
    parser = argparse.ArgumentParser(prog = 'backup_script', description='A script that compress using xz -9e and backup the minecraft server directory, run periodically using cron')
    parser.add_argument('source', help='The source directory')
    parser.add_argument('destination', help='the destination directory that you want to save the compressed backup file')

    args = parser.parse_args() # Place data inside the namespace args

    # Put source and dest as Path object instead of string ==> easier to work with later on using pathlib. expanduser() and resolve() solve problems with ~ and relatiev path
    source = Path(args.source).expanduser().resolve()
    dest = Path(args.destination).expanduser().resolve() 

    # Add in time and date 
    time = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    backup_filename = dest / f"mc_backup_{time}.tar.xz"
    print(backup_filename)

def pause_server():
    run(["tmux", "send-keys", "-t", "MC", "save-off", "Enter"])
    run(["tmux", "send-keys", "-t", "MC", "save-all", "Enter"])
    time.sleep(120)

def copy_world(src):
    # Use random for now, but will move to an ID base system later on, as random format is confusing and ugly
    random_num = random.random()
    dst = Path(f"/tmp/mcServerCopyTemp{random_num}/") 
    last_error = None
    
    for attempt in range(3):
        try:
            copytree(src, dst)
            return dst
        except Exception as e:
            last_error = e
            # Will use a dedicated log module later on
            print("Attempt fail, retry")

    raise RuntimeError("Failed to copy world") from last_error

def resume_server():
    run(["tmux", "send-keys", "-t", "MC", "save-on", "Enter"])

def compress_backup(src, dst):
    run(["tar", "-cf", "--use-compress-program = 'pixz -9e'"])

def cleanup_temp(dst):
    rmtree(dst) 



# Execute the code 
if __name__=="__main__":
    main()
