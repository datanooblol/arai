from typing import Optional
from arai.memories.base import MemoryManagement
from arai.variables.memory import BaseSchemas, DuckType, Schema


class JargonSchemas(BaseSchemas):
    """This is a table for jargon memory"""
    id:Optional[str] = Schema(type=DuckType.STRING, desc="unique identifier")
    jargon:Optional[str] = Schema(type=DuckType.STRING, desc="jargon")
    definition:Optional[str] = Schema(type=DuckType.STRING, desc="definition")
    metadata:Optional[str] = Schema(type=DuckType.STRING, desc="metadata of the jargon")
    created_at:Optional[int] = Schema(type=DuckType.INTEGER, desc="timestamp of the jargon creation")
    updated_at:Optional[int] = Schema(type=DuckType.INTEGER, desc="timestamp of the jargon update")

class JargonMemory(MemoryManagement):
    def __init__(self):
        super().__init__(memory_name=JargonSchemas.get_table(), schema=JargonSchemas.get_schemas())