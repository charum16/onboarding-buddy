class Prompt:
    def __init__(self) -> None:
        pass
    def rephraser(self, user_query: str, history: list) -> str:
        prompt = f""" you're a rephraser this is the user query {user_query} and this is the history {history}"""
        return prompt

    def augmenter(self, user_query: str, history: list, chunks: list)->str:
        prompt = f"""  you're a query augmenter this is the user query {user_query} and this the history {history} and these are the chunks {chunks}"""
        return prompt