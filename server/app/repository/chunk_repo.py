class ChunkRepo:
    def __init__(self) -> None:
        """only placeholders to complete and for me to call them in other functions"""
        pass

    def add_chunk(self, doc_id: int, content: str, page_num: int, embeddings: list)->None:
        """pushes chunk to database"""
        pass

    def retrieve_chunks(self, text: str, top_k: int) -> list[dict]:
        """list of retrieved chunks from db should be something like {doc_name: xyz, page_number: 2, content: big string} """
        pass