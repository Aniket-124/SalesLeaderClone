import os
from crewai import Agent, LLM

# ─── Environment-Driven LLM Configuration ────────────────────────────────────────
SALES_MODEL   = os.getenv("SALES_MODEL", "ollama/phi3")  # Changed from "ollama/phi3-mini" to "ollama/phi3"
SALES_PROVIDER = os.getenv("SALES_PROVIDER", "ollama")
SALES_BASE_URL = os.getenv("SALES_BASE_URL", "http://localhost:11434")
SALES_TIMEOUT  = int(os.getenv("SALES_TIMEOUT", "1200"))

sales_llm = LLM(
    model=SALES_MODEL,
    provider=SALES_PROVIDER,
    base_url=SALES_BASE_URL,
    timeout=SALES_TIMEOUT
)

# ─── Agent Definition: Sales Leader Clone ────────────────────────────────────────
SalesLeaderClone = Agent(
    role="Sales Leader",
    goal="Provide tactical advice to sales and consulting leaders to help them close enterprise deals.",
    backstory=(
        "You're a seasoned sales strategist with over two decades in enterprise sales. You hold an MBA focused on sales strategy, "
        "and you're known for clear, concise communication. You specialize in management consulting, BPO, and accounting. "
        "You mentor sales teams and provide actionable guidance, especially to junior reps. You prioritize clarity, relevance, "
        "and brevity. You avoid unnecessary flourish and deliver the most salient points upfront. If asked, you expand with justifications."
    ),
    llm=sales_llm,
    allow_delegation=False,         # Keeps agent focused and self-contained
    verbose=False,                  # Set to True for detailed execution logs
    max_iterations=2,               # Allows deeper reasoning without overthinking
    memory=True                     # ✅ Enables session memory for contextual continuity
)

# ✅ Debug print to confirm agent loads correctly
if __name__ == "__main__":
    print(f"✅ SalesLeaderClone initialized with model: {sales_llm.model}")