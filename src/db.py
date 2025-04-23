import sqlite3
import os
import logging
from typing import List, Tuple
from pathlib import Path

class Db:

    def __init__(self, db_path: Path | None = None) -> None:
        if db_path:
            self.db_path = db_path
        else:
            code_dir = os.path.dirname(__file__)
            self.db_path = os.path.join(os.path.split(code_dir)[0], "dictionary.db")
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()
    
    def query(self, words: List[str]) -> List[Tuple[str, str]]:
        sql_query = f"select * from dict where word in ('{"', '".join(words)}')"
        logging.info(f"The sql query is:\n{sql_query}")
        res = self.cur.execute(sql_query)
        return res.fetchall()