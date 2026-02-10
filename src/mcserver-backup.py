from os import rmdir
from pathlib import Path
import argparse
from datetime import datetime
from subprocess import run
import time
from shutil import copytree, rmtree 
from uuid import uuid4

# Main logic of the code 
def main():
    # Parse the argument from the command line
    parser = argparse.ArgumentParser(prog = 'backup_script', description='* A script that compress using xz -9e and backup the minecraft server directory, run periodically using cron or systemd timer\n* Example usage: python3 mcserver-backup.py ~/server_dir /mnt/backup_dir')
    parser.add_argument('source', help='The source directory')
    parser.add_argument('destination', help='the destination directory that you want to save the compressed backup file')

    args = parser.parse_args() # Place data inside the namespace args

    # Put source and dest as Path object instead of string ==> easier to work with later on using pathlib. expanduser() and resolve() solve problems with ~ and relatiev path
    source = Path(args.source).expanduser().resolve()
    dest = Path(args.destination).expanduser().resolve() 

    # Add in time and date 
    current_time = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    backup_filename = dest / f"mc_backup_{current_time}.tar.xz"
    
    # pause_server()
    copy_dst = copy_world(source)
    # resume_server()
    compress_backup(copy_dst, backup_filename)
    rmtree(copy_dst) 

def pause_server():
    # Tell minecraft to stop writing to disk
    run(["tmux", "send-keys", "-t", "MC", "save-off", "Enter"])

    # Tell minecraft to finish saving the content to disk
    run(["tmux", "send-keys", "-t", "MC", "save-all", "Enter"])
    time.sleep(120)

# TESTED for the copy part, hasn't tested for the error handling part
def copy_world(copy_src):
    last_error = None
    
    for attempt in range(3):

        # Create a tmp dierctory using an unique ID each time the code retry or run
        snapshot_id = uuid4().hex
        copy_dst = Path(f"/tmp/mcServerCopyTemp_{snapshot_id}/") 
        try:
            copytree(copy_src, copy_dst)
            return copy_dst

        # Raise an exception if copytree fail, and follow up with clean up and retry
        except Exception as e:
            # Check if the directory dst exist or not. If yes, then delete it here
            if copy_dst.exists():
                rmtree(copy_dst)
            last_error = e
            # Will use a dedicated log module later on
            print("Attempt fail, retry")

    raise RuntimeError("Failed to copy world") from last_error

def resume_server():
    run(["tmux", "send-keys", "-t", "MC", "save-on", "Enter"])

# It is a live backup so I think I will remove the compression program thing, as it will use all the available threads and leave none for the minecraft server. One or two threads for this should be sufficient
# TESTED (very basic test case, but it works), but if you can come up with some more test cases, please test this function more thoroughly
def compress_backup(compress_src, compress_dst):
    run(["tar", "-cJf", compress_dst, "--exclude=./logs", "--exclude=./cache", "--exclude=./libraries", f"--directory={compress_src}", "."])

def cleanup_temp(temp_dst):
    rmtree(temp_dst) 

def rotation():
    pass


# Execute the code 
if __name__=="__main__":
    main() 
