import uuid
import pymupdf4llm
from arai.agents.base import OfflineAgent
from arai.utils.utils import Document


class DocumentParser(OfflineAgent):
    def __init__(self):
        super().__init__()
    
    def load_document(self, document_path:str):
        pages = pymupdf4llm.to_markdown(document_path, page_chunks=True)
        documents = [
            Document(
                id=str(uuid.uuid4()), 
                page_content=page['text'], 
                metadata=dict(
                    page=page['metadata']['page'],
                    source=page['metadata']['file_path']
                ),
                type="document"
            ) 
            for page in pages
        ]
        first_page = documents[0]
        self.event_bus.publish("summary_needed", {"first_page": first_page})
        self.event_bus.publish("chunking_needed", {"documents": documents})
