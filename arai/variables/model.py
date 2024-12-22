import json
from pydantic import BaseModel, Field

def extract_content(input_str: str) -> str:
    start = input_str.find('{') + 1
    end = input_str.rfind('}')
    if start == 0 or end == -1 or start >= end:
        return ""  # Return an empty string if the braces are not found or in the wrong order
    return input_str[start:end]

def extract_json_from_codeblock(content: str) -> str:
    # content = content.split("```json")[1]
    # content = content.split("```")[0]
    first_paren = content.find("{")
    last_paren = content.rfind("}")
    return content[first_paren : last_paren + 1]

def BroField(description:str, default:str, **kwargs):
    kwargs['example'] = default
    return Field(description=description, default=default, **kwargs)

class BroModel(BaseModel):
    @classmethod
    def get_instruction(cls):
        instruction = {
            name:annotation.description
            for name, annotation
            in cls.model_fields.items()
        }
        return instruction

    @classmethod
    def get_example(cls):
        example = {
            name:annotation.json_schema_extra['example']
            for name, annotation
            in cls.model_fields.items()
        }
        return example

    @classmethod
    def as_prompt(cls):
        prompt = []
        prompt.append("Remember always return your response in a code block with the correct JSON schema format because your response will be used later in the next stage.")
        prompt.append("Use this JSON schemas: ")
        prompt.append(json.dumps(cls.get_instruction()))
        prompt.append("Example of the response: ")
        prompt.append(
            "```json\n\n" + json.dumps(cls.get_example()) + "\n\n```"
        )
        return "\n\n".join(prompt)

    @classmethod
    def from_json(cls, json_str:str):
        json_str = extract_json_from_codeblock(json_str)
        return cls.model_validate_json(json_str)