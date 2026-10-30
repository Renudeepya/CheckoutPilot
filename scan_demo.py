"""Day 1: CheckoutPilot's first LangGraph agent.

A tiny 2-step graph that mirrors the real project:
  scan   -> Claude reads a store's checkout HTML and lists missing PayPal features
  report -> turns that list into a short merchant-friendly summary
"""
import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END

load_dotenv(override=True)  # reads ANTHROPIC_API_KEY (and others) from .env

# Small, cheap model for development. Change in .env without touching code.
llm = ChatAnthropic(model=os.getenv("MODEL", "claude-haiku-5-5"), max_tokens=2000)
# A deliberately outdated checkout page: one basic PayPal button, nothing else.
SAMPLE_STORE_HTML = """
<h1>Maple & Moss Candles</h1>
<div class="product">Lavender Candle - $24 <button>Add to cart</button></div>
<div class="cart">
  Total: $24
  <form action="https://www.paypal.com/cgi-bin/webscr" method="post">
    <input type="hidden" name="cmd" value="_xclick">
    <input type="submit" value="Pay with PayPal">
  </form>
</div>
"""


class State(TypedDict):
    html: str
    gaps: str
    report: str


def scan(state: State) -> dict:
    """Step 1: find what's missing in the store's PayPal setup."""
    msg = llm.invoke(
        "You are CheckoutPilot, an expert in PayPal checkout integrations. "
        "List the 3 most important PayPal checkout improvements this store is missing "
        "(for example: modern PayPal buttons, Pay Later messaging, PayPal on product pages). "
        "One short line each, no intro.\n\nSTORE HTML:\n" + state["html"]
    )
    return {"gaps": msg.text}


def report(state: State) -> dict:
    """Step 2: explain the findings to a non-technical shop owner."""
    msg = llm.invoke(
        "Rewrite these findings as a friendly 3-bullet note to a small shop owner. "
        "Explain why each one could bring more sales. Keep it under 80 words.\n\n" + state["gaps"]
    )
    return {"report": msg.text}


# Build the graph: START -> scan -> report -> END
graph = StateGraph(State)
graph.add_node("scan", scan)
graph.add_node("report", report)
graph.add_edge(START, "scan")
graph.add_edge("scan", "report")
graph.add_edge("report", END)
app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({"html": SAMPLE_STORE_HTML})
    print("\n=== GAPS FOUND (scan step) ===\n" + result["gaps"])
    print("\n=== MERCHANT REPORT (report step) ===\n" + result["report"])