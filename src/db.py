import os
import logging
from typing import List, Tuple
from config import Config

class Db:

    def __init__(self) -> None:
        if Config.get("database_path"):
            self.db_path = Config["database_path"]
        else:
            code_dir = os.path.dirname(__file__)
            self.db_path = os.path.join(os.path.split(code_dir)[0], "dictionary.db")
        
        if os.path.isfile(self.db_path):
            import sqlite3
            self.type = "sqlite"
            self.conn = sqlite3.connect(self.db_path)
            self.cur = self.conn.cursor()
        elif os.path.isdir(self.db_path):
            import kuzu
            self.type = "kuzu"
            self.conn = kuzu.Database(self.db_path, read_only=True)
            self.cur = kuzu.Connection(self.conn)
        else:
            raise RuntimeError("No vaild database path. Please check the config file.")
    
    def query(self, words: List[str]) -> List[Tuple[str, str]]:
        if self.type == "sqlite":
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
        
        else:
            result = []
            for word in words:
                res = self.cur.execute(
                    "MATCH (w:Word {content: '"+word+"'})-[r:DefinedAs]->(d:Definition) RETURN d"
                )
                while res.has_next():
                    item = res.get_next()
                    result.append((word, item[0]["content"]))
                
        return result
    
    def fetch_all_words(self) -> List[str]:
        if self.type == "sqlite":
            res = self.cur.execute("select word from dict")
            result = res.fetchall()
            # The result of fetchall is List[Tuple[str]].
            # So here needs type conversion.
            result = [word_tuple[0] for word_tuple in result]
        else:
            res = self.cur.execute("MATCH (w: Word) RETURN w")
            result = []
            while res.has_next():
                item = res.get_next()
                result.append(item[0]["content"])
        
        logging.info(f"fetched {len(result)} words from the database.")
        return result