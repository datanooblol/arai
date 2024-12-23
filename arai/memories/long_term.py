from typing import List, Optional
from arai.memories.base import MemoryManagement
from arai.utils.utils import Document
from arai.variables.memory import BaseSchemas, DuckType, Schema


class LongTermSchemas(BaseSchemas):
    """This is a table for long term memory"""
    id:Optional[str] = Schema(type=DuckType.STRING, desc="unique identifier")
    page_content:Optional[str] = Schema(type=DuckType.STRING, desc="content of the page")
    metadata:Optional[str] = Schema(type=DuckType.STRING, desc="metadata of the page")
    embedding:Optional[List[float]] = Schema(type=DuckType.EMBEDDING[2], desc="embedding of the page")
    created_at:Optional[int] = Schema(type=DuckType.INTEGER, desc="timestamp of the page creation")
    updated_at:Optional[int] = Schema(type=DuckType.INTEGER, desc="timestamp of the page update")

class LongTermMemory(MemoryManagement):
    def __init__(self):
        super().__init__(memory_name=LongTermSchemas.get_table(), schema=LongTermSchemas.get_schemas())

    def create_fts_index(self):
        # https://duckdb.org/docs/extensions/full_text_search.html
        self.execute("INSTALL fts;")
        self.execute("LOAD fts;")
        query = f"PRAGMA create_fts_index('{self.memory_name}', 'id', 'page_content', overwrite=1);"
        self.execute(query)

    # def create_vs_index(self):
    #     self.execute("INSTALL vss;")
    #     self.execute("LOAD vss;")
    #     self.execute("SET GLOBAL hnsw_enable_experimental_persistence = true;")
    #     query = f"CREATE INDEX idx ON {self.memory_name} USING HNSW (embedding);"
    #     self.execute(query)

    def add_document(self, document:list):
        query = f"INSERT INTO {self.memory_name} VALUES (?, ?, ?, ?, ?, ?);"
        self.execute(query, document)

    def fts_search(self, query:str, limit:int=10):
        query = query.replace(";", "")
        query = f"SELECT id, page_content, metadata, fts_main_{self.memory_name}.match_bm25(id, '{query}') AS score FROM {self.memory_name} WHERE score IS NOT NULL ORDER BY score DESC LIMIT {limit};"
        return self.execute(query)
    
    def vector_search(self, query:str, limit:int=10):
        query = f"SELECT *, array_cosine_similarity(embedding, {query}::FLOAT[2]) AS score FROM {self.memory_name} ORDER BY score DESC LIMIT 5;"
        return self.execute(query)
    
    def hybrid_search(self, query:str, limit:int=10):
        ...

    def drop_index(self, memory_name=None):
        query = f"PRAGMA drop_fts_index({self.memory_name if memory_name is None else memory_name});"
        self.execute(query)

    def sample(self,):
        query = f"SELECT * FROM {self.memory_name} LIMIT 10;"
        return self.execute(query)
    
    def drop_all(self):
        self.drop_memory()
        self.drop_index()