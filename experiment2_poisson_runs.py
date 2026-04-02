from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from poisson_decay.experiment2 import run_experiment2
from poisson_decay.poisson_utils import load_config


if __name__ == "__main__":
    cfg = load_config("config.json")
    run_experiment2(Path(cfg["defaults"]["data_path"]), Path(cfg["defaults"]["output_dir"]), Path("config.json"), cfg["defaults"]["mode"])
