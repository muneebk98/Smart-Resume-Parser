import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [parser|report]")
        return

    choice = sys.argv[1].lower()

    if choice == "parser":
        subprocess.run(["python", "parser.py"])
    elif choice == "report":
        subprocess.run(["python", "report.py"])
    else:
        print("Invalid option. Use 'parser' or 'report'.")

if __name__ == "__main__":
    main()
