import re

def chatbot():
    print("Hello! I am a simple chatbot. How can I help you today?")
    
    while True:
        user_input = input("You: ").strip().lower()
        
        # Exit condition
        if user_input in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye! Have a great day!")
            break
        
        # Greeting responses
        elif re.search(r"\b(hello|hi|hey)\b", user_input):
            print("Chatbot: Hello! How can I assist you today?")
        
        # Assistance inquiries
        elif re.search(r"\b(help|assist|support)\b", user_input):
            print("Chatbot: I'm here to help! Please let me know what you need assistance with.")
        
        # Bot introduction
        elif re.search(r"\b(who are you|what are you)\b", user_input):
            print("Chatbot: I am a simple chatbot created to assist you with basic queries.")
        
        # Time-related inquiries
        elif re.search(r"\b(time|date)\b", user_input):
            from datetime import datetime
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Chatbot: The current date and time is {current_time}.")
        
        # Simple gratitude response
        elif re.search(r"\b(thank you|thanks)\b", user_input):
            print("Chatbot: You're welcome! Let me know if there's anything else I can do for you.")
        
        # Default response for unknown queries
        else:
            print("Chatbot: I'm sorry, I didn't understand that. Could you please rephrase it?")

if __name__ == "__main__":
    chatbot()
