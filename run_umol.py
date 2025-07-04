import argparse
import os
import subprocess
import sys
import time
import shutil

UMOL_REPO = "Umol"
PREDICT_SCRIPT = "predict.sh"

def check_umol_installed():
    if not os.path.isdir(UMOL_REPO):
        print("[ERROR] UMol repo not found. Please run:\n"
              "git clone https://github.com/patrickbryant1/Umol.git\n"
              "cd Umol && bash install_dependencies.sh")
        sys.exit(1)
    script_path = os.path.join(UMOL_REPO, PREDICT_SCRIPT)
    if not os.path.isfile(script_path):
        print(f"[ERROR] {PREDICT_SCRIPT} not found in {UMOL_REPO}.")
        sys.exit(1)
    return script_path

def main():
    parser = argparse.ArgumentParser(description="UMol pose prediction")
    parser.add_argument("--protein", required=True)
    parser.add_argument("--ligand", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    check_umol_installed()
    # Run UMol prediction
    cmd = ["bash", os.path.join(UMOL_REPO, PREDICT_SCRIPT), args.protein, args.ligand, args.output]
    try:
        subprocess.run(cmd, check=True)
        print(f"[UMol] Output written to {args.output}")
    except Exception as e:
        print(f"[UMol] Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 