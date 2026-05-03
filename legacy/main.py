import sys
import os
import json
import subprocess

def print_header(text):
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80)

def run_step(cmd, step_name):
    print_header(f"RUNNING: {step_name}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error in {step_name}:")
        print(e.stderr)
        return False
    return True

def main():
    print_header("EPISTEMOLOGICAL ENGINE V2 - COMMAND CENTER")

    # 1. Discovery (Path A)
    if not run_step("python3 semantic_extractor.py", "Autonomous Dimension Discovery"):
        return

    # 2. Optimization (Singularity)
    if not run_step("python3 singularity_engine.py TOE", "Singularity Resolution (TOE)"):
        return

    # 3. Adversarial Stress-Testing
    if not run_step("python3 adversarial_tester.py", "Adversarial Stress-Testing"):
        return

    # 4. Publication (Path B)
    # Singularity engine already calls paper_generator.py

    print_header("SYSTEM COMPLETE: All preprints and results generated.")

if __name__ == "__main__":
    main()
