import sys

def convert_to_oneliner(vbscript_file):
    try:
        with open(vbscript_file, "rt") as file:
            vbs_code = file.read()
            return (
                vbs_code
                .replace("\r", "")
                .replace("\n", ":")
                .replace("\t", " ")
                .replace("& _ :", "& ")
                .replace("& _:", "& ")
            )
    except FileNotFoundError:
        return "Podany plik nie istnieje."

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Podaj nazwę pliku VBS jako argument.")
    else:
        vbscript_file = sys.argv[1]
        print(convert_to_oneliner(vbscript_file))