# import subprocess
# import os

# MESHROOM_PYTHON_EXE = "/path/to/Meshroom-*/aliceVision/Python/python.exe"
# TARGET_SCRIPT = "C:/_MAIN/ARBEIT/STUDIUM/MASTER/SEMESTER1/MRL/Repo/I-Scan/implementation/MeshroomPipeline/meshroom_pipeline.py"

# def run_script_with_meshroom_python(script_path: str, python_exe_path: str) -> bool:
#     command = [
#         python_exe_path,
#         script_path
#     ]

#     try:
#         result = subprocess.run(
#             command,
#             check=True,
#             capture_output=True,
#             text=True,
#             encoding='utf-8'
#         )

#         print("✅ Execution successful.")
#         # print("--- Output ---", result.stdout) # Uncomment for full output
#         return True

#     except subprocess.CalledProcessError as e:
#         print(f"❌ Script failed! Return Code: {e.returncode}")
#         print("--- STDERR ---", e.stderr.strip())
#         return False
#     except FileNotFoundError:
#         print(f"❌ Error: Python executable not found at {python_exe_path}")
#         return False

# if __name__ == "__main__":
#     if not os.path.exists(MESHROOM_PYTHON_EXE):
#         print("Error: Please update MESHROOM_PYTHON_EXE to the correct path.")
#     else:
#         run_script_with_meshroom_python(TARGET_SCRIPT, MESHROOM_PYTHON_EXE)