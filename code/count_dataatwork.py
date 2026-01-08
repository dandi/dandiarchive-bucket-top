#!/usr/bin/env python3
"""Count DataAtWork entries per dataset in open-data-registry."""

import sys
from pathlib import Path

import yaml


def count_dataatwork(yaml_path: Path) -> dict:
    """Count entries in each DataAtWork section."""
    try:
        with open(yaml_path) as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return {"error": str(e)}

    counts = {
        "Tutorials": 0,
        "Tools & Applications": 0,
        "Publications": 0,
    }

    dataatwork = data.get("DataAtWork", {})
    if dataatwork:
        for key in counts:
            items = dataatwork.get(key)
            if items:
                counts[key] = len(items)

    return counts


def main():
    datasets_dir = Path("sourcedata/open-data-registry/datasets")
    if not datasets_dir.exists():
        print(f"Error: {datasets_dir} not found", file=sys.stderr)
        sys.exit(1)

    # TSV header
    print("dataset\tTutorials\tTools & Applications\tPublications\tTotal")

    for yaml_file in sorted(datasets_dir.glob("*.yaml")):
        counts = count_dataatwork(yaml_file)
        if "error" in counts:
            print(f"{yaml_file.name}\tERROR\tERROR\tERROR\t0")
            continue

        total = sum(counts.values())
        print(
            f"{yaml_file.name}\t"
            f"{counts['Tutorials']}\t"
            f"{counts['Tools & Applications']}\t"
            f"{counts['Publications']}\t"
            f"{total}"
        )


if __name__ == "__main__":
    main()
