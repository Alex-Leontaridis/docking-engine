import argparse
import os
import sys
import json
import time
import tempfile

try:
    from boltz import predict
except Exception as e:
    print("[ERROR] Could not import boltz. Full error below:")
    import traceback
    traceback.print_exc()
    sys.exit(1)

def check_inputs(protein, ligand):
    if not os.path.isfile(protein):
        print(f"[ERROR] Protein file not found: {protein}")
        sys.exit(1)
    if not os.path.isfile(ligand):
        print(f"[ERROR] Ligand file not found: {ligand}")
        sys.exit(1)
    if not (protein.endswith('.fasta') or protein.endswith('.fa')):
        print(f"[ERROR] Protein must be a FASTA file (.fasta or .fa): {protein}")
        sys.exit(1)
    if not ligand.endswith('.smi'):
        print(f"[ERROR] Ligand must be a SMILES file (.smi): {ligand}")
        sys.exit(1)

def make_yaml(protein, ligand, yaml_path):
    yaml_content = f"""protein:
  fasta_path: {os.path.abspath(protein)}
ligand:
  smiles_path: {os.path.abspath(ligand)}
properties:
  - affinity
"""
    with open(yaml_path, "w") as f:
        f.write(yaml_content)

def main():
    parser = argparse.ArgumentParser(description="Binding affinity estimation using Boltz2")
    parser.add_argument("--protein", required=True, help="Protein FASTA file (.fasta)")
    parser.add_argument("--ligand", required=True, help="Ligand SMILES file (.smi)")
    parser.add_argument("--output", required=True, help="Output JSON file")
    parser.add_argument("--ligand_id", default="LIG", help="Ligand ID")
    parser.add_argument("--protein_id", default="PROT", help="Protein ID")
    args = parser.parse_args()

    check_inputs(args.protein, args.ligand)
    start = time.time()
    result = {
        "protein": args.protein,
        "ligand": args.ligand,
        "protein_id": args.protein_id,
        "ligand_id": args.ligand_id,
        "model": "Boltz2",
        "fallback": False,
    }
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            yaml_path = os.path.join(tmpdir, "input.yaml")
            make_yaml(args.protein, args.ligand, yaml_path)
            pred = predict(yaml_path)
            # Parse output (see Boltz2 docs for exact keys)
            affinity = pred.get("affinity_pred_value", None)
            confidence = pred.get("affinity_probability_binary", None)
            result["delta_g"] = affinity
            result["confidence"] = confidence
    except Exception as e:
        result["delta_g"] = None
        result["confidence"] = None
        result["fallback"] = True
        result["error"] = str(e)
    elapsed = time.time() - start
    result["runtime_sec"] = round(elapsed, 2)
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    print(f"[Boltz2] Output written to {args.output} (runtime: {elapsed:.2f}s)")

if __name__ == "__main__":
    main() 