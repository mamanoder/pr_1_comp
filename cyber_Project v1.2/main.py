import os
import sys

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(current_dir, "packages"))

    # Use relative import
    myprogram = "cyber_Project v1.2"
    myprogram.main()

if __name__ == "__main__":
    main()