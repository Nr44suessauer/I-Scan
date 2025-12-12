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

    print(f"\n🚀 Executing Meshroom Batch: {' '.join(command)}")
    print("-" * 50)
    print("--- STARTING REAL-TIME LOG STREAM ---")
    
    # 1. Use subprocess.Popen for streaming
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE, # Capture stdout pipe
        stderr=subprocess.STDOUT, # Direct stderr into stdout pipe for simpler reading
        text=True,
        bufsize=1, # Set buffer size to 1 line
        universal_newlines=True # Alias for text=True, good for line-by-line reading
    )

    # 2. Read output line by line as it is generated
    for line in iter(process.stdout.readline, ''):
        print(line.strip()) # Print log line immediately

    # 3. Wait for the process to finish and check the return code
    process.wait()
    
    print("-" * 50)
    
    if process.returncode == 0:
        print("✅ Meshroom batch execution successful!")
        return True
    else:
        # If return code is non-zero, the job failed
        print(f"❌ Meshroom batch failed with error code {process.returncode}")
        
        # Optionally, read any remaining output from the buffer if necessary
        remaining_output = process.stdout.read()
        if remaining_output:
             print("--- Remaining Output ---")
             print(remaining_output.strip())
             
        # Raise an exception to be caught by run_meshroom_pipeline
        raise subprocess.CalledProcessError(process.returncode, command)

if __name__ == "__main__":
    run_meshroom_pipeline()
