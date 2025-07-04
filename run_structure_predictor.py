import argparse
import os
import sys
import hashlib
import subprocess
import time
import json
import shutil

# Helper: hash FASTA content for unique cache key
def fasta_hash(fasta_path):
    with open(fasta_path, 'rb') as f:
        content = f.read()
    return hashlib.sha256(content).hexdigest()[:16]

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def check_cached_pdb(cache_dir, protein_id, hash_id):
    pdb_path = os.path.join(cache_dir, f"{protein_id}_{hash_id}.pdb")
    log_path = os.path.join(cache_dir, f"{protein_id}_{hash_id}.log.json")
    if os.path.isfile(pdb_path):
        return pdb_path, log_path
    return None, None

def log_result(log_path, model, runtime, error=None):
    log = {
        "model_used": model,
        "runtime_sec": round(runtime, 2),
        "error": error
    }
    with open(log_path, 'w') as f:
        json.dump(log, f, indent=2)

def find_pdb_file(search_dir):
    """Recursively find the first .pdb file in search_dir."""
    for root, _, files in os.walk(search_dir):
        for fname in files:
            if fname.endswith('.pdb'):
                return os.path.join(root, fname)
    return None

def run_colabfold(fasta, out_pdb):
    # Check if colabfold_batch is available
    if shutil.which("colabfold_batch") is None:
        return False, "colabfold_batch not found in PATH. Please install ColabFold."
    tmp_outdir = os.path.dirname(out_pdb)
    cmd = ["colabfold_batch", fasta, tmp_outdir]
    try:
        proc = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pdb_found = find_pdb_file(tmp_outdir)
        if pdb_found:
            shutil.move(pdb_found, out_pdb)
            with open(out_pdb + ".colabfold.log", 'wb') as f:
                f.write(proc.stdout + b"\n" + proc.stderr)
            return True, None
        return False, "ColabFold did not produce a .pdb file."
    except Exception as e:
        return False, f"ColabFold failed: {e}"

def run_openfold(fasta, out_pdb):
    # Check if openfold_predict.py is available
    openfold_script = shutil.which("openfold_predict.py")
    if openfold_script is None:
        return False, "openfold_predict.py not found in PATH. Please install OpenFold or provide the correct script."
    tmp_outdir = os.path.dirname(out_pdb)
    cmd = [openfold_script, "--fasta", fasta, "--out", tmp_outdir]
    try:
        proc = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pdb_found = find_pdb_file(tmp_outdir)
        if pdb_found:
            shutil.move(pdb_found, out_pdb)
            with open(out_pdb + ".openfold.log", 'wb') as f:
                f.write(proc.stdout + b"\n" + proc.stderr)
            return True, None
        return False, "OpenFold did not produce a .pdb file."
    except Exception as e:
        return False, f"OpenFold failed: {e}"

def run_esmfold(fasta, out_pdb):
    # Check if esmfold.py is available
    esmfold_script = shutil.which("esmfold_predict.py")
    if esmfold_script is None:
        return False, "esmfold_predict.py not found in PATH. Please install ESMFold or provide the correct script."
    tmp_outdir = os.path.dirname(out_pdb)
    cmd = [esmfold_script, "--fasta", fasta, "--out", tmp_outdir]
    try:
        proc = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pdb_found = find_pdb_file(tmp_outdir)
        if pdb_found:
            shutil.move(pdb_found, out_pdb)
            with open(out_pdb + ".esmfold.log", 'wb') as f:
                f.write(proc.stdout + b"\n" + proc.stderr)
            return True, None
        return False, "ESMFold did not produce a .pdb file."
    except Exception as e:
        return False, f"ESMFold failed: {e}"

def main():
    parser = argparse.ArgumentParser(description="Predict 3D structure from FASTA using ColabFold/OpenFold/ESMFold with caching.")
    parser.add_argument("--protein", required=True, help="Input protein FASTA file (.fasta)")
    parser.add_argument("--output_dir", default="data/cache/structures/", help="Directory to save predicted PDB")
    parser.add_argument("--protein_id", default=None, help="Protein ID for naming (default: basename of FASTA)")
    args = parser.parse_args()

    fasta = args.protein
    if not os.path.isfile(fasta):
        print(f"[ERROR] FASTA file not found: {fasta}")
        sys.exit(1)
    ensure_dir(args.output_dir)
    hash_id = fasta_hash(fasta)
    protein_id = args.protein_id or os.path.splitext(os.path.basename(fasta))[0]
    pdb_path = os.path.join(args.output_dir, f"{protein_id}_{hash_id}.pdb")
    log_path = os.path.join(args.output_dir, f"{protein_id}_{hash_id}.log.json")

    # Caching
    if os.path.isfile(pdb_path):
        print(f"[CACHE] Structure already exists: {pdb_path}")
        print(f"[CACHE] Log: {log_path}")
        sys.exit(0)

    # Try models in order
    start = time.time()
    for model, runner in [
        ("ColabFold", run_colabfold),
        ("OpenFold", run_openfold),
        ("ESMFold", run_esmfold)
    ]:
        print(f"[INFO] Trying {model}...")
        ok, err = runner(fasta, pdb_path)
        if ok:
            elapsed = time.time() - start
            print(f"[SUCCESS] {model} prediction complete. Output: {pdb_path}")
            log_result(log_path, model, elapsed)
            sys.exit(0)
        else:
            print(f"[WARNING] {model} failed: {err}")
    # All failed
    elapsed = time.time() - start
    log_result(log_path, None, elapsed, error="All models failed.")
    print(f"[ERROR] All structure predictors failed. See log: {log_path}")
    sys.exit(2)

if __name__ == "__main__":
    main() 