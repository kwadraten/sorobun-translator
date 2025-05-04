import argparse


parser = argparse.ArgumentParser(
    prog="sorobun translator",
    description="a tool for sorobun translation by providing domain-specific to LLMs.",
)

parser.add_argument("-f", "--file", help="The path of sorobun text file.")

parser.add_argument("-o", "--output", help="The path to output.")

parser.add_argument("-c", "--conf", help="The path of config(.json) file.")

parser.add_argument("-d", "--database", help=(
                            "The path of sqlite database file or kuzu database "
                            "directory path."
                        )
)

parser.add_argument("-t", "--target", help="The target language of translation.")

parser.add_argument("-l", "--logging", help=(
                        "Set up with 'info' to show the process of translation. "
                        "Set up with 'debug' to show more information."
                        )
                    )

parser.add_argument("-m", "--mecab", help=(
                            "The path of mecab dictionary directory. If not exists, "
                            "use default FMM algorithm."
                        )
)


if __name__ == "__main__":
    args = parser.parse_args()

    # initalize with config
    from src.config import initialize
    
    initialize(args.conf, inject={
        "logging_level": args.logging,
        "target_language": args.target,
        "database_path": args.database,
        "mecab_dictionary_path": args.mecab
    })

    # input sorobun text
    if args.file:
        with open(args.file, "rt", encoding="utf-8") as f:
            sorobun = f.read()
    else:
        print("Input the sorobun text:")
        sorobun = input(">>> ")
    
    # output translation
    from src.process import translate

    result = translate(sorobun)
    if args.output:
        with open(args.output, "wt", encoding="utf-8") as f:
            f.write(result)
    else:
        print("------------  translation  ---------------")
        print(result)

