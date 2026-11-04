from ollama import chat

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = chat(
        model="tinyllama",
        messages=[
            {
                "role": "system",
                "content": "Answer briefly in one or two sentences only."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print("Bot:", response["message"]["content"])
