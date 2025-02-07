
import argparse

def main ():
    parser = argparse.ArgumentParser()
    parser.add_argument("value")

    args = parser.parse_args()
    
    with open("/app/value.txt", "r") as file:
        assert file.read() == str(args.value)

if __name__ == "__main__":
    main()
