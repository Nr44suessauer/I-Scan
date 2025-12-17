import subprocess
import os

# Path to meshroom folder
MESHROOM_DIR = r"C:\_MAIN\PROGRAMME\MESHROOM\Meshroom-2025.1.0-Windows\Meshroom-2025.1.0"
# Path to meshroom_batch.exe
MESHROOM_BATCH_PATH = MESHROOM_DIR + r"\meshroom_batch.exe"
CAMERA_INIT_EXE = MESHROOM_DIR + r"\aliceVision\bin\aliceVision_cameraInit.exe"
SENSOR_DB_PATH = MESHROOM_DIR + r"\aliceVision\share\aliceVision\cameraSensors.db"

# The path to this MeshroomPipeline folder
MR_PIPELINE_DIR = r"C:\_MAIN\ARBEIT\STUDIUM\MASTER\SEMESTER1\MRL\Repo\I-Scan\implementation\MeshroomPipeline"
# Path to the image output folder
# IMAGES_DIR = r"C:\_MAIN\ARBEIT\STUDIUM\MASTER\SEMESTER1\MRL\Repo\I-Scan\implementation\ControlScript\Modular Version\pictures"
IMAGES_DIR = MR_PIPELINE_DIR + r"\images\skull"

SFM_DIR = MR_PIPELINE_DIR + r"\images\cameraInit.sfm"
PIPELINE_DIR = MR_PIPELINE_DIR + "\\pipelines\\" # Templates can be found here: C:\_MAIN\PROGRAMME\MESHROOM\Meshroom-2025.1.0-Windows\Meshroom-2025.1.0\aliceVision\share\meshroom
OVERRIDE_PATH = MR_PIPELINE_DIR + r"\overrides\meshroom_override.json"
CACHE_DIR = MR_PIPELINE_DIR + r"\cache"
OUTPUT_DIR = MR_PIPELINE_DIR + r"\output"

CAMERA_FOV = "45.0"


def run_meshroom_pipeline():
    try:
        print("\nConvert Images to SFM.")
        convert_images()
        print("\nStarting Meshroom Pipeline.")
        run_meshroom()
        print("\nPipeline execution complete.")
    except Exception as e:
        print(f"\nFATAL ERROR: Pipeline aborted: {e}")

def convert_images():
    env = os.environ.copy()
    alice_root = os.path.join(MESHROOM_DIR, "aliceVision")
    alice_bin = os.path.join(alice_root, "bin")
    
    env["ALICEVISION_ROOT"] = alice_root
    env["PATH"] = alice_bin + os.pathsep + env.get("PATH", "")

    command = [
        CAMERA_INIT_EXE,
        "--sensorDatabase", SENSOR_DB_PATH,
        "--imageFolder", IMAGES_DIR,
        "--output", SFM_DIR,
        "--defaultFieldOfView", CAMERA_FOV,
        "--groupCameraFallback", "folder", 
        "--allowSingleView", "1"
    ]

    try:
        subprocess.run(command, check=True, env=env)
        print(f"✅ Created SFM file at: {SFM_DIR}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create SFM: {e}")

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
