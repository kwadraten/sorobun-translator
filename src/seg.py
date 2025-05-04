import logging
from typing import List
from .db import Db
from .config import Config

class TrieNode:
    def __init__(self) -> None:
        self.children = {}
        self.is_word = False

class Trie:
    def __init__(self, dictionary: List[str]) -> None:
        self.trie = TrieNode()
        self.max_length = 0
        self.dictionary = dictionary

        self.build_trie(dictionary)

    def build_trie(self, dictionary: List[str]) -> None:
        """Builds a Trie from the dictionary."""
        for word in dictionary:
            self.insert(word)
            self.max_length = max(self.max_length, len(word))

    def insert(self, word: str) -> None:
        """Inserts a word into the Trie."""
        node = self.trie
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True

    def in_dictionary(self, word: str) -> bool:
        """Checks if a word exists in the dictionary, using Trie Search.  This is the key optimization"""
        node = self.trie
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word

class Tagger():

    def __init__(self) -> None:
        self.mecab = None
        self.trie = None

        if Config.get("mecab_dictionary_path"):
            import MeCab
            if Config["mecab_dictionary_path"][-1] != '/':
                dict_path = Config["mecab_dictionary_path"] + '/' 
            else:
                dict_path = Config["mecab_dictionary_path"]
            argument = f"-r {dict_path + "dicrc"} -d {dict_path}"
            logging.info(f"The cli argument for mecab is: {argument}")
            self.mecab = MeCab.Tagger(argument)
        else:
            logging.info("No mecab config found. Switching to FMM.")
            database = Db()
            logging.info("Start to build Trie...")
            all_words = database.fetch_all_words()
            self.trie = Trie(all_words)
            logging.info("Success. Trie is built.")
    
    def FMM(self, text: str)  -> List[str]:
        # forward maximum matching algorithm
        result = []
        start = 0

        while start < len(text):
            end = min(start + self.trie.max_length, len(text))  # Limit the search to max_length
            while end > start:
                word = text[start:end]
                if self.trie.in_dictionary(word):  # Use the in_dictionary method
                    result.append(word)
                    # if the last part of sentence is a word, this code make start = len(text),
                    # and thus cause a IndexError
                    start = end  
                    break
                end -= 1

            # so fix the "start = len(text)" bug here
            if end == start and start < len(text):  # No word found, treat it as a single character
                try:
                    result.append(text[start])
                    start += 1
                except IndexError as e:
                    print(f"the start num is {start}, cause:",e)
        
        return result

    def parse(self, sorobun: str) -> List[str]:
        if self.mecab:
            tags = self.mecab.parse(sorobun)
            words = [row.split('\t')[0] for row in tags.split("\n")]
            words.remove("EOS")
            words.remove("")
            return words
        else:
            return self.FMM(sorobun)
