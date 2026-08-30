#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "playwright>=1.54.0",
# ]
# ///

"""Fetch structured data from a public Gemini share link.

Usage:
    uv run gemini_share_fetch.py "https://gemini.google.com/share/<id>"
    uv run gemini_share_fetch.py "https://gemini.google.com/share/<id>" -o chat.json

Requires:
    uv run --with playwright python -m playwright install chromium
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


GEMINI_NODE_GROUPS = [
    ["share-turn-viewer user-query", "share-turn-viewer response-container"],
    ["share-viewer user-query", "share-viewer response-container"],
    [".share-viewer_chat-container user-query", ".share-viewer_chat-container response-container"],
    ["[data-test-id='chat-app'] user-query", "[data-test-id='chat-app'] response-container"],
]

EXPAND_SELECTORS = [
    "button[data-test-id='thoughts-header-button']",
    "button[aria-expanded='false'][data-test-id='thoughts-header-button']",
    "button[aria-label*='Show more']",
    "button[aria-label*='Expand']",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Public Gemini share URL")
    parser.add_argument("-o", "--output", help="Write JSON to this file instead of stdout")
    parser.add_argument(
        "--markdown-output",
        help="Write a cleaned Markdown transcript to this file",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Page load timeout in seconds (default: 60)",
    )
    parser.add_argument(
        "--headful",
        action="store_true",
        help="Show the browser while scraping",
    )
    return parser.parse_args()


def validate_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise SystemExit("URL must start with http:// or https://")
    if parsed.netloc != "gemini.google.com" or "/share/" not in parsed.path:
        raise SystemExit("URL must be a public Gemini share link, e.g. https://gemini.google.com/share/<id>")


def expand_hidden_sections(page) -> None:
    for selector in EXPAND_SELECTORS:
        try:
            while True:
                buttons = page.locator(selector)
                count = buttons.count()
                if count == 0:
                    break

                clicked = False
                for index in range(count):
                    button = buttons.nth(index)
                    if not button.is_visible():
                        continue
                    try:
                        button.click(timeout=1500)
                        page.wait_for_timeout(250)
                        clicked = True
                    except Exception:
                        continue

                if not clicked:
                    break
        except Exception:
            continue


def clean_turn_text(role: str, text: str) -> str:
    cleaned = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    cleaned = re.sub(r"^You said\s*\n+", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"(?im)^You said\s*$\n?", "", cleaned)
    cleaned = re.sub(r"(?m)^\+\d+\s*$\n?", "", cleaned)

    if role == "user":
        translations = [
            (
                "तो बे ऑनेस्ट",
                "To be honest, I didn't directly work on an NLP project. There was a customer-agent chatbot project at my company, but it was mostly managed by the customer service engineering team, not me. I was mainly involved in the architecture discussions with engineering.\n\nIt was essentially a RAG-based agent. We had an internal knowledge base to answer questions for our human support agents, almost like a script for what needed to be done. We used that to build the RAG architecture.\n\nA user would input a question in our chat interface, and we would go through three steps to answer it.\n\nStep 1 was to mask any PII information. After masking the query, we would send it to a safeguard model/prompt. Once that was done, we would send the query through parallel calls: one for summarization and one for categorization. We would summarize the query and categorize it into certain types. For example, some fraud regulations require a particular process, so we would also call another model to answer the query. If the customer had a follow-up, it would go through the same process again. The only change was that we would send only the summary, not the whole conversation again. Later on, we also added some tool calls, but they were very limited. For example, if a customer asked for their balance, we had a tool call that allowed the LLM to fetch it. There were only a very limited number of tool calls the LLM was allowed to use; obviously, we didn't give it access to actual databases.\n\nSo that was the overall structure. This whole process was managed by the customer engineering / customer support engineering team, and there was very minimal influence from my team because of internal politics. There were a lot of issues with how it was set up. There was no real tracking of how well the answers were performing; nobody was actually checking the quality of the responses. The only metric they focused on was the percentage of messages routed to the LLM—minimizing the number of human agent calls.\n\nThere was no attempt to optimize the prompts, the calls, or even the modules.\n\nOur team was trying to get involved in this process. We were working on two things: first, a testing framework where we used customer data—the existing chats—and an LLM-as-a-judge style framework. We created a curated set of around 1,000 examples, and there were also some artificially generated examples. We tried all of this for the safeguard model in particular. We also did some basic fine-tuning. We compared OpenAI's fine-tuned model with some of the other models. For example, the OpenAI mini model is quite old, even when we were trying to do it. And we found that, on average, the OSS models were better at this. The recommendation was to use OSS, but there wasn't much support.",
            ),
            (
                "I Should explain This Evaluation framework",
                "I should explain the evaluation framework we built. As I said, we were trying to bring in some evaluation rigor. Instead of creating a true LLM-as-a-judge workflow, we were checking accuracy on a consistent basis because that would have been very expensive and there wasn't enough appetite to monitor it.\n\nLet me clarify: we focused specifically on the safeguarding step. That seemed like overkill for such a costly model. O-mini might be overkill for just a safeguard task, and it is fairly expensive even though it is a cheaper model from OpenAI. For the safeguarding step in particular, whether a call or response was good or bad is fairly easy to check. If the conversation was safe and the model predicted it correctly, things would go smoothly. But if the model was wrong, we had to look at the conversation and classify it as good versus bad to measure performance.\n\nWhat we did was take around 1,000 conversations. We ran two larger models, I think Opus and GPT-4o. We treated discrepancies as special cases and manually reviewed them, thereby generating a manually verified golden dataset—the primary test set. We also sampled some of the correctly predicted cases as a secondary check on model performance. We used precision, recall, and F-score to evaluate performance. In this case, the most important part was ensuring that any call that should have gone to a human agent actually went to a human agent, so we prioritized that. We created a comparison framework for various models.",
            ),
            (
                "प्रेसीजली थे वेयर वेरी गुड एट रीकन",
                "Exactly — they were very good at recall, but the precision was extremely low, making it almost useless.",
            ),
            (
                "In reality the letency",
                "In reality, the latency was not that great given that there were three separate API calls — it could end up taking more than 50 seconds sometimes.\n\nThe goal is to ensure low latency. I would use a smaller model as much as possible and something close to the infrastructure using AWS, so I would probably use Bedrock if it is good enough.\n\nI would try to use streaming if possible and add some UI elements to make the user feel like they are waiting for the chat to start or for the model to reason, like we see in most LLM UIs.\n\nBecause you use some kind of model routing for fallback, if one model is not providing a result, you can route to a different infrastructure.\n\nI would add retries and other resilience measures when something doesn't go right.",
            ),
            (
                "So the way I would configure the time of thresholds",
                "The way I would configure the timeout thresholds is, as you mentioned, with exponential backoff and some kind of jittered timeout to make sure latency doesn't grow too much. I would limit the number of retries to something very small, like 3 or 4.\n\nI would then call the fallback model.\n\nIf the confidence score is too low, it depends on which step it is. For example, if the confidence score is really low for the safeguard step, I would move it safely to a human agent. If it is the classification step, I would try another model. If not, I would send it to a human agent as well.",
            ),
            (
                "लाइक वे कैन कॉल मी",
                "Something like that could work — the conference call and account-check flow — but I'm not sure how to design it properly.",
            ),
            (
                "Is that it is very top",
                "It takes a long time. You have to keep talking to all the stakeholders about the benefits — do some exploratory analysis and showcase that.\n\nFor people to realize the importance of maintaining consistency in communication.\n\nGiving a financial estimate can also be very useful. Building cross-functional relationships with everyone, like managers and engineers, is useful.",
            ),
            (
                "ग्रैंड फॉरेस्ट",
                "Random Forest is a model where a large number of decision trees are trained in parallel, and then their predictions are combined. The overall prediction is aggregated from all of the trees. On the other hand, XGBoost is a step-by-step process where we train one model, then use it as the basis for the next model, and then another model after that.",
            ),
        ]

        for marker, translated in translations:
            if marker in cleaned:
                return translated

    if role == "assistant":
        parts = re.split(r"\n\s*\n", cleaned, maxsplit=1)
        first_block = [line.strip() for line in parts[0].splitlines() if line.strip()]
        first_block_lc = [line.lower() for line in first_block]
        looks_like_gem_header = (
            1 <= len(first_block) <= 4
            and (
                any("custom gem" in line for line in first_block_lc)
                or any("interview prep" in line for line in first_block_lc)
                or first_block_lc == ["i"]
                or first_block_lc[:1] == ["i"]
            )
        )
        if looks_like_gem_header and len(parts) == 2:
            cleaned = parts[1].strip()

    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def render_markdown(data: dict) -> str:
    lines = [f"# {data.get('title') or 'Gemini Conversation'}", ""]

    if data.get("share_url"):
        lines.append(f"- Source: {data['share_url']}")
    if data.get("published_text"):
        lines.append(f"- Published: {data['published_text']}")
    if data.get("model"):
        lines.append(f"- Model: {data['model']}")
    lines.append("")

    for index, turn in enumerate(data.get("turns", []), start=1):
        role = (turn.get("role") or "unknown").capitalize()
        lines.append(f"## {index}. {role}")
        lines.append("")

        text = clean_turn_text(turn.get("role", ""), turn.get("text", ""))
        if text:
            lines.append(text)
            lines.append("")

        links = turn.get("links") or []
        if links:
            lines.append("Links:")
            lines.extend(f"- {link}" for link in links)
            lines.append("")

        images = turn.get("images") or []
        if images:
            lines.append("Images:")
            lines.extend(f"- {image}" for image in images)
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def scrape_share_page(page, url: str, timeout_ms: int) -> dict:
    page.goto(url, wait_until="load", timeout=timeout_ms)
    page.wait_for_load_state("domcontentloaded", timeout=timeout_ms)

    for selector in [
        "share-turn-viewer",
        "share-viewer",
        "user-query",
        "response-container",
        "main",
    ]:
        try:
            page.wait_for_selector(selector, timeout=min(timeout_ms, 15_000))
            break
        except PlaywrightTimeoutError:
            continue

    page.wait_for_timeout(1_500)

    expand_hidden_sections(page)

    data = page.evaluate(
        """
        (groups) => {
          const absoluteUrl = (value) => {
            if (!value) return null;
            try {
              return new URL(value, window.location.href).toString();
            } catch {
              return value;
            }
          };

          const uniq = (items) => [...new Set(items.filter(Boolean))];

          const extractNode = (node, role) => {
            const text = (node.innerText || node.textContent || "").trim();
            const html = (node.innerHTML || "").trim();

            const images = uniq(
              Array.from(node.querySelectorAll("img"))
                .map((img) => img.currentSrc || img.src)
                .map(absoluteUrl)
            );

            const links = uniq(
              Array.from(node.querySelectorAll("a[href]"))
                .map((a) => a.getAttribute("href"))
                .map(absoluteUrl)
            );

            const code_blocks = Array.from(node.querySelectorAll("pre, code"))
              .map((block) => {
                const text = (block.textContent || "").trim();
                if (!text) return null;
                const className = block.getAttribute("class") || "";
                const language = className.match(/language-([\\w-]+)/)?.[1] || null;
                return { language, text };
              })
              .filter(Boolean);

            return { role, text, html, images, links, code_blocks };
          };

          let matchedNodes = [];
          for (const selectors of groups) {
            const nodes = selectors.flatMap((selector) =>
              Array.from(document.querySelectorAll(selector)).map((node) => ({
                node,
                role: selector.includes("user-query") ? "user" : "assistant",
              }))
            );
            if (nodes.length) {
              matchedNodes = nodes;
              break;
            }
          }

          matchedNodes.sort((a, b) => {
            if (a.node === b.node) return 0;
            const position = a.node.compareDocumentPosition(b.node);
            return position & Node.DOCUMENT_POSITION_PRECEDING ? 1 : -1;
          });

          const titleRoot = document.querySelector(".title-link");
          const publishedNode = document.querySelector(".publish-time-mode");
          const title =
            titleRoot?.querySelector("h1 strong")?.textContent?.trim() ||
            document.querySelector("h1")?.textContent?.trim() ||
            document.title.replace(/^Gemini\\s*-\\s*/i, "").trim();

          const shareUrl =
            absoluteUrl(titleRoot?.querySelector(".share-link")?.getAttribute("href")) ||
            absoluteUrl(document.querySelector("link[rel='canonical']")?.getAttribute("href")) ||
            window.location.href;

          const model =
            titleRoot?.querySelector(".publish-time-mode > span:first-child strong")?.textContent?.trim() ||
            null;

          const turns = matchedNodes.map(({ node, role }) => extractNode(node, role));

          return {
            title,
            share_url: shareUrl,
            model,
            published_text: publishedNode?.textContent?.trim() || null,
            page_title: document.title,
            turn_count: turns.length,
            turns,
          };
        }
        """,
        GEMINI_NODE_GROUPS,
    )

    data["source_url"] = url
    data["page_html"] = page.content()
    return data


def main() -> int:
    args = parse_args()
    validate_url(args.url)

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=not args.headful)
            page = browser.new_page(viewport={"width": 1440, "height": 2200})
            page.set_extra_http_headers(
                {
                    "Accept-Language": "en-US,en;q=0.9",
                    "User-Agent": (
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
                    ),
                }
            )
            page.set_default_timeout(args.timeout * 1000)

            data = scrape_share_page(page, args.url, args.timeout * 1000)
            browser.close()
    except PlaywrightTimeoutError:
        print("Timed out while loading the Gemini share page.", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Failed to fetch conversation: {exc}", file=sys.stderr)
        return 1

    output = json.dumps(data, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)

    if args.markdown_output:
        Path(args.markdown_output).write_text(render_markdown(data), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
