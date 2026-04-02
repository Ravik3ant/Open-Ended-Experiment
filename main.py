import json
import subprocess
import sys
from pathlib import Path

from experiment1_poisson_runs import run_experiment1
from experiment2_poisson_runs import run_experiment2
from generate_pdf_report import main as build_report
from poisson_utils import load_config


CONFIG_PATH = Path("config.json")


def save_config(cfg: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)


def start_pipeline():
    cfg = load_config(CONFIG_PATH)
    data_path = Path(cfg["defaults"]["data_path"])
    output_dir = Path(cfg["defaults"]["output_dir"])
    mode = cfg["defaults"]["mode"]

    if not data_path.exists():
        print(f"Data file not found: {data_path}")
        return

    run_experiment1(data_path, output_dir, CONFIG_PATH, mode)
    run_experiment2(data_path, output_dir, CONFIG_PATH, mode)
    build_report(CONFIG_PATH, mode)
    print("Done. Outputs are in:", output_dir)


def config_menu():
    while True:
        print("\nCONFIG")
        print("1. Set data file path")
        print("2. Edit config in nano")
        print("3. Back")
        choice = input("Select option: ").strip()

        if choice == "1":
            cfg = load_config(CONFIG_PATH)
            path = input("Enter Excel file path: ").strip()
            if path:
                cfg["defaults"]["data_path"] = path
                save_config(cfg)
                print("Updated data path in config.json")
        elif choice == "2":
            subprocess.run(["nano", str(CONFIG_PATH)], check=False)
        elif choice == "3":
            return
        else:
            print("Invalid choice")


def main():
    while True:
        print("\nCLI")
        print("1. START")
        print("2. CONFIG")
        print("3. EXIT")
        choice = input("Select option: ").strip()

        if choice == "1":
            start_pipeline()
        elif choice == "2":
            config_menu()
        elif choice == "3":
            print("Exiting")
            sys.exit(0)
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
