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
        time_range="w",  # past week
        max_results=10,
        include_raw_content=True,
        include_images=False,
        include_answer=True,
        exclude_domains=["some-spammy-site.com", "low-quality-blog.org"],
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
        exclude_domains=["spammy-site.com", "low-quality-blog.org"],
    )
    return (response_default,)


@app.cell
def _(pprint, response_default):
    pprint(response_default)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Module 3 Advanced Tools: Extract, Crawl, Map
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Extract

    - API that extracts full _cleaned_ content of URL
    - page text (and optional images/metadata)
    - Use
        - need entire content for analysis
        - don't want to write custom parsing logic
        - have specific question and want Extract to rerank the most relavant part of page (or limit number of snippets from the source)
    -
    """)
    return


@app.cell
def _(tavily_client):
    extract_response = tavily_client.extract(
        urls=["https://en.wikipedia.org/wiki/Artificial_intelligence"],
        include_images=False,
        include_metadata=True,
        extract_depth="basic",
    )

    for _res in extract_response["results"]:
        print("URL: ", _res["url"])
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
        extract_depth="basic",
        chunks_per_source=3,
        query="What are the main applications of AI?",
    )

    for _res in extract_response_2["results"]:
        print("URL: ", _res["url"])
        print(_res["raw_content"][:300], "...")
    return (extract_response_2,)


@app.cell
def _(extract_response_2):
    extract_response_2["results"][0]["raw_content"]
    return


@app.cell
def _(extract_response_2):
    with open("extract_response.txt", "w") as f:
        f.write(str(extract_response_2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Note: There is a practical limit of up to 20 URLs per Extract request, requests with more than 20 URLs will return a 400 error.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Best Practices

    - 1st search; then extract
    - For dynamic content (media/table etc) use `extract_depth="advanced"`
    - Add a question using `query` parameter; helps with reranking chunks
    - Use `chunck_per_source` (1-5; default 3) to keep `raw_content` small
        - raw_content looks like: `<chunk> [...] <chunk2> [...] <chunk3>`
    - Only <=20 URL at once
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Crawl & Map
    > Currently in Beta
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Crawl**:
    - Graph based site traversal
    - Explore links in parallel
    - Follows hyperlinks and fetched content
    - Useful for scraping and indexing documentation, blogs, products etc.


    **Map**:
    - Walks a site like a graph and returns a list of URL
    - Doesn't extract the content
    - Useful for understanding the structure of a site before paying for full ingestion
        - URL index of documentation, blogs, wikis
        - Understand navigation structure and page hierarchy
        - Used before a Extract or focused crawl step
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    | Crawl Parameter                                   | What It Controls                                                                                                                            |
    |---------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
    | url (string)                                | The base URL from where the crawl begins (root domain or subdomain)                                                                         |
    | max_depth (int)                             | How many link-hops away from the root the crawl can reach (e.g. 1 = only pages directly linked, 2 = pages linked from those pages, etc.)    |
    | max_breadth (int)                           | How many links per page the crawler will follow (i.e. how wide each level of traversal is)                                                  |
    | limit (int)                                 | Total number of links/pages the crawl will process before stopping, useful to cap cost and runtime                                          |
    | select_paths / select_domains (string[])    | Regex filters to include only URLs matching certain path patterns or domains (e.g. /blog/.*, only docs subdomain)                           |
    | exclude_paths / exclude_domains (string[])  | Regex filters to exclude certain paths/domains (e.g. /private/.*, admin pages)                                                              |
    | allow_external (bool)                       | Whether links to external domains are allowed (if you want to stay within the same domain or permit external links)                         |
    | extract_depth (enum: "basic" or "advanced") | Controls how the crawl extracts content from each page: basic may fetch main text; advanced tries to include embedded content, tables, etc. |
    | include_images (bool)                       | Optionally include image data from pages, useful when extracting multimedia or rich content                                                 |
    | instructions (string)                       | Natural language instructions for the crawler.                                                                                              |
    """)
    return


@app.cell
def _(tavily_client):
    crawl_response = tavily_client.crawl(
        url="https://docs.tavily.com",
        max_depth=3,
        max_breadth=30,
        limit=100,
        select_paths=["/documentation/.*", "/sdk/.*"],
        exclude_paths=["/private/.*", "/admin/.*"],
        allow_external=False,
        extract_depth="advanced",
        include_images=False
    )

    for page in crawl_response["results"]:
        print(page["url"])
        print(page["raw_content"][:200], "...")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
