from generation import generate_answer

query = input("Ask a question: ")

answer = generate_answer(query)

print("\nAnswer:\n")
print(answer)