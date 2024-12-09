import os
import sys
import subprocess

def create_and_activate_venv():
    """
    Creates a new Python virtual environment, activates it, installs requirements, and runs app.py.
    """
    venv_dir = "myenv"

    # Create the virtual environment
    print(f"Creating virtual environment in {venv_dir}...")
    if sys.platform.startswith("win"):
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
    else:
        subprocess.run([f"{sys.executable}", "-m", "venv", venv_dir], check=True)

    # Activate the virtual environment
    print("Activating virtual environment...")
    if sys.platform.startswith("win"):
        activate_script = os.path.join(venv_dir, "Scripts", "activate")
        os.system(f"call {activate_script}")
    else:
        activate_script = os.path.join(venv_dir, "bin", "activate")
        subprocess.run([f"source {activate_script}"], shell=True)

    print("Virtual environment activated.")

    # Install requirements
    print("Installing requirements from requirements.txt...")
    if sys.platform.startswith("win"):
        subprocess.run([os.path.join(venv_dir, "Scripts", "pip"), "install", "-r", "requirements.txt"], check=True)
    else:
        subprocess.run([os.path.join(venv_dir, "bin", "pip3"), "install", "-r", "requirements.txt"], check=True)

    print("Requirements installed.")

    # Run app.py
    print("Running app.py...")
    if sys.platform.startswith("win"):
        subprocess.run([os.path.join(venv_dir, "Scripts", "python"), "app.py"], check=True)
    else:
        subprocess.run([os.path.join(venv_dir, "bin", "python3"), "app.py"], check=True)

    print("app.py execution complete.")

if __name__ == "__main__":
    create_and_activate_venv()