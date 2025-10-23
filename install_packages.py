import subprocess
import sys
import tkinter.messagebox as box

def install_requirements():
    try:
        box.showinfo("Install Packages", "This program will install all the necessary packages to run ITk Metrologist. Press OK to continue")

        # Run the pip command and display output in real-time
        process = subprocess.Popen(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Print output in real-time
        for line in process.stdout:
            print(line, end="")  # Print stdout lines in real-time

        # Wait for the process to complete
        process.wait()

        # Handle errors
        if process.returncode != 0:
            error_message = process.stderr.read()
            print(f"Failed to install packages: {error_message}")
            box.showerror("Error", f"Failed to install the packages:\n{error_message}")
            sys.exit(1)

        print("All packages installed successfully.")
        box.showinfo("Install Packages", "All packages installed successfully")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        box.showerror("Error", f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()