from src.menus._menu import Menu
from util._session import Session

class EmbeddingsMenu(Menu):
    def __init__(self, session:Session, parent: Menu = None):
        is_root = False
        is_leaf = True
        options = [
            "all-MiniLM-L6-v2",
            "all-MiniLM-L12-v2",
            "multi-qa-MiniLM-L6-cos-v1",
            "all-mpnet-base-v2",
            "Muennighoff/SGPT-125M-weightedmean-msmarco-specb-bitfit",
            "Muennighoff/SGPT-125M-weightedmean-nli-bitfit",
            "Muennighoff/SGPT-1.3B-weightedmean-msmarco-specb-bitfit",
        ]

        self.name = "Embeddings"

        super().__init__(session, options, is_leaf, is_root, name=self.name)

