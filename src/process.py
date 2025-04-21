from .prompt import analyze_prompt, lookup_prompt, reason_prompt
import logging
from typing import List

def predict():
    pass

def definition_formatting():
    pass

def query_definitions():
    definition_formatting()
    pass

def analyze(sorobun: str) -> str:
    prompt = analyze_prompt(sorobun)
    logging.debug(f"the prompt of the first stage is:\n{prompt}")
    result = predict(prompt)
    logging.debug(f"the result of the first stage is:\n{result}")
    return result

def lookup_loop(output_history: str, definitions_list: List[str]) -> str:
    step = 5
    batch_number = int(len(definitions_list) / step) + 1

    for num in range(batch_number):

        start = num * step
        end = (num + 1) * step
        list_slice = definitions_list[start:end]
        definitions = "\n".join(list_slice)
        
        prompt = lookup_prompt(output_history, definitions)
        logging.debug(f"the prompt ({num+1}/{batch_number}) in the second stage is:\n{output_history}")
        result = predict(prompt)
        logging.debug(f"the result ({num+1}/{batch_number}) in the second stage is:\n{result}")

    return result

def reason(output_history: str, target_language: str) -> str:
    prompt = reason_prompt(output_history, target_language)
    logging.debug(f"the prompt of the third stage is:\n{output_history}")
    result = predict(prompt)
    logging.debug(f"the result of the third stage is:\n{result}")
    return result

def translate(sorobun: str) -> str:
    TARGET_LANGUAGE = "chinese"

    analyze_result = analyze(sorobun)
    definitions_list = query_definitions(sorobun)
    analysis_with_notes = lookup_loop(analyze_result, definitions_list)
    translation = reason(analysis_with_notes, TARGET_LANGUAGE)

    return translation


    
