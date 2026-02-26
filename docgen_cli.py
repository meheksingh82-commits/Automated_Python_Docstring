import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from scripts.check_docs import main


if __name__ == "__main__":
    main()
