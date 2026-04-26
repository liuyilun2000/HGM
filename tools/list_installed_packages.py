#!/usr/bin/env python3
"""Print installed Python packages and their versions."""

import argparse
import json
import sys
from importlib import metadata


def list_distributions():
    """Return installed packages as sorted (name, version) tuples."""
    packages = {}
    for dist in metadata.distributions():
        name = dist.metadata.get("Name") or dist.metadata.get("Summary")
        if not name:
            continue
        # Keep one entry per normalized package name.
        key = name.strip().lower()
        packages[key] = (name.strip(), dist.version)
    return sorted(packages.values(), key=lambda item: item[0].lower())


def main():
    parser = argparse.ArgumentParser(
        description="Print all installed Python packages and versions."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output package list as JSON.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Write output to a file path instead of stdout.",
    )
    args = parser.parse_args()

    try:
        packages = list_distributions()
    except Exception as exc:  # pragma: no cover
        print(f"Failed to read installed distributions: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    if args.json:
        payload = [{"name": name, "version": version} for name, version in packages]
        content = json.dumps(payload, indent=2)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(content)
                f.write("\n")
            print(f"Wrote package JSON to: {args.output}")
        else:
            print(content)
        return

    lines = [f"Installed packages: {len(packages)}"]
    lines.extend(f"{name}=={version}" for name, version in packages)
    content = "\n".join(lines)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
            f.write("\n")
        print(f"Wrote package report to: {args.output}")
    else:
        print(content)


if __name__ == "__main__":
    main()
