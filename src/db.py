import sqlite3
import os
import logging
from typing import List, Tuple
from pathlib import Path
from config import Config

class Db:

    def __init__(self) -> None:
        if Config.get("database_path"):
            self.db_path = Config["database_path"]
        else:
            code_dir = os.path.dirname(__file__)
            self.db_path = os.path.join(os.path.split(code_dir)[0], "dictionary.db")
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()
    
    def query(self, words: List[str]) -> List[Tuple[str, str]]:
        result = []
        step = 10
        batch_number = int(len(words) / step) + 1
        
        for num in range(batch_number):
            start = num * step
            end = (num + 1) * step
            sql_query = f"select * from dict where word in ('{"', '".join(words[start:end])}')"
            logging.info(f"The sql query ({num+1}/{batch_number}) is:\n{sql_query}")
            res = self.cur.execute(sql_query)
            result += res.fetchall()
        return result