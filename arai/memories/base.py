import os
from typing import List, Optional
import duckdb
from arai.variables.memory import BaseSchemas, Schema, DuckType

class MockMemory(BaseSchemas):
    """This is a table for mocking purpose"""
    id:Optional[str] = Schema(type=DuckType.STRING, desc="unique identifier")
    page_content:Optional[str] = Schema(type=DuckType.STRING, desc="content of the page")
    metadata:Optional[str] = Schema(type=DuckType.STRING, desc="metadata of the page")
    embedding:Optional[List[float]] = Schema(type=DuckType.EMBEDDING[100], desc="embedding of the page")
    created_at:Optional[int] = Schema(type=DuckType.INTEGER, desc="timestamp of the page creation")
    updated_at:Optional[int] = Schema(type=DuckType.INTEGER, desc="timestamp of the page update")

class MemoryManagement:
    """Memory should do CRUD operations on a database
    What it should do:
        - Insert data into the memory
        - Read data from the memory
        - Update data in the memory
        - Delete data from the memory

    Args:
        database_path (str): The path to the database, "./path/to/memory.db"
    """

    def __init__(
            self, 
            database_path: str="./db/memory.db",
            memory_name: str=MockMemory.get_table(),
            schema: dict=MockMemory.get_schemas()
    )->None:
        self.database_path = self.validate_database_path(database_path)
        self.connection = duckdb.connect
        self.memory_name = memory_name
        self.schema = schema
        self.initialize_database()
        self.create_memory()
    
    def initialize_database(self)->None:
        directory = os.path.dirname(self.database_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def validate_database_path(self, database_path: str)->str:
        if not database_path.endswith(".db"):
            raise ValueError("Database path should end with .db")
        return database_path
    
    def execute(self, query:str, data:list | None = None):
        with self.connection(self.database_path) as connection:
            if data:
                return connection.execute(query, data).df()
            return connection.execute(query).df()
        
    def create_memory(self, memory_name:str=None, schema:dict=None)->None:
        if memory_name is None:
            memory_name = self.memory_name
        if schema is None:
            schema = self.schema
        query = f"CREATE TABLE IF NOT EXISTS {memory_name} ({', '.join([f'{key} {value}' for key, value in schema.items()])})"
        self.execute(query)

    def list_memories(self)->list:
        query = "SHOW ALL TABLES;"
        return self.execute(query).query("schema=='main'").reset_index(drop=True)
    
    def drop_memory(self, memory_name=None)->None:
        query = f"DROP TABLE IF EXISTS {self.memory_name if memory_name is None else memory_name}"
        self.execute(query)

    def list_all(self):
        query = "SHOW ALL TABLES;"
        return self.execute(query)