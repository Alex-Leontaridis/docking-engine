import argparse
import os
import subprocess
import sys
import time
import shutil

EQUIBIND_REPO = "EquiBind"
INFERENCE_SCRIPT = "inference.py"
CONFIG_PATH = "configs_clean/inference.yml"

def check_equibind_installed():
    if not os.path.isdir(EQUIBIND_REPO):
        print("[ERROR] EquiBind repo not found. Please run:\n"
              "git clone https://github.com/HannesStark/EquiBind.git\n"
              "cd EquiBind && conda env create -f environment.yml && conda activate equibind")
        sys.exit(1)
    if not os.path.isfile(os.path.join(EQUIBIND_REPO, INFERENCE_SCRIPT)):
        print(f"[ERROR] {INFERENCE_SCRIPT} not found in {EQUIBIND_REPO}.")
        sys.exit(1)
    return os.path.join(EQUIBIND_REPO, INFERENCE_SCRIPT)

def main():
    parser = argparse.ArgumentParser(description="EquiBind pose prediction")
    parser.add_argument("--protein", required=True)
    parser.add_argument("--ligand", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    check_equibind_installed()
    # Prepare input/output as needed by EquiBind
    # (Assume input files are already in correct format)
    # Run EquiBind inference
    cmd = [sys.executable, os.path.join(EQUIBIND_REPO, INFERENCE_SCRIPT),
           "--protein", args.protein, "--ligand", args.ligand, "--output", args.output]
    try:
        subprocess.run(cmd, check=True)
        print(f"[EquiBind] Output written to {args.output}")
    except Exception as e:
        print(f"[EquiBind] Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 