from typing import Dict, NamedTuple

class EMBEDDING:
    def __getitem__(self, item):
        return f"FLOAT[{item}]"
    
STRING = "STRING"
INTEGER = "INTEGER"
FLOAT = "FLOAT"
EMBEDDING = EMBEDDING()
class DuckType:
    STRING = STRING
    INTEGER = INTEGER
    FLOAT = FLOAT
    EMBEDDING = EMBEDDING

# class Schema(NamedTuple):
#     type:str
#     desc:str

# class MetaSchemas(type):
#     def __new__(cls, name, bases, dct, table=None):
#         if table is not None:
#             cls.__table__ = table
#         else:
#             cls.__table__ = name.lower()
#         return super().__new__(cls, name, bases, dct)

# class BaseSchemas(metaclass=MetaSchemas):
#     @classmethod
#     def get_table(cls):
#         return cls.__table__
    
#     @classmethod
#     def get_schemas(cls)->Dict[str, Schema]:
#         dct:dict = cls.__dict__.copy()
#         [dct.pop(target) for target in ["__module__", "__doc__"]]
#         return dct
    
#     @classmethod
#     def get_schemas_dict(cls):
#         return {key: value.type for key, value in cls.get_schemas().items()}
    
#     @classmethod
#     def get_table_description(cls):
#         return cls.__doc__


from pydantic import BaseModel, Field

def Schema(type:str, desc:str, **kwargs):
    kwargs["type"] = type
    kwargs["desc"] = desc
    return Field(**kwargs, default=None)

class BaseSchemas(BaseModel):
    __table__ = None

    @classmethod
    def get_table(cls):
        if cls.__table__ is None:
            return cls.__name__.lower()
        return cls.__table__
    
    @classmethod
    def get_schemas(cls):
        dct = cls.model_fields
        return {field:info.json_schema_extra['type'] for field, info in dct.items()}
    
    @classmethod
    def set_table_name(cls, table_name:str):
        cls.__table__ = table_name

    @classmethod
    def get_table_description(cls):
        return cls.__doc__