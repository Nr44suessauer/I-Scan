import subprocess
import os

# The path to this MeshroomPipeline folder
MR_PIPELINE_DIR = r"C:\_MAIN\ARBEIT\STUDIUM\MASTER\SEMESTER1\MRL\Repo\I-Scan\implementation\MeshroomPipeline"
# Path to meshroom_batch.exe
MESHROOM_BATCH_PATH = r"C:\_MAIN\PROGRAMME\MESHROOM\Meshroom-2025.1.0-Windows\Meshroom-2025.1.0\meshroom_batch.exe"
# Path to the image output folder
IMAGES_DIR = r"C:\_MAIN\ARBEIT\STUDIUM\MASTER\SEMESTER1\MRL\Repo\I-Scan\implementation\ControlScript\Modular Version\pictures"

SFM_DIR = MR_PIPELINE_DIR + r"\images\skull"
PIPELINE_DIR = MR_PIPELINE_DIR + "\\pipelines\\" # Templates can be found here: C:\_MAIN\PROGRAMME\MESHROOM\Meshroom-2025.1.0-Windows\Meshroom-2025.1.0\aliceVision\share\meshroom
OVERRIDE_PATH = MR_PIPELINE_DIR + r"\overrides\meshroom_override.json"
CACHE_DIR = MR_PIPELINE_DIR + r"\cache"
OUTPUT_DIR = MR_PIPELINE_DIR + r"\output"


def run_meshroom_pipeline():
    try:
        print("\nConvert Images to SFM.")
        convert_images()
        print("\nStarting Meshroom Pipeline.")
        # run_meshroom()
        print("\nPipeline execution complete.")
    except Exception as e:
        print(f"\nFATAL ERROR: Pipeline aborted: {e}")

def convert_images(
        pipeline: str = "convertImages.mg"
):
    command = [
        MESHROOM_BATCH_PATH,
        "--input", IMAGES_DIR,
        "--pipeline", PIPELINE_DIR + pipeline,
        "--output", OUTPUT_DIR,
        "--cache", SFM_DIR
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
        print(f"❌ Error: The meshroom_batch script was not found. Check the path: {MESHROOM_BATCH_PATH}")
        raise

# See https://meshroom-manual.readthedocs.io/en/latest/feature-documentation/cmd/photogrammetry.html
def run_meshroom(
        pipeline: str = "photogrammetry.mg"
):
    command = [
        MESHROOM_BATCH_PATH,
        "--input", SFM_DIR,
        "--pipeline", PIPELINE_DIR + pipeline,
        # "--overrides", OVERRIDE_PATH,
        "--output", OUTPUT_DIR,
        "--cache", CACHE_DIR
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
        print(f"❌ Error: The meshroom_batch script was not found. Check the path: {MESHROOM_BATCH_PATH}")
        raise

if __name__ == "__main__":
    run_meshroom_pipeline()
