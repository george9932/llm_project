import sys
from langchain_community.llms import Ollama

DIM_TEXT = "\033[2m"
RESET_TEXT = "\033[0m"

# Ollama is installed in the ros2 conda environment
llm = Ollama(model = "llama3")

try:
    with open('ts_example_2.yaml', 'r') as file:
        ts = str(file.read()) # transition system as string

    with open('ts_instructions_2.txt', 'r') as file:
        ts_instructions = file.read() # instructions to LLM
except FileNotFoundError as e:
    print(f"Error: {e}")
    sys.exit(1)

conversation_history = ""   
initial_prompt = ts_instructions + ts
print(f"\nThe following prompt has been given: '{initial_prompt}'\n")

user_input = input(f"{DIM_TEXT}Send a message or press 'i' to use the prompt: {RESET_TEXT}")
if user_input.strip() == "i":
    user_input = initial_prompt
     
while True:
    if user_input.strip() == "q": 
        print("Exiting...")
        break
    else:
        conversation_history += "\nUser prompt: " + user_input + "\nLLM answer: "

        try:
            response = ""
            for chunks in llm.stream(conversation_history):
                print(chunks, end="")
                response += chunks

            conversation_history += response
            user_input = input(f"\n{DIM_TEXT}Send a message (Press 'q' to quit): {RESET_TEXT}")
        except Exception as e:
            print(f"Error during LLM interaction: {e}")
            break
