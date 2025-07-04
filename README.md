# Binding & Docking Insight Engine

A comprehensive molecular docking and binding analysis pipeline that integrates multiple ML models for protein-ligand interaction prediction.

## Project Structure

```
project_root/
│
├── scripts/
│   ├── run_equibind.py              # EquiBind pose prediction
│   ├── run_neuralplexer.py          # NeuralPLexer pose prediction
│   ├── run_umol.py                  # UMol pose prediction (structure-free)
│   ├── run_structure_predictor.py   # Multi-model structure prediction
│   ├── run_boltz2.py                # Binding affinity estimation
│   ├── extract_interactions.py      # Molecular interaction analysis
│   ├── run_druggability.py          # Binding site druggability scoring
│   ├── model_consensus.py           # Pose consensus scoring
│   ├── compute_confidence.py        # Composite confidence scoring
│   └── parse_and_score_results.py   # Output consolidation
│
├── models/
│   └── pretrained/                  # Downloaded/converted ML models
│
├── data/
│   ├── input/                       # Protein + Ligand files (.pdb, .mol2, .smi, .fasta)
│   ├── output/                      # All result files (poses, JSON, CSV)
│   └── cache/                       # Cached structure predictions
│
├── examples/
│   └── example1/                    # Sample protein-ligand run
│
├── README.md
└── requirements.txt
```

## Features

### 1. Pose Prediction
- **EquiBind**: Structure-based pose prediction
- **NeuralPLexer**: Advanced neural network-based docking
- **UMol**: Structure-free pose prediction

### 2. Binding Affinity Estimation
- **Boltz2**: State-of-the-art binding energy prediction
- Fallback mechanisms for robustness

### 3. Structure Prediction
- **ColabFold**: AlphaFold2-based structure prediction
- **OpenFold**: Open-source AlphaFold2 implementation
- **ESMFold**: Meta's protein structure prediction
- Intelligent caching system

### 4. Interaction Analysis
- **PLIP**: Protein-ligand interaction profiler
- **RDKit**: Chemical informatics fallback
- H-bonds, π-π interactions, van der Waals contacts

### 5. Druggability Scoring
- **fpocket**: Binding site druggability analysis
- Multi-parameter scoring algorithm
- Mock fallback for testing

### 6. Consensus & Confidence Engine
- **RMSD-based clustering**: Pose agreement analysis
- **Composite scoring**: Weighted confidence metrics
- **Ligand efficiency**: LE, SILE, LLE calculations

### 7. Output Formatter
- **CSV summary**: Tabular results for analysis
- **JSON details**: Complete data for downstream processing
- **Standardized format**: Consistent across all outputs

## Requirements

```bash
pip install -r requirements.txt
```

### Core Dependencies
- Python 3.8+
- BioPython
- NumPy
- SciPy
- scikit-learn
- RDKit

### External Tools (Optional)
- fpocket (for druggability analysis)
- ColabFold (for structure prediction)
- OpenFold (for structure prediction)

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd docking-engine
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install external tools (optional):**
```bash
# Ubuntu/Debian
sudo apt-get install fpocket

# macOS
brew install fpocket

# Conda
conda install -c conda-forge fpocket
```

## Usage

### Individual Scripts

#### 1. Pose Prediction
```bash
# EquiBind
python scripts/run_equibind.py --protein data/input/protein.pdb --ligand data/input/ligand.sdf --output data/output/equibind_pose.pdb

# NeuralPLexer
python scripts/run_neuralplexer.py --protein data/input/protein.pdb --ligand data/input/ligand.sdf --output data/output/neuralplexer_pose.pdb

# UMol
python scripts/run_umol.py --protein data/input/protein.pdb --ligand data/input/ligand.sdf --output data/output/umol_pose.pdb
```

#### 2. Structure Prediction
```bash
python scripts/run_structure_predictor.py --protein data/input/protein.fasta --output_dir data/cache/structures/
```

#### 3. Binding Affinity
```bash
python scripts/run_boltz2.py --protein data/input/protein.fasta --ligand data/input/ligand.smi --output data/output/affinity.json
```

#### 4. Interaction Analysis
```bash
python scripts/extract_interactions.py --pdb data/output/pose.pdb --ligand LIG --protein PROT --output_dir data/output/interactions/
```

#### 5. Druggability Scoring
```bash
python scripts/run_druggability.py --protein data/output/pose.pdb --output data/output/druggability.json
```

#### 6. Consensus Analysis
```bash
python scripts/model_consensus.py --poses data/output/equibind_pose.pdb data/output/neuralplexer_pose.pdb data/output/umol_pose.pdb --output data/output/consensus.json --ligand_id LIG1
```

#### 7. Confidence Scoring
```bash
python scripts/compute_confidence.py --consensus_json data/output/consensus.json --druggability_json data/output/druggability.json --affinity_json data/output/affinity.json --interaction_json data/output/interactions/LIG_PROT.json --output data/output/confidence.json --ligand_id LIG1
```

#### 8. Output Consolidation
```bash
python scripts/parse_and_score_results.py --input_dir data/output/ --output_csv data/output/final_summary.csv --output_json data/output/summary.json
```

### Complete Pipeline Example

```bash
# 1. Structure prediction (if needed)
python scripts/run_structure_predictor.py --protein data/input/protein.fasta --output_dir data/cache/structures/

# 2. Pose predictions
python scripts/run_equibind.py --protein data/cache/structures/protein.pdb --ligand data/input/ligand.sdf --output data/output/equibind_pose.pdb
python scripts/run_neuralplexer.py --protein data/cache/structures/protein.pdb --ligand data/input/ligand.sdf --output data/output/neuralplexer_pose.pdb
python scripts/run_umol.py --protein data/cache/structures/protein.pdb --ligand data/input/ligand.sdf --output data/output/umol_pose.pdb

# 3. Binding affinity
python scripts/run_boltz2.py --protein data/input/protein.fasta --ligand data/input/ligand.smi --output data/output/affinity.json

# 4. Interaction analysis
python scripts/extract_interactions.py --pdb data/output/equibind_pose.pdb --ligand LIG --protein PROT --output_dir data/output/interactions/

# 5. Druggability scoring
python scripts/run_druggability.py --protein data/output/equibind_pose.pdb --output data/output/druggability.json

# 6. Consensus analysis
python scripts/model_consensus.py --poses data/output/equibind_pose.pdb data/output/neuralplexer_pose.pdb data/output/umol_pose.pdb --output data/output/consensus.json --ligand_id LIG1

# 7. Confidence scoring
python scripts/compute_confidence.py --consensus_json data/output/consensus.json --druggability_json data/output/druggability.json --affinity_json data/output/affinity.json --interaction_json data/output/interactions/LIG_PROT.json --output data/output/confidence.json --ligand_id LIG1

# 8. Final summary
python scripts/parse_and_score_results.py --input_dir data/output/ --output_csv data/output/final_summary.csv --output_json data/output/summary.json
```

## Output Formats

### CSV Summary (`final_summary.csv`)
```csv
ligand_id,confidence_score,consensus_score,druggability_score,affinity_kcal_per_mol,LE,model_voting,mean_rmsd,num_clusters,h_bonds,pi_pi,vdW,structure_source
LIG1,85,0.8,0.75,-8.5,0.34,0.8,1.2,2,"ASP155;ARG198","TRP156","LEU83;VAL91",data/input/protein.fasta
```

### JSON Summary (`summary.json`)
```json
{
  "LIG1": {
    "ligand_id": "LIG1",
    "confidence_score": 85,
    "consensus_score": 0.8,
    "druggability_score": 0.75,
    "affinity_kcal_per_mol": -8.5,
    "LE": 0.34,
    "model_voting": 0.8,
    "mean_rmsd": 1.2,
    "num_clusters": 2,
    "h_bonds": ["ASP155", "ARG198"],
    "pi_pi": ["TRP156"],
    "vdW": ["LEU83", "VAL91"],
    "structure_source": "data/input/protein.fasta",
    "summary": {
      "confidence": {...},
      "consensus": {...},
      "druggability": {...},
      "affinity": {...},
      "interaction": {...}
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **External tool not found:**
   - Scripts include fallback mechanisms
   - Install missing tools or use `--force_mock` flag

2. **Memory issues:**
   - Reduce batch sizes
   - Use CPU-only mode where available

3. **File format errors:**
   - Ensure input files are in correct format
   - Check file permissions

### Getting Help

- Check script help: `python scripts/script_name.py --help`
- Review log files in `logs/` directory
- Ensure all dependencies are installed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **EquiBind**: Authors of the EquiBind model
- **NeuralPLexer**: NeuralPLexer development team
- **UMol**: UMol research group
- **Boltz2**: Boltz2 developers
- **ColabFold**: ColabFold team
- **OpenFold**: OpenFold contributors
- **ESMFold**: Meta AI Research
- **fpocket**: fpocket development team
- **PLIP**: PLIP authors
- **RDKit**: RDKit contributors 