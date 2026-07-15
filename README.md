# SmartKart AI Customer Support Assistant

A terminal-based AI customer support chatbot for **SmartKart**, an online store, built with **Python, LangChain, and Google Gemini**. It answers order, product, and delivery questions, calls real business logic (tools) when it needs actual data, and stays scoped strictly to SmartKart support — refusing to answer unrelated general-knowledge or coding questions.

---

## Features

- **Conversational support agent** — understands customer queries in natural language and replies politely and concisely.
- **Tool-calling (function calling)** — Gemini decides when a query needs real data (order status, discount, delivery charge, delivery estimate) and calls the matching Python function instead of guessing.
- **Structured ticket classification** — a separate module labels any customer message with category, priority, sentiment, summary, recommended team, and whether it needs a human agent, using a strict schema (Pydantic).
- **Focused on SmartKart support** — the assistant stays on topic, handling order, product, pricing, and delivery questions rather than general-purpose conversation.
- **Multi-turn memory** — the terminal chat keeps conversation history for the session, so follow-up questions work naturally.
- **Safe by default** — every function validates its own input and fails gracefully with a friendly message instead of crashing or leaking a stack trace to the customer.

---

## Tech Stack

| Component | Purpose |
|---|---|
| [Python 3.10+](https://www.python.org/) | Core language |
| [LangChain](https://www.langchain.com/) | Prompt templates, message types, tool-calling orchestration |
| [langchain-google-genai](https://pypi.org/project/langchain-google-genai/) | Connects LangChain to Google Gemini |
| [Google Gemini](https://ai.google.dev/) (`gemini-2.0-flash`) | The underlying LLM |
| [Pydantic](https://docs.pydantic.dev/) | Structured output schemas (ticket classifier, scope guard) |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Loads the API key from `.env` |

---

## Project Structure

```
smartkart-ai-assistant/
│
├── .env                    # Stores your Gemini API key (not committed)
├── requirements.txt        # Python dependencies
├── config.py                # Sets up the Gemini model connection
├── prompts.py                # System prompt template defining the assistant's rules and scope
├── ticket_classifier.py      # Classifies a message into category/priority/sentiment/etc.
├── tools.py                  # Business logic: order status, discount, delivery charge, delivery time
├── assistant.py               # Core orchestration: scope guard → Gemini → tool calls → final answer
└── main.py                    # Terminal chat interface (entry point)
```

---

## How It Works

```
User types a question
        │
        ▼
 Scope guard checks: is this about SmartKart? ──► No ──► Return fixed redirect message
        │ Yes
        ▼
 Gemini reads the query + conversation history
        │
        ▼
 Does Gemini need real data? ──► No ──► Return Gemini's direct answer
        │ Yes
        ▼
 Python runs the requested tool(s)
 (get_order_status / calculate_discount /
  calculate_delivery_charge / get_estimated_delivery_days)
        │
        ▼
 Tool result(s) sent back to Gemini
        │
        ▼
 Gemini turns the raw result into a natural,
 polite final reply
        │
        ▼
 Reply shown to the customer
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ashutoshkt-code/AI-based-customer-support.git
cd AI-based-customer-support
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API key

Create a `.env` file in the project root (this file is git-ignored and should **never** be committed):

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 5. Run the assistant

```bash
python main.py
```

---

## Usage Example

```
==================================================
   SmartKart Customer Support
   Built by Ashutosh
==================================================
Type your question below. Type 'exit' or 'quit' to stop.

You: What is the status of ORD-1001?
SmartKart Support: Your order ORD-1001 is currently Shipped.

You: A product costs 7500 with an 18% discount, what's the final price?
SmartKart Support: The final price after an 18% discount is ₹6150.00.

You: How long does Express shipping take?
SmartKart Support: Estimated delivery time for Express shipping is 1-2 business days.

You: exit
SmartKart Support: Thank you for chatting with us. Goodbye!
```

---

## Available Tools

| Tool | Description | Example Trigger |
|---|---|---|
| `get_order_status` | Looks up an order's current status by ID | "Where is my order ORD-1002?" |
| `calculate_discount` | Applies a discount percentage to a price | "What's 20% off ₹500?" |
| `calculate_delivery_charge` | Calculates delivery fee based on order value and customer type | "How much is delivery on a ₹1500 order for a Standard customer?" |
| `get_estimated_delivery_days` | Returns estimated delivery time by shipping type | "How long does Express shipping take?" |

Order data is currently mocked in-memory in `tools.py` (`MOCK_ORDERS`) for demonstration purposes; in production this would be replaced by a real database or API call.

---

## Ticket Classification

`ticket_classifier.py` can independently classify any raw customer message into a structured `SupportTicket`:

```python
from ticket_classifier import classify_ticket

result = classify_ticket("I was charged twice for my last order, this is really frustrating.")
print(result)
# category='Billing' priority='High' sentiment='Negative'
# summary='Customer was billed twice for one order.'
# recommended_team='Billing Team' requires_human_agent=True
```

This is useful for routing or logging tickets independently of the live chat flow.

---

## Design Notes

- **Two-model-call pattern for tool use**: Gemini is called once to decide whether a tool is needed, and again after the tool runs, to turn the raw result into a natural sentence. This keeps tool logic (in `tools.py`) completely separate from language generation.
- **Query relevance check runs before the main model**: this keeps the assistant focused on SmartKart support rather than drifting into general-purpose conversation.
- **Every tool validates its own input** and returns a plain string, even on failure — so the customer always sees a clean message, never a raw error.
- **Conversation history is a single in-memory list** for the terminal session — no database is used, since this is a learning/demo project, not a production deployment.

---

## Known Limitations

- Order data is mocked in memory (`MOCK_ORDERS`) and resets every time the app restarts.
- No persistent conversation storage — history is lost when the terminal session ends.
- Single-user, terminal-only interface (no web UI or multi-session support).
- Topic-relevance detection is best-effort and can occasionally misclassify an edge-case query.

---

## Author

Built by **Ashutosh** as a structured learning project covering LangChain, LLM tool-calling, structured outputs, and prompt design.
