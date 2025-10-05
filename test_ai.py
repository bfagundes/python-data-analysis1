from ai_integration import ask_ai

def main():
    prompt = "Write a haiku about data analysis with Python."
    answer = ask_ai(prompt)
    print("AI Response:\n", answer)

if __name__ == "__main__":
    main()