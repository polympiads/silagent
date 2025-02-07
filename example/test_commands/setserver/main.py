
import argparse

def main ():
    parser = argparse.ArgumentParser()
    parser.add_argument("value")

    args = parser.parse_args()
    
    with open("/app/value.txt", "w") as file:
        file.write(str(args.value))

if __name__ == "__main__":
    main()
