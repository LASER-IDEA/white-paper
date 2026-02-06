#!/usr/bin/env python3
"""
Convenience script to process markdown data files and generate web report data.

Usage:
    python scripts/process_data.py                              # Process default example files
    python scripts/process_data.py --input data/my_data.md      # Process specific file
    python scripts/process_data.py --annual                     # Use annual example
    python scripts/process_data.py --all                        # Use all data files

    # Or run from python/src directory:
    python markdown_processor.py --input ../../data/example.md --output ../../output/metrics.json
"""

import sys
import os
from pathlib import Path

# Determine workspace root (parent of scripts folder)
script_dir = Path(__file__).parent
workspace = script_dir.parent

# Add python/src to path
sys.path.insert(0, str(workspace / 'python' / 'src'))

try:
    from markdown_processor import process_markdown_files
    from generate_web_data import generate_typescript
except ImportError as e:
    print(f"Error importing modules: {e}")
    print(f"Script dir: {script_dir}")
    print(f"Workspace: {workspace}")
    print(f"Python path: {sys.path}")
    sys.exit(1)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Process markdown data files and generate web report.'
    )
    parser.add_argument(
        '--input', '-i',
        nargs='*',
        help='Input markdown file(s). If not specified, uses data/example.md'
    )
    parser.add_argument(
        '--annual', '-a',
        action='store_true',
        help='Use data/annual_example.md'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Use all markdown files in data folder'
    )
    parser.add_argument(
        '--output-json', '-j',
        default='output/metrics.json',
        help='Output JSON file (default: output/metrics.json)'
    )
    parser.add_argument(
        '--output-ts', '-t',
        default='web/src/utils/computedData.ts',
        help='Output TypeScript file (default: web/src/utils/computedData.ts)'
    )
    parser.add_argument(
        '--json-only',
        action='store_true',
        help='Only generate JSON, skip TypeScript generation'
    )

    args = parser.parse_args()

    # Determine workspace root
    workspace = script_dir.parent

    print(f"Workspace: {workspace}")

    # Determine input files
    if args.input:
        input_files = [str(workspace / f) for f in args.input]
    elif args.annual:
        input_files = [str(workspace / 'data' / 'annual_example.md')]
    elif args.all:
        data_dir = workspace / 'data'
        input_files = sorted([str(f) for f in data_dir.glob('*.md')])
    else:
        input_files = [str(workspace / 'data' / 'example.md')]

    # Validate input files
    for f in input_files:
        if not Path(f).exists():
            print(f"Error: Input file not found: {f}")
            return 1

    # Process markdown files
    print("=" * 60)
    print("PROCESSING MARKDOWN DATA FILES")
    print("=" * 60)
    print(f"Input files: {input_files}")
    print()

    output_json = str(workspace / args.output_json)
    metrics = process_markdown_files(input_files, output_json)

    if not args.json_only:
        print()
        print("=" * 60)
        print("GENERATING TYPESCRIPT FILE")
        print("=" * 60)

        output_ts = str(workspace / args.output_ts)
        generate_typescript(metrics, output_ts)

    print()
    print("=" * 60)
    print("DONE!")
    print("=" * 60)
    print(f"JSON output: {output_json}")
    if not args.json_only:
        print(f"TypeScript output: {output_ts}")
    print()
    print("To use in web app:")
    print("  1. Update web/src/utils/mockData.ts to import from computedData.ts")
    print("  2. Or replace mockData.ts contents with computedData.ts")
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
