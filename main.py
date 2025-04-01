import tkinter as tk
from tkinter import ttk, messagebox
import requests
from chatbot.llmcore import ollama_generate
from guardrails.guardrails import AIGuardrail
class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot Frontend")
        
        # Create a frame for the input fields
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # User Name
        ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.name_entry = ttk.Entry(frame)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

        # User ID
        ttk.Label(frame, text="User  ID:").grid(row=1, column=0, sticky=tk.W)
        self.user_id_entry = ttk.Entry(frame)
        self.user_id_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        # Difficulty Level
        ttk.Label(frame, text="Difficulty Level:").grid(row=2, column=0, sticky=tk.W)
        self.difficulty_var = tk.StringVar(value="easy")
        difficulty_options = ["easy", "medium", "hard"]
        self.difficulty_combobox = ttk.Combobox(frame, textvariable=self.difficulty_var, values=difficulty_options)
        self.difficulty_combobox.grid(row=2, column=1, sticky=(tk.W, tk.E))

        # Submit Button
        self.submit_button = ttk.Button(frame, text="Start Chat", command=self.start_chat)
        self.submit_button.grid(row=3, columnspan=2)

        # Configure grid weights
        frame.columnconfigure(1, weight=1)

    def start_chat(self):
        name = self.name_entry.get()
        user_id = self.user_id_entry.get()
        difficulty = self.difficulty_var.get()

        if not name or not user_id:
            messagebox.showerror("Input Error", "Please enter both Name and User ID.")
            return

        # Display welcome message
        messagebox.showinfo("Chat Started", f"Welcome {name}! Your User ID is {user_id} and difficulty level is {difficulty}.")

        # Close the initial window
        self.root.destroy()

        # Create a new window for the chat interface
        self.open_chat_interface(name, user_id, difficulty)

    def open_chat_interface(self, name, user_id, difficulty):
        chat_window = tk.Tk()
        chat_window.title("Chat Interface")

        # Create a text area for chat messages
        chat_area = tk.Text(chat_window, state='disabled', width=50, height=20)
        chat_area.grid(row=0, column=0, columnspan=2)

        # Create an entry field for user input
        user_input = ttk.Entry(chat_window, width=40)
        user_input.grid(row=1, column=0)

        # Function to send a message
        def send_message():
            user_message = user_input.get()
            if user_message:
                chat_area.config(state='normal')
                chat_area.insert(tk.END, f"You: {user_message}\n")
                chat_area.config(state='disabled')
                user_input.delete(0, tk.END)

                try:
                    guardrail = AIGuardrail()
                    result = guardrail.guardrails(user_message)
                    if result:
                          label = guardrail.extract_label(result)
                          reason = guardrail.extract_reason(result)
                          if label == "SAFE":
                                response_data = ollama_generate(user_message)
                                chatbot_response = response_data
                          else:
                                chatbot_response=reason
                    else:
                        print("Please try later.")
                    
                    
                except Exception as e:
                    chatbot_response=print(f"i can't help with this")
                
                # Here you would add the logic to get a response from the chatbot
                # For now, we'll just echo the message
                chat_area.config(state='normal')
                chat_area.insert(tk.END, f"Chatbot: {chatbot_response}\n")
                chat_area.config(state='disabled')

        # Create a send button
        send_button = ttk.Button(chat_window, text="Send", command=send_message)
        send_button.grid(row=1, column=1)

        chat_window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()