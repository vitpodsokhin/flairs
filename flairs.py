#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace, REMAINDER
from subprocess import run
from pathlib import Path

def get_script_directory() -> Path:
    return Path(__file__).resolve().parent / 'exe'

def list_available_scripts() -> list:
    script_dir = get_script_directory()
    scripts = [f.stem for f in script_dir.glob('*.py')]
    return scripts

def select_script(script_name: str) -> Path:
    script_dir = get_script_directory()
    script_path = script_dir / f"{script_name}.py"
    return script_path

class ArgHelp:
    description = "Run a specified script with arguments."
    script      = "Script to run (e.g., exclude-addresses)"
    script_args = "Arguments to pass to the script"

def parse_arguments() -> Namespace:
    available_scripts = list_available_scripts()
    script_list_str = ', '.join(script for script in available_scripts)

    parser = ArgumentParser(
        description=ArgHelp.description,
        epilog=f"Available scripts: {script_list_str}"
    )
    parser.add_argument('script', help=ArgHelp.script)
    parser.add_argument('script_args', nargs=REMAINDER, help=ArgHelp.script_args)
    return parser.parse_args()

def main() -> None:
    import sys
    args = parse_arguments()

    script_name = args.script
    script_path = select_script(script_name)

    if script_path.exists():
        try:
            result = run(
                [sys.executable, script_path] + args.script_args,
                capture_output=True, text=True
            )
            print(result.stdout.strip(), file=sys.stdout)
            if result.stderr:
                print(result.stderr.strip(), file=sys.stderr)
            sys.exit(result.returncode)
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)
            sys.exit(result.returncode)
    else:
        available_scripts = list_available_scripts()
        print(f"Script '{script_name}' not found.", file=sys.stderr)
        print("Available scripts:")
        for script in available_scripts:
            print(f" - {script}")
        sys.exit(255)

if __name__ == '__main__':
    main()