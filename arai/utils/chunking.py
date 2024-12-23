from typing import List
from arai.utils.utils import Document

class CustomChunker:
    def __init__(self, chunk_size:int, overlap:int):
        self.chunk_size = self.validate_chunk_size(chunk_size)
        self.overlap = self.validate_overlap(overlap)
        self.start_idx = 0
        self.end_idx = self.validate_chunk_size(chunk_size)
        self.offset = 0
        self.doc_offset = 0
        self.doc_idx = 0
        self.max_documents = 0
        self.chunks:List[str] = []

    def validate_chunk_size(self, chunk_size):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")
        return chunk_size

    def validate_overlap(self, overlap):
        if overlap <= 0:
            raise ValueError("overlap must be greater than 0")
        if self.chunk_size <= overlap:
            raise ValueError("overlap must be less than chunk_size")
        return overlap

    def chunk_forward(self):
        last_chunk = self.chunks[-1].split(" ")
        self.offset = 0 # reset offset here, so chunk_backward will have the right reference if last chunk completes the chunk_size
        while True:
            gap = self.chunk_size - len(last_chunk)
            self.doc_idx += 1
            if gap <= 0:
                break
            if self.doc_idx == self.max_documents:
                break
            content = self.documents[self.doc_idx].page_content.split(" ")
            self.offset = gap
            fill = content[:self.offset]
            last_chunk = last_chunk + fill
        self.chunks[-1] = " ".join(last_chunk)

    def chunk_backward(self):
        if self.doc_idx > 0:
            self.offset += self.chunk_size - self.overlap
            first_chunk = self.content[:self.offset]
            self.start_idx = self.offset - self.overlap
            self.end_idx = self.start_idx + self.chunk_size
            self.doc_offset = self.doc_idx - 1
            while self.doc_offset >= 0:
                if len(first_chunk) >= self.chunk_size:
                    gap = len(first_chunk) - self.chunk_size
                    first_chunk = first_chunk[gap:]
                    break
                gap = self.chunk_size - len(first_chunk)
                if gap <= 0:
                    break
                prev_content = self.documents[self.doc_offset].page_content.split(" ")
                fill = prev_content[-gap:]
                first_chunk = fill + first_chunk
                self.doc_offset -= 1
            self.chunks.append(" ".join(first_chunk))

    def chunk_normal(self):
        while True:
            chunk = " ".join(self.content[self.start_idx:self.end_idx])
            self.chunks.append(chunk)
            if self.end_idx > len(self.content):
                break
            self.start_idx = self.end_idx - self.overlap
            self.end_idx = self.start_idx + self.chunk_size

    def chunk_end(self):
        if len(self.chunks)>1:
            last_chunk = self.chunks[-1].split(" ")
            if len(last_chunk) < self.overlap:
                self.chunks.pop(-1)
                self.chunks[-1] = " ".join(self.chunks[-1].split(" ") + last_chunk)

    def clear(self):
        self.start_idx = 0
        self.end_idx = self.chunk_size
        self.offset = 0
        self.doc_offset = 0
        self.doc_idx = 0
        self.max_documents = 0
        return self.chunks

    def run(self, documents:List[Document])->List[str]:
        self.chunks:List[str] = []
        self.documents = documents
        self.max_documents = len(documents)
        while self.doc_idx < self.max_documents:
            self.content = documents[self.doc_idx].page_content.split(" ")
            self.chunk_backward()
            self.chunk_normal()
            self.chunk_forward()
        self.chunk_end()
        return self.clear()
    
    def check_chunks(self):
        for enum, chunk in enumerate(self.chunks):
            print(f"chunk {enum} with size {len(chunk.split(' '))}")