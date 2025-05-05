import logging
from typing import List, Tuple
from .prompt import analyze_prompt, lookup_prompt, reason_prompt
from .llm import Model
from .db import Db
from .seg import Tagger

# -------------------------
# !! global variables !!
MODEL = Model()
DATABASE = Db()
TAGGER = Tagger()
# -------------------------


def text_segment(sorobun: str) -> List[str]:
    words = TAGGER.parse(sorobun)
    words = list(set(words))
    return words

def definition_formatting(query_results: List[Tuple[str, str]]) -> List[str]:
    result = []
    for w, d in query_results:
        d = d.replace("\n", "")
        result.append(
            f"Dictionary Content related to the word '{w}': {d} \n"
        )
    return result

def query_definitions(sorobun: str) -> List[str]:
    words = text_segment(sorobun)
    logging.info(f"text segmentation ended. The result is as below:\n{words}")
    dictionary_tuple = DATABASE.query(words)
    return definition_formatting(dictionary_tuple)

def analyze(sorobun: str) -> str:
    prompt = analyze_prompt(sorobun)
    logging.info(f"the prompt of the first stage is:\n{prompt}")
    result = MODEL.predict(prompt, is_reasoning=False)
    logging.info(f"the result of the first stage is:\n{result}")
    return result

def lookup_loop(output_history: str, definitions_list: List[str]) -> str:
    step = 8
    batch_number = int(len(definitions_list) / step)
    if len(definitions_list) % step > 0:
        batch_number += 1
    temp_result = output_history

    for num in range(batch_number):
        start = num * step
        end = (num + 1) * step
        list_slice = definitions_list[start:end]
        definitions = "".join(list_slice)
        
        prompt = lookup_prompt(temp_result, definitions)
        logging.info(f"the prompt ({num+1}/{batch_number}) in the second stage is:\n{prompt}")
        temp_result = MODEL.predict(prompt, is_reasoning=False)
        logging.info(f"the result ({num+1}/{batch_number}) in the second stage is:\n{temp_result}")

    return temp_result

def reason(output_history: str) -> str:
    prompt = reason_prompt(output_history)
    logging.info(f"the prompt of the third stage is:\n{prompt}")
    result = MODEL.predict(prompt, is_reasoning=True)
    logging.info(f"the result of the third stage is:\n{result}")
    return result

def translate(sorobun: str) -> str:

    analyze_result = analyze(sorobun)
    definitions_list = query_definitions(sorobun)
    analysis_with_notes = lookup_loop(analyze_result, definitions_list)
    translation = reason(analysis_with_notes)

    return translation
