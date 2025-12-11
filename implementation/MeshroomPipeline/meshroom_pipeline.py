import subprocess
import os

# The path to this MeshroomPipeline folder
USER_DIR = r"C:\_MAIN\ARBEIT\STUDIUM\MASTER\SEMESTER1\MRL\Repo\I-Scan\implementation\MeshroomPipeline"
# Path to meshroom_batch.exe
MESHROOM_BATCH_PATH = r"C:\_MAIN\PROGRAMME\MESHROOM\Meshroom-2025.1.0-Windows\Meshroom-2025.1.0\meshroom_batch.exe"

INPUT_IMAGES_DIR = USER_DIR + r"\images"
PIPELINE_PATH = USER_DIR + r"\pipelines\photogrammetry.mg" # Templates can be found here: C:\_MAIN\PROGRAMME\MESHROOM\Meshroom-2025.1.0-Windows\Meshroom-2025.1.0\aliceVision\share\meshroom
OVERRIDE_PATH = USER_DIR + r"\overrides\meshroom_override.json"
CACHE_DIR = USER_DIR + r"\cache"
OUTPUT_DIR = USER_DIR + r"\output"


def run_meshroom_pipeline():
    try:
        print("\nStarting Meshroom Pipeline.")
        run_meshroom()
        print("\nPipeline execution complete.")
    except Exception as e:
        print(f"\nFATAL ERROR: Pipeline aborted: {e}")

# See https://meshroom-manual.readthedocs.io/en/latest/feature-documentation/cmd/photogrammetry.html
def run_meshroom(
    meshroom_batch_path: str = MESHROOM_BATCH_PATH,
    input_images: str = INPUT_IMAGES_DIR,
    pipeline_mg: str = PIPELINE_PATH,
    overrides_json: str = OVERRIDE_PATH,
    output_dir: str = OUTPUT_DIR,
    cache_dir: str = CACHE_DIR
):
    command = [
        meshroom_batch_path,
        "--input", input_images,
        "--pipeline", pipeline_mg,
        # "--overrides", overrides_json,
        "--output", output_dir,
        "--cache", cache_dir
    ]

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        print("✅ Meshroom batch execution successful!")
        print("--- STDOUT (Summary) ---")
        print("\n".join(result.stdout.strip().splitlines()[-5:]))
        if result.stderr.strip():
            print("--- STDERR (Warnings/Logs) ---")
            print(result.stderr.strip())

    except subprocess.CalledProcessError as e:
        print(f"❌ Meshroom batch failed with error code {e.returncode}")
        print("--- STDERR (Error Details) ---")
        print(e.stderr)
        raise

    except FileNotFoundError:
        # Note: This usually catches if meshroom_batch_path is invalid
        print(f"❌ Error: The meshroom_batch script was not found. Check the path: {meshroom_batch_path}")
        raise

if __name__ == "__main__":
    run_meshroom_pipeline()
