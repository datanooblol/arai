from typing import Optional
from arai.memories.base import MemoryManagement
from arai.variables.memory import BaseSchemas, DuckType, Schema


class PersonaSchemas(BaseSchemas):
    """This is a table for persona memory"""
    id:Optional[str] = Schema(type=DuckType.STRING, desc="unique identifier")
    page_content:Optional[str] = Schema(type=DuckType.STRING, desc="content of the page")
    metadata:Optional[str] = Schema(type=DuckType.STRING, desc="metadata of the page")
    created_at:Optional[int] = Schema(type=DuckType.INTEGER, desc="timestamp of the page creation")
    updated_at:Optional[int] = Schema(type=DuckType.INTEGER, desc="timestamp of the page update")

class PersonaMemory(MemoryManagement):
    def __init__(self):
        super().__init__(memory_name=PersonaSchemas.get_table(), schema=PersonaSchemas.get_schemas())