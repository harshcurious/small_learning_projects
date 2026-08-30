import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium", auto_download=["ipynb"])


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from tqdm import tqdm

    return (tqdm,)


@app.cell
def _():
    dataset = []

    with open("data/cat-facts.txt", "r") as file:
        dataset = file.readlines()
        print(f"Loaded {len(dataset)} lines")
    return (dataset,)


@app.cell
def _():
    import ollama

    EMBEDDING_MODEL = "hf.co/CompendiumLabs/bge-base-en-v1.5-gguf"
    LANGUAGE_MODEL = "hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF"

    VECTOR_DB = []

    def add_chunk_to_database(chunk):
        embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)[
            "embeddings"
        ][0]
        VECTOR_DB.append((chunk, embedding))

    return (add_chunk_to_database,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Taking each line to be a chunk
    """)
    return


@app.cell
def _(add_chunk_to_database, dataset, tqdm):
    for i, chunk in enumerate(tqdm(dataset)):
        add_chunk_to_database(chunk=chunk)
    return


@app.function
def cosine_similarity(a, b):
    dot_product = sum([x * y for x, y in zip(a, b)])
    norm_a = sum([x**2 for x in a]) ** 0.5
    norm_b = sum([x**2 for x in b]) ** 0.5
    return dot_product / (norm_a * norm_b)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
