
import argparse

from client import get_value

def main ():
    parser = argparse.ArgumentParser()
    parser.add_argument("value")

    args = parser.parse_args()
    
    assert get_value().decode(encoding="utf-8") == f"Hello, World {args.value} !"

if __name__ == "__main__":
    main()

import argparse
