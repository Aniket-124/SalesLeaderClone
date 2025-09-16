import os
import yaml
import json
from crewai import Crew, Task
from sentence_transformers import SentenceTransformer, util
from app.agents.sales_leader import SalesLeaderClone
from app.agents.technical_advisor import TechnicalAdvisorClone

YAML_PATH    = "app/config/sales_tasks.yaml"
MEMORY_PATH  = os.getenv("SALES_MEMORY_PATH", "sales_memory.json")
MAX_HISTORY  = 5
EMBED_MODEL  = "all-MiniLM-L6-v2"

# --- Robust YAML loading with error handling ---
try:
    with open(YAML_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f)
        TASKS = data.get("tasks", []) if data else []
except Exception as e:
    print(f"❌ Failed to load YAML: {e}")
    TASKS = []

embedder    = SentenceTransformer(EMBED_MODEL)
DESCRIPTIONS = [t["description"] for t in TASKS]
DESC_EMBS    = embedder.encode(DESCRIPTIONS, convert_to_tensor=True) if DESCRIPTIONS else []

def load_memory(path=MEMORY_PATH):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_memory(entry, path=MEMORY_PATH):
    history = load_memory(path)
    history.append(entry)
    history = history[-MAX_HISTORY:]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def format_memory(history):
    lines = []
    for item in history:
        lines.append(f"Q: {item['question']}\nA: {item['answer']}")
    return "\n\n".join(lines)

def match_task_to_question(tasks, question):
    if DESC_EMBS is None or len(DESC_EMBS) == 0:
        raise RuntimeError("No task descriptions loaded for semantic matching.")
    q_emb = embedder.encode(question, convert_to_tensor=True)
    sims  = util.cos_sim(q_emb, DESC_EMBS)[0]
    best  = int(sims.argmax())
    return tasks[best]

def load_sales_tasks(question):
    selected = match_task_to_question(TASKS, question)
    agent_cls = (
        SalesLeaderClone
        if selected.get("agent", "sales_leader") == "sales_leader"
        else TechnicalAdvisorClone
    )
    return Task(
        description=selected["description"],
        expected_output=selected["expected_output"],
        agent=agent_cls,
        return_final_answer=True
    )

def run_sales_clone(message: str):
    history = load_memory()
    context = format_memory(history)
    if context:
        prompt = f"Previous conversation:\n{context}\n\nNew question: {message}"
    else:
        prompt = message

    try:
        task = load_sales_tasks(prompt)
        crew = Crew(agents=[SalesLeaderClone, TechnicalAdvisorClone], tasks=[task], verbose=False)
        answer = crew.kickoff()
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"⚠️ SalesLeaderClone encountered an error: {e}"

    answer = str(answer).strip()
    save_memory({"question": message, "answer": answer})
    return answer