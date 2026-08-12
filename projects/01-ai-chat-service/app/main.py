# imports the function that talks to llm from ask_llm
from app.llm import ask_llm

# defines the main entry point of the application
def main():
    print("=" * 60)
    print("AI Engineering Portfolio - Project 1")
    print("=" * 60)

    #Instead of asking one question and exiting, the application keeps running until the user types 'exit'
    while True:
    	#This waits for the user to type something.
        question = input("\nAsk a question (or type 'exit'): ")

        #Exit if user types 'exit'
        if question.lower() == "exit":
            print("Goodbye!")
            break

        #error handling
        try:
            answer = ask_llm(question)
            
            #displays the model's response.
            print("\nResponse:\n")
            print(answer)

        except Exception as ex:
            print(f"\nError: {ex}")

# Only run main() if this file is executed directly.
if __name__ == "__main__":
    main()