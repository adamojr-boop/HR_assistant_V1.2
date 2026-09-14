class MockCollection:
    def __init__(self):
        self.items = []

    def get(self, ids=None, where=None, limit=None, offset=None, include=None):
        metadatas = [item["metadata"] for item in self.items if "metadata" in item]
        ids_list = [item["id"] for item in self.items if "id" in item]
        documents = [item["document"] for item in self.items if "document" in item]
        
        res = {}
        if include:
            if "metadatas" in include:
                res["metadatas"] = metadatas
            if "documents" in include:
                res["documents"] = documents
            if "ids" in include:
                res["ids"] = ids_list
        else:
            res = {"ids": ids_list, "metadatas": metadatas, "documents": documents}
        return res

    def add(self, documents, metadatas=None, ids=None):
        for i, doc in enumerate(documents):
            doc_id = ids[i] if ids and i < len(ids) else str(len(self.items))
            meta = metadatas[i] if metadatas and i < len(metadatas) else {}
            self.items.append({"id": doc_id, "document": doc, "metadata": meta})

    def query(self, query_texts, n_results=2, include=None):
        docs = [item["document"] for item in self.items]
        metas = [item["metadata"] for item in self.items]
        return {
            "documents": [docs[:n_results]],
            "metadatas": [metas[:n_results]],
            "distances": [[0.1] * min(n_results, len(docs))]
        }

class Database:
    def __init__(self, collection_name="hr_resumes"):
        self.collection_name = collection_name
        self._collection = MockCollection()

    def get_or_create_collection(self, name=None):
        return self._collection

    def get_collection(self):
        return self._collection