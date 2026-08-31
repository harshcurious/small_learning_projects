import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", auto_download=["ipynb"])


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import os

    return (os,)


@app.cell
def _():
    from datasets import load_dataset

    data = load_dataset("jamescalam/ai-arxiv-chunked", split="train")
    data
    return (data,)


@app.cell
def _(data):
    data[0]
    return


@app.cell
def _(data):
    data.column_names
    return


@app.cell
def _(data):
    data_mapped = data.map(
        lambda x: {
            "id": f"{x['id']}-{x['chunk-id']}",
            "test": x["chunk"],
            "metadata": {
                "title": x["title"],
                "url": x["source"],
                "published": x["published"],
                "primary_category": x["primary_category"],
                "updated": x["updated"],
                "text": x["chunk"],
            },
        }
    )

    data_mapped = data_mapped.remove_columns(
        [
            "title",
            "summary",
            "source",
            "authors",
            "categories",
            "comment",
            "journal_ref",
            "primary_category",
            "published",
            "updated",
            "references",
            "doi",
            "chunk-id",
            "chunk",
        ]
    )
    data_mapped
    return


@app.cell
def _(getpass, os):
    from pinecone import Pinecone

    api_key = os.getenv("PINECONE_API_KEY") or getpass.getpass()

    ps = Pinecone(api_key=api_key)
    return (ps,)


@app.cell
def _():
    from pinecone import ServerlessSpec

    spec = ServerlessSpec(
        cloud="aws", region="us-east-1"
    )
    return (spec,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Picking embedding model based on <https://huggingface.co/spaces/mteb/leaderboard>

    Main choices:
    1. jinaai/jina-embeddings-v5-text-small
    2. jinaai/jina-embeddings-v5-text-nano
    3. google/embeddinggemma-300m

    Going with gemma because the scoring is transparent and popular model
    """)
    return


@app.cell
def _(formatted_texts, os, ps, spec):
    import torch
    import torch.nn.functional as F
    from sentence_transformers import SentenceTransformer

    hf_token = os.getenv("HF_TOKEN")
    model_id = "google/embeddinggemma-300m"
    model = SentenceTransformer(model_id, use_auth_token=hf_token)

    EMBED_DIM = 768
    INDEX_NAME = "gemma-embeddings"

    if not ps.has_index(INDEX_NAME):
        ps.create_index(name=INDEX_NAME, dimension=EMBED_DIM, metric="cosine", spec=spec)

    index = ps.Index(INDEX_NAME)

    # get embeddings (truncate if used)
    def get_truncated_embeddings(
        texts: list[str], target_dim: int = EMBED_DIM
    ) -> list[list[float]]:
        # Generate raw embeddings
        embeddings = model.encode(
            texts, normalize_embeddings=False, convert_to_tensor=True
        )

        # Apply Matryoshka slicing if truncating
        if target_dim < 768:
            embeddings = embeddings[:, :target_dim]
        embeddings = F.normalize(embeddings, p=2, dim=1)

        return embeddings.cpu().tolist()

    # upsert docs
    def upsert_docs(docs: list[dict]):
        formatted_text = [
            f"title: {doc.get('title', 'none')} | text: {doc['text']}"
            for doc in docs
        ]

        vectors_values = get_truncated_embeddings(
            formatted_texts, target_dim=EMBED_DIM
        )

        vectors = []

        for doc, val in zip(docs, vectors_values):
            meta = doc.get("metadata", {})
            meta["text"] = doc["text"]

            vectors.append({"id": doc["id"], "values": val, "metadata": meta})

        index.upset(vectors=vectors)

    def search(query: str, top_k: int = 5):
        formatted_query = f"task: search result | query: {query}"
        query_vector = get_truncated_embeddings(
            [formatted_query], target_dim=EMBED_DIM
        )[0]
        return index.query(
            vector=query_vector, top_k=top_k, include_metadata=True
        )

    return (index,)


@app.cell
def _(data, index):
    from tqdm.auto import tqdm

    batch_size = 100  # how many embeddings we create and insert at once

    for i in tqdm(range(0, len(data), batch_size)):
        passed = False
        # find end of batch
        i_end = min(len(data), i+batch_size)
        # create batch
        batch = data[i:i_end]
        # upsert to Pinecone
        index.upsert_docs()
    return


if __name__ == "__main__":
    app.run()
