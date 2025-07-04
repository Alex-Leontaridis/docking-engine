import argparse
import os
import subprocess
import sys
import time
import shutil

NEURALPLEXER_REPO = "NeuralPLexer"
INFERENCE_CLI = "neuralplexer-inference"
MODEL_CKPT = "models/complex_structure_prediction.ckpt"  # User must download

def check_neuralplexer_installed():
    if not os.path.isdir(NEURALPLEXER_REPO):
        print("[ERROR] NeuralPLexer repo not found. Please run:\n"
              "git clone https://github.com/zrqiao/NeuralPLexer.git\n"
              "cd NeuralPLexer && make environment && make install")
        sys.exit(1)
    cli_path = shutil.which(INFERENCE_CLI)
    if not cli_path:
        print(f"[ERROR] {INFERENCE_CLI} not found in PATH. Please install NeuralPLexer CLI.")
        sys.exit(1)
    return cli_path

def main():
    parser = argparse.ArgumentParser(description="NeuralPLexer pose prediction")
    parser.add_argument("--protein", required=True)
    parser.add_argument("--ligand", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    check_neuralplexer_installed()
    # Run NeuralPLexer inference
    cmd = [INFERENCE_CLI, "--protein", args.protein, "--ligand", args.ligand, "--output", args.output]
    try:
        subprocess.run(cmd, check=True)
        print(f"[NeuralPLexer] Output written to {args.output}")
    except Exception as e:
        print(f"[NeuralPLexer] Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 