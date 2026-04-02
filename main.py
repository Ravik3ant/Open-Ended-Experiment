import json
import subprocess
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from data_validation import validate_data_file
from experiment1_poisson_runs import run_experiment1
from experiment2_poisson_runs import run_experiment2
from generate_pdf_report import main as build_report
from poisson_utils import load_config


console = Console()
CONFIG_PATH = Path("config.json")


def save_config(cfg: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)


def show_current_config(cfg: dict):
    table = Table(title="Current Configuration")
    table.add_column("Key")
    table.add_column("Value")
    table.add_row("data_path", cfg["defaults"]["data_path"])
    table.add_row("output_dir", cfg["defaults"]["output_dir"])
    table.add_row("mode", cfg["defaults"]["mode"])
    table.add_row("seeds", str(cfg["random"]["seeds"]))
    console.print(table)


def start_pipeline():
    cfg = load_config(CONFIG_PATH)
    data_path = Path(cfg["defaults"]["data_path"])
    output_dir = Path(cfg["defaults"]["output_dir"])
    mode = cfg["defaults"]["mode"]

    ok, messages = validate_data_file(data_path)
    for msg in messages:
        console.print(f"- {msg}")
    if not ok:
        console.print("[red]Validation failed. Fix data file and rerun START.[/red]")
        return

    console.print("[cyan]Running Experiment 1...[/cyan]")
    run_experiment1(data_path, output_dir, CONFIG_PATH, mode)
    console.print("[cyan]Running Experiment 2...[/cyan]")
    run_experiment2(data_path, output_dir, CONFIG_PATH, mode)
    console.print("[cyan]Building PDF report...[/cyan]")
    build_report(CONFIG_PATH, mode)
    console.print(f"[green]Done. Outputs are in: {output_dir}[/green]")


def config_menu():
    while True:
        cfg = load_config(CONFIG_PATH)
        console.print(Panel("CONFIG MENU\n1) Set data file path\n2) Toggle mode (scientific/clean)\n3) Set output directory\n4) Edit config in nano\n5) Back"))
        show_current_config(cfg)
        choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5"], default="5")

        if choice == "1":
            path = Prompt.ask("Enter Excel file path", default=cfg["defaults"]["data_path"]).strip()
            cfg["defaults"]["data_path"] = path
            save_config(cfg)
            console.print("[green]Updated data path.[/green]")
        elif choice == "2":
            cfg["defaults"]["mode"] = "clean" if cfg["defaults"]["mode"] == "scientific" else "scientific"
            save_config(cfg)
            console.print(f"[green]Mode set to {cfg['defaults']['mode']}[/green]")
        elif choice == "3":
            out = Prompt.ask("Enter output directory", default=cfg["defaults"]["output_dir"]).strip()
            cfg["defaults"]["output_dir"] = out
            save_config(cfg)
            console.print("[green]Updated output directory.[/green]")
        elif choice == "4":
            subprocess.run(["nano", str(CONFIG_PATH)], check=False)
        elif choice == "5":
            return


def main():
    while True:
        console.print(Panel("POISSON DECAY CLI\n1) START\n2) CONFIG\n3) VALIDATE DATA\n4) EXIT", title="Main Menu"))
        choice = Prompt.ask("Select option", choices=["1", "2", "3", "4"], default="1")

        if choice == "1":
            start_pipeline()
        elif choice == "2":
            config_menu()
        elif choice == "3":
            cfg = load_config(CONFIG_PATH)
            ok, messages = validate_data_file(Path(cfg["defaults"]["data_path"]))
            for msg in messages:
                console.print(f"- {msg}")
            console.print("[green]Data valid[/green]" if ok else "[red]Data invalid[/red]")
        elif choice == "4":
            console.print("Exiting")
            return


if __name__ == "__main__":
    main()
