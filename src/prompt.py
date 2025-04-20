
def analyze_prompt(sorobun: str) -> str:

    return (
        "You are a soro-bun(候文) translator. Now the first step you need to do is "
        "to analyze the context of the original text: Which period was this text "
        "written in? What are the subject and object of each sentence in this text?"
        " Can we infer any other potential context about this text? Output the "
        "original text and analysis in TOML format. Don't add any additional "
        "content by yourself.\n"
        "**<example>**\n"
        "[text]\n"
        "original = {{Put Original Text Here}}\n"
        "analysis = {{Put Analyzing Text Here}}\n"
        "**original text**\n"
        f"{sorobun}"
    )

def lookup_prompt(last: str, definitions: str) -> str:

    return (
        "You are a soro-bun(候文) translator. Now you need add notes into your output "
        "history for the translation. According to the your analysis, compare the given "
        "information and your translation, choose the best definition of words.\n"
        "Remember: 1.Retain existing notes. 2.Summary the definition to save the token.\n"
        "**<example>**\n"
        "[text]\n"
        "notes = [\n"
        '	{ word = "{{Put a word here.}}", definition = "{{Put a definition here.}}"},\n'
        "]\n"
        "original = {{Put Original Text Here}}\n"
        "analysis = {{Put Analyzing Text Here}}\n"
        "**your output history**\n"
        f"{last}\n"
        "**given information**\n"
        f"{definitions}"
    )

def reason_prompt(last: str, language: str) -> str:

    return (
        "You are a soro-bun(候文) translator. Now according to your output history, you need "
        "to select the proper meaning of words from the notes, output your translation. "
        f"The target language is {language}, don't output anything in other languages.\n"
        "**your output history**\n"
        f"{last}"
    )