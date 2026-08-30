# Small Learning Projects

This repository contains small Python experiments and learning exercises. They do not follow an overarching theme; each project is a self-contained exploration of an idea, tool, or workflow.

## Notebooks and scripts

The notebooks are written as [Marimo](https://marimo.io/) Python notebooks and can be run as scripts or opened with Marimo.

### Root-level scripts

- [`main.py`](main.py) — Minimal hello-world entry point for the repository.
- [`gemini_share_fetch.py`](gemini_share_fetch.py) — Uses Playwright to fetch a public Gemini share page, extract conversation turns, and write JSON or cleaned Markdown output.

### Marimo notebooks

- [`notebooks/gradient_descent.py`](notebooks/gradient_descent.py) — Generates noisy linear data and compares batch, stochastic, and mini-batch gradient descent, including configurable learning rates, epochs, batch sizes, loss charts, and final parameters.
- [`notebooks/linear_regression_from_scratch.py`](notebooks/linear_regression_from_scratch.py) — Begins an implementation of simple linear regression with NumPy, including coefficient, intercept, and R²-score calculations.
- [`notebooks/hf_rag_tutorial.py`](notebooks/hf_rag_tutorial.py) — Builds a small local retrieval-augmented generation (RAG) chatbot from cat facts, using Ollama embeddings, cosine-similarity retrieval, and an Ollama language model.
- [`notebooks/pinecone_rag.py`](notebooks/pinecone_rag.py) — Loads and reshapes chunked AI arXiv data from Hugging Face, prepares Pinecone access, and records notes about selecting an embedding model for a Pinecone RAG workflow.
- [`notebooks/tavily_cert.py`](notebooks/tavily_cert.py) — Experiments with Tavily search through its Python client and HTTP API, then demonstrates advanced search options, content extraction, and crawl/map operations.

### Pytest learning example

The [`pytest/`](pytest/) directory is a separate hands-on pytest exercise built around a small statistics module:

- [`pytest/stats.py`](pytest/stats.py) — Implements mean, median, variance, standard deviation, and Pearson correlation with input validation.
- [`pytest/conftest.py`](pytest/conftest.py) — Defines shared fixtures, including sample data, setup/teardown behavior, and session-scoped state.
- [`pytest/test_statistics.py`](pytest/test_statistics.py) — Basic assertion-based tests for the statistics functions.
- [`pytest/test_statistics_errors.py`](pytest/test_statistics_errors.py) — Tests expected exceptions with `pytest.raises`.
- [`pytest/test_statistics_fixtures.py`](pytest/test_statistics_fixtures.py) — Demonstrates locally defined fixtures and fixture-based tests.
- [`pytest/test_statistics_markers.py`](pytest/test_statistics_markers.py) — Demonstrates custom markers, skipped tests, unit/integration labels, and marked performance tests.
- [`pytest/test_statistics_parametrized.py`](pytest/test_statistics_parametrized.py) — Uses `pytest.mark.parametrize` to run statistics tests against multiple inputs.
- [`pytest/test_conftest_fixtures.py`](pytest/test_conftest_fixtures.py) — Uses the shared fixtures from `conftest.py`.

See [`pytest/PYTEST_TUTORIAL.md`](pytest/PYTEST_TUTORIAL.md) for the pytest concepts and commands covered by that example.
