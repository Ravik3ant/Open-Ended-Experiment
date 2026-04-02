from pathlib import Path

import pandas as pd


REQUIRED = {
    "Sheet1": ["Sr. Num", "Count"],
    "Sheet2": ["Sr. No.", "t=20s", "t=30s"],
}


def validate_data_file(path: Path) -> tuple[bool, list[str]]:
    messages: list[str] = []
    if not path.exists():
        return False, [f"Data file not found: {path}"]

    try:
        xls = pd.ExcelFile(path)
    except Exception as exc:
        return False, [f"Failed to open workbook: {exc}"]

    ok = True
    for sheet, cols in REQUIRED.items():
        if sheet not in xls.sheet_names:
            ok = False
            messages.append(f"Missing sheet: {sheet}")
            continue
        df = pd.read_excel(path, sheet_name=sheet)
        missing_cols = [c for c in cols if c not in df.columns]
        if missing_cols:
            ok = False
            messages.append(f"{sheet}: missing columns {missing_cols}")
            continue

        clean = df[cols].dropna()
        messages.append(f"{sheet}: rows={len(df)}, valid_rows={len(clean)}")
        if len(clean) == 0:
            ok = False
            messages.append(f"{sheet}: no valid rows after dropping missing values")

    return ok, messages
