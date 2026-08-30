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
    data_mapped = data.map(lambda x: {
        "id": f"{x['id']}-{x['chunk-id']}",
        "test": x["chunk"], 
        "metadata": {
            "title": x["title"],
            "url": x["source"],
            "published":x["published"],
            "primary_category":x["primary_category"],
            "updated":x["updated"],
            "text":x["chunk"],
        }
    })

    data_mapped = data_mapped.remove_columns(["title", "summary", "source",
        "authors", "categories", "comment",
        "journal_ref", "primary_category",
        "published", "updated", "references",
        "doi", "chunk-id",
        "chunk"])
    data_mapped
    return


@app.cell
def _(getpass, os):
    from pinecone import Pinecone

    api_key = os.getenv("PINECONE_API_KEY") or getpass.getpass()

    ps = Pinecone(api_key=api_key)
    return


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
def _():
    return


if __name__ == "__main__":
    app.run()
