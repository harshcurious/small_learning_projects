import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from pprint import pprint

    return (pprint,)


@app.cell
def _():
    import os
    from dotenv import load_dotenv

    # Load variables from .env file into os.environ
    load_dotenv()
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    return (TAVILY_API_KEY,)


@app.cell
def _(TAVILY_API_KEY, pprint):
    from tavily import TavilyClient

    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

    response = tavily_client.search("Who is Leo Messi?")

    pprint(response)
    return (tavily_client,)


@app.cell
def _(TAVILY_API_KEY, pprint):
    import requests

    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
    }

    response_post = requests.post(
        "https://api.tavily.com/search",
        json={"query": "Who is Leo Messi?"},
        headers=headers,
    )

    pprint(response_post.json())
    return


@app.cell
def _(pprint, tavily_client):
    _response = tavily_client.search(
        query="latest trends in generative AI 2026",
        search_depth="advanced",
        topic="news",
        time_range="w",        # past week
        max_results=10,
        include_raw_content=True,
        include_images=False,
        include_answer=True,
        exclude_domains=["some-spammy-site.com","low-quality-blog.org"]
    )

    for res in _response["results"]:
        print(res["title"], res["url"])
        print(res["content"][:200], "...")

    pprint(_response)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Use as default format for research agent
    """)
    return


@app.cell
def _(tavily_client):
    # from tavily import TavilyClient

    # tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

    response_default = tavily_client.search(
        query="2026 trends in web-agent search APIs",
        search_depth="advanced",
        max_results=10,
        include_raw_content=True,
        include_images=False,
        include_answer=False,
        exclude_domains=["spammy-site.com","low-quality-blog.org"]
    )
    return (response_default,)


@app.cell
def _(pprint, response_default):
    pprint(response_default)
    return


@app.cell(hide_code=True)
def _():
    ## Module 3 Advanced Tools: Extract, Crawl, Map

    return


app._unparsable_cell(
    r"""
    ## Extract

    - API that extracts full _cleaned_ content of URL
    - page text (and optional images/metadata)
    - Use
        - need entire content for analysis
        - don't want to write custom parsing logic
        - have specific question and want Extract to rerank the most relavant part of page (or limit number of snippets from the source)
    - 
    """,
    column=None, disabled=False, hide_code=True, name="_"
)


@app.cell
def _(tavily_client):
    extract_response = tavily_client.extract(
        urls=["https://en.wikipedia.org/wiki/Artificial_intelligence"],
        include_images=False,
        include_metadata=True,
        extract_depth='basic'
    )

    for _res in extract_response["results"]:
        print('URL: ', _res["url"])
        print(_res["raw_content"][:300], "...")
    return (extract_response,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Expected Response Structure:
    ```
    {
      "results": [
        {
          "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
          "raw_content": "Artificial intelligence (AI) is intelligence demonstrated by machines...",
          "images": [],
          // possibly other metadata fields
        }
      ],
      "failed_results": [],
      "response_time": 0.8
    }
    ```
    """)
    return


@app.cell
def _(extract_response):
    extract_response["results"][0]["raw_content"]
    return


@app.cell
def _(extract_response):
    extract_response["response_time"]
    return


@app.cell
def _(tavily_client):
    extract_response_2 = tavily_client.extract(
        urls=["https://en.wikipedia.org/wiki/Artificial_intelligence"],
        include_images=False,
        include_metadata=True,
        extract_depth='basic',
        chunks_per_source=3,
        query="What are the main applications of AI?",
    )

    for _res in extract_response_2["results"]:
        print('URL: ', _res["url"])
        print(_res["raw_content"][:300], "...")
    return (extract_response_2,)


@app.cell
def _(extract_response_2):
    extract_response_2["results"][0]["raw_content"]
    return


@app.cell
def _(extract_response_2):
    with open("extract_response.txt", 'w') as f:
        f.write(str(extract_response_2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Note: There is a practical limit of up to 20 URLs per Extract request, requests with more than 20 URLs will return a 400 error.
    """)
    return


app._unparsable_cell(
    r"""
    ### Best Practices

    - 1st search; then extract
    - For dynamic content (media/table etc) use `extract_depth="advanced"`
    - Add a question using `query` parameter; helps with reranking chunks
    - Use `chunck_per_source` (1-5; default 3) to keep `raw_content` small
        - raw_content looks like: `<chunk> [...] <chunk2> [...] <chunk3>`
    - Only <=20 URL at once
    """,
    column=None, disabled=False, hide_code=True, name="_"
)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
