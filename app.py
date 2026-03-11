from generation import generate_answer

while True:
    query = input("Ask a question (or type 'quit' to exit): ")
    
    if query.lower() in ['quit', 'exit']:
        print("Goodbye!")
        break
    
    if not query.strip():
        print("Please enter a valid question.\n")
        continue
    
    answer = generate_answer(query)
    print("\nAnswer:\n")
    print(answer)
    print("\n" + "="*50 + "\n")