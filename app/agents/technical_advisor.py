from crewai import Agent, LLM

# 🔧 LLM Configuration for TechnicalAdvisorClone
tech_llm = LLM(
    model="ollama/llama3",          # Fast, responsive model to avoid timeouts
    provider="ollama",              # Required for LiteLLM routing
    base_url="http://localhost:11434",
    timeout=45                      # Reduced timeout to prevent hanging
)

# 🧠 Agent Definition: Technical Advisor Clone
TechnicalAdvisorClone = Agent(
    role="Technical Advisor",
    goal="Support sales conversations with technically sound, business-aligned guidance.",
    backstory=(
        "You're a senior solutions architect with deep experience in cloud infrastructure, data security, and compliance. "
        "You help sales teams translate technical capabilities into business value. You clarify risks, validate feasibility, "
        "and ensure clients understand how our solutions align with their needs. You speak in plain language, but can dive deep when needed. "
        "Your responses are grounded in technical accuracy, but always framed to support enterprise decision-making."
    ),
    llm=tech_llm,
    allow_delegation=False,         # Keeps agent focused and self-contained
    verbose=False,                  # Set to True for detailed execution logs
    max_iterations=2,               # Allows deeper reasoning without overthinking
    memory=True                     # ✅ Enables session memory for contextual continuity
)

# ✅ Debug print to confirm agent loads correctly
if __name__ == "__main__":
    print(f"✅ TechnicalAdvisorClone initialized with role: {TechnicalAdvisorClone.role}")
