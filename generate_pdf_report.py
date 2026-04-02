from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from poisson_decay.poisson_utils import load_config
from poisson_decay.report import build_report


if __name__ == "__main__":
    cfg = load_config("config.json")
    build_report(Path("config.json"), cfg["defaults"]["mode"])
