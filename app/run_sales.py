import time
from app.crew_sales import run_sales_clone

def main():
    print("\n🧠 SalesLeaderClone & TechnicalAdvisorClone are ready to help you close enterprise deals.")
    print("💡 Tip: Ask about BPO positioning, consulting coaching, accounting strategies, or technical objections.\n")

    while True:
        question = input("💬 Enter your sales question (or type 'exit' to quit): ").strip()

        if question.lower() == "exit":
            print("\n👋 Session ended. Good luck closing those deals, Muskan!")
            break

        if not question:
            print("⚠️ No input received. Please enter a valid question.\n")
            continue

        print("🚀 Routing your question to the right expert...")

        start_time = time.time()
        try:
            answer = run_sales_clone(question)
            duration = round(time.time() - start_time, 2)

            print(f"\n✅ Response generated in {duration} seconds")
            print("\n🎯 Answer:\n", answer.strip() if answer else "⚠️ No response returned.")
        except Exception as e:
            print(f"\n❌ Agent execution failed: {str(e)}")
            print("⚠️ Try restarting Ollama, simplifying your input, or checking your agent setup.\n")

if __name__ == "__main__":
    main()