#!/usr/bin/env python3
"""Count DataAtWork entries per dataset in open-data-registry."""

import subprocess
import sys
from pathlib import Path

import yaml


def get_last_updated(yaml_path: Path, repo_root: Path) -> str:
    """Get last git commit date for the file."""
    try:
        # Use relative path from repo root
        rel_path = yaml_path.relative_to(repo_root)
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ai", str(rel_path)],
            capture_output=True,
            text=True,
            cwd=repo_root,
        )
        if result.returncode == 0 and result.stdout.strip():
            # Return just the date part (YYYY-MM-DD)
            return result.stdout.strip().split()[0]
    except Exception:
        pass
    return ""


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
    repo_root = Path("sourcedata/open-data-registry")
    if not datasets_dir.exists():
        print(f"Error: {datasets_dir} not found", file=sys.stderr)
        sys.exit(1)

    # TSV header
    print("dataset\tTutorials\tTools & Applications\tPublications\tTotal\tlast_updated")

    for yaml_file in sorted(datasets_dir.glob("*.yaml")):
        counts = count_dataatwork(yaml_file)
        last_updated = get_last_updated(yaml_file, repo_root)

        if "error" in counts:
            print(f"{yaml_file.name}\tERROR\tERROR\tERROR\t0\t{last_updated}")
            continue

        total = sum(counts.values())
        print(
            f"{yaml_file.name}\t"
            f"{counts['Tutorials']}\t"
            f"{counts['Tools & Applications']}\t"
            f"{counts['Publications']}\t"
            f"{total}\t"
            f"{last_updated}"
        )


if __name__ == "__main__":
    main()
