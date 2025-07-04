import argparse
import os
import subprocess
import sys
import time
import logging

MODELS = [
    ("equibind", "run_equibind.py"),
    ("neuralplexer", "run_neuralplexer.py"),
    ("umol", "run_umol.py"),
]

OUTPUT_DIR = "data/output/poses"
LOG_DIR = "logs"

def ensure_dirs(model):
    os.makedirs(f"{OUTPUT_DIR}/{model}", exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(model):
    logger = logging.getLogger(model)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(f"{LOG_DIR}/pose_{model}.log")
    fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(fh)
    return logger

def run_model(model, script, protein, ligand, ligand_id, protein_id):
    ensure_dirs(model)
    logger = setup_logger(model)
    output_path = f"{OUTPUT_DIR}/{model}/{ligand_id}_{protein_id}.pdb"
    cmd = [sys.executable, script, "--protein", protein, "--ligand", ligand, "--output", output_path]
    start = time.time()
    try:
        logger.info(f"Running {model} for {ligand_id} and {protein_id}")
        subprocess.run(cmd, check=True)
        runtime = time.time() - start
        logger.info(f"Success: {output_path} (runtime: {runtime:.2f}s)")
    except Exception as e:
        logger.error(f"Failure: {e}")
        print(f"[{model}] Failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Pose prediction orchestrator (EquiBind, NeuralPLexer, UMol)")
    parser.add_argument("--protein", required=True)
    parser.add_argument("--ligand", required=True)
    parser.add_argument("--ligand_id", required=True)
    parser.add_argument("--protein_id", required=True)
    parser.add_argument("--models", nargs="*", default=[m[0] for m in MODELS], help="Models to run (default: all)")
    args = parser.parse_args()
    for model, script in MODELS:
        if model in args.models:
            run_model(model, script, args.protein, args.ligand, args.ligand_id, args.protein_id)

if __name__ == "__main__":
    main() 