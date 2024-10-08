import sys
import subprocess
from pathlib import Path

# def run_module():
#     try:
#         subprocess.run(["./a.out", "2", "2", "2", "12345", "1.0", "karate.txt"], timeout = 10, check=True)
#     except FileNotFoundError as exc:
#         print(f"Process failed because the executable could not be found.\n{exc}")
#     except subprocess.CalledProcessError as exc:
#         print(
#             f"Process failed because did not return a successful return code. "
#             f"Returned {exc.returncode}:\\\\ {exc}"
#         )
#     except subprocess.TimeoutExpired as exc:
#         print(f"Process timed out.\n{exc}")
    
import os
import shutil
import argparse
import random
import string
from contextlib import contextmanager

def generate_random_string(length=4):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

@contextmanager
def subprocess_context():
    # import pdb; pdb.set_trace()
    try:
        yield
    except FileNotFoundError as exc:
        print(f"Process failed because the executable could not be found.\n{exc}")
    except subprocess.CalledProcessError as exc:
        print(
            f"Process failed because did not return a successful return code. "
            f"Returned {exc.returncode}:\\\\ {exc}"
        )
    except subprocess.TimeoutExpired as exc:
        print(f"Process timed out.\n{exc}")



def run_work_script(filename):
    """Run the work.sh script with a file."""
    # import pdb; pdb.set_trace()
    source_path = Path(__file__).resolve()
    source_dir = source_path.parent
    path_to_exec  = os.path.join(source_dir, "work.sh")
    with subprocess_context():
        subprocess.run(['bash', path_to_exec, filename], check=True)

def run_format_script(filename, sep = None):
    "Run the format_edgelist.py script"
    if sep is None:
        sep = "space"

    source_path = Path(__file__).resolve()
    source_dir = source_path.parent
    path_to_exec  = os.path.join(source_dir, "format_edgelist.py")
    with subprocess_context():
        subprocess.run(["python", path_to_exec, filename, "--sep", "comma"])
    filepath_orig = Path(filename)
    return str(filepath_orig.with_stem(filepath_orig.stem + "_formatted")),str(filepath_orig.with_stem(filepath_orig.stem + "_key"))

def remap_partition_results(keyfile, formatted_file):
    result_filename = f'partition_{os.path.basename(formatted_file)}'
    partitions = {}
    mappings = {}
    with open(result_filename, 'r') as f:
        i = 0
        for line in f:
            i+=1
            partitions[i] = int(line.strip())
    
    with open(keyfile, 'r') as f:
        for line in f:
            a, b = line.split()
            a, b = int(a), int(b)
            mappings[b] = a

    with open(result_filename, 'w') as f:
        for k, v in partitions.items():
            print(f'{mappings[k]} {v}', file=f)


def _setup_and_enter_scratch(initial_working_directory, input_file):
    scratch_directory = os.path.join(initial_working_directory, f"gcm_cache_{generate_random_string()}")
    os.makedirs(scratch_directory)
    scratch_file = os.path.join(scratch_directory, os.path.basename(input_file))
    shutil.copy(input_file, scratch_file)
    os.chdir(scratch_directory)
    return scratch_directory, scratch_file

def _exit_and_cleanup_scratch(output_dir, output_file, initial_working_dir,  scratch_directory, formatted_file):
    result_filename = f'partition_{os.path.basename(formatted_file)}'
    output_filepath = os.path.join(output_dir, output_file)
    result_filepath = os.path.join(scratch_directory, result_filename)
    if os.path.exists(result_filepath):
        shutil.copy(result_filepath, output_filepath)
    else:
        print("Error encountered, no result exists")

    os.chdir(initial_working_dir)
    if os.path.exists(scratch_directory):
        shutil.rmtree(scratch_directory)

def run_clustering(filename, chi = 0.0, seed = 12345):
    source_path = Path(__file__).resolve()
    source_dir = source_path.parent
    
    with subprocess_context():
        subprocess.run([f'{source_dir}/a.out', "2", "5", "2", f"{seed}", f"{chi}", filename], check = True)

def gcm(input_file, chi = 0.0, seed = 12345, output_dir = None, output_file = None, return_df = False):
    initial_working_directory  = os.getcwd()
    if output_dir is None:
        output_dir = initial_working_directory
    
    if output_file is None:
        output_file = "clustering_output.txt"
    try:
        scratch_directory, scratch_file = _setup_and_enter_scratch(initial_working_directory, input_file)
        formatted_file, key_file = run_format_script(os.path.basename(scratch_file))
        run_work_script(os.path.basename(formatted_file))
        run_clustering(os.path.basename(formatted_file), chi, seed)
        remap_partition_results(key_file, formatted_file)
    finally:
        _exit_and_cleanup_scratch(output_dir, output_file, initial_working_directory, scratch_directory, formatted_file)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process an input file, run a script, and handle output.')
    parser.add_argument('input_file', type=str, help='Input file name, e.g., file_name.txt')
    parser.add_argument('--output_dir', type=str, help='Directory to save the output file', default = None, required= False)
    parser.add_argument('--output_file', type=str, help='Filename for the output file', default= None, required= False)
    parser.add_argument('--seed', type=int, help='Random seed for GCM', default = 12345)
    parser.add_argument('--chi', type=float, help = 'Value of Chi', default = 0.0)
    parser.add_argument('--sep', type=str, help = 'Value of sep for formatting', default = None)
    args = parser.parse_args()
    gcm(args.input_file, args.chi, args.seed, args.output_dir, args.output_file)

# python test_ground/run_gcm.py "/Users/pranjalsrivastava/Work/RA work/karate.txt" "/Users/pranjalsrivastava/Work/RA work" information.txt

# darts-balloon game - Outcome: direction to game room
# game room - projector - Outcome: code, golf stick, follow sound
# sound - sandook - golf ball, golf head

