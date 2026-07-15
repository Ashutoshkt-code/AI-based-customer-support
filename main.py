from assistant import customer_support_assistant

def main():
    print("=" * 50)
    print("   SmartKart Customer Support")
    print("   Built by Ashutosh")
    print("=" * 50)
    print("Type your question below. Type 'exit' or 'quit' to stop.\n")

    # This list stores the whole conversation for this terminal session
    conversation_history = []

    while True:
        user_query = input("You: ").strip()

        if user_query.lower() in ("exit", "quit"):
            print("SmartKart Support: Thank you for chatting with us. Goodbye!")
            break

        if not user_query:
            print("SmartKart Support: Please type a question.")
            continue

        answer = customer_support_assistant(user_query, conversation_history)
        print(f"SmartKart Support: {answer}\n")


if __name__ == "__main__":
    main()