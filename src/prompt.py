from .config import Config

TARGET_LANG = Config["target_language"]

def analyze_prompt(sorobun: str) -> str:

    return (
        "You are a soro-bun(候文) translator. Now the first step you need to do is "
        "to analyze the context of the original text: Which period was this text "
        "written in? What are the subject and object of each sentence in this text?"
        "Is there people's or institutions' name in this text? Can we infer any "
        "other potential context about this text? "
        f"Output the original text and analysis in TOML format, using {TARGET_LANG}. "
        "Don't add any additional content by yourself.\n"
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
        "Remember: 1.Retain existing notes. 2.Summary the definition to save the token." 
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

def reason_prompt(last: str) -> str:

    return (
        "You are a soro-bun (候文) translator. Based on the existing annotations provided below, "
        "select the most appropriate meaning of words and phrases to produce accurate translations."
        "Remember: 1. It's not necessary to write notes in final translation. "
        f"2. You need translate the *original* text. The target language is **{TARGET_LANG}**, "
        "Just output plain text, don't output anything in other languages.\n"
        "**your output history**\n"
        f"{last}"
    )