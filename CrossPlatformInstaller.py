import subprocess, sys, shutil, os


def run_build(spec_file, distpath, workpath):
    print(f"Building {spec_file} ...")
    result = subprocess.run([sys.executable, "-m", "PyInstaller", spec_file, "--distpath", distpath, "--workpath", workpath], capture_output=False)
    if result.returncode != 0:
        print(f"Build of {spec_file} failed with code {result.returncode}")
        sys.exit(result.returncode)


def clean_workpath(workpath):
    if os.path.exists(workpath):
        shutil.rmtree(workpath, ignore_errors=True)
        print(f"Cleaned {workpath}")


run_build("SeedNexusData.spec", "executable", "temp_seed_build")
run_build("NexusHotel.spec", "executable", "temp_build")
clean_workpath("temp_seed_build")
clean_workpath("temp_build")
print("Builds complete.")
