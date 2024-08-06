import os
import string
import random
import shutil

pwd = os.getcwd()
scratch_folder = None

def generate_random_string(length=3):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def create_and_enter_scratch():
    global scratch_folder
    scratch_name = ".gcm_cache_"+generate_random_string()
    scratch_folder = os.path.join(pwd, scratch_name)

    os.makedirs(scratch_folder, exist_ok=True)
    os.chdir(scratch_folder)

def exit_and_delete_scratch():
    global scratch_folder
    os.chdir(pwd)
    shutil.rmtree(scratch_folder)
    scratch_folder = None

if __name__ == '__main__':

    print("Before")
    print(os.listdir(pwd))
    print("cwd: ", os.getcwd())
    print("pwd: ", pwd)
    print("scratch: ", scratch_folder)
    
    print("...........")
    create_and_enter_scratch()
    print("After")
    print(os.listdir(pwd))
    print("cwd: ", os.getcwd())
    print("pwd: ", pwd)
    print("scratch: ", scratch_folder)
    print("..............")
    exit_and_delete_scratch()
    print("After 2")
    print(os.listdir(pwd))
    print("cwd: ", os.getcwd())
    print("pwd: ", pwd)
    print("scratch: ", scratch_folder)







