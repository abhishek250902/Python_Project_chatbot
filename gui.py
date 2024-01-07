import tkinter as tk
from tkinter import scrolledtext
from main import calculate, open_resource, watch, process_command
from voice_input import VoiceInputHandler


class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Chattur!")
        self.master.geometry("600x600")
        self.master.configure(bg="DarkSlateGray")

        self.chat_history = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=60, height=20)
        self.chat_history.pack(pady=10)
        self.chat_history.configure(state="disabled", bg="LightGray")

        self.user_input = tk.Entry(self.master, width=50)
        self.user_input.pack(pady=10)

        self.voice_input_handler = VoiceInputHandler(self.process_voice_input)

        self.voice_button = tk.Button(self.master, text="Voice Input", command=self.voice_input)
        self.voice_button.pack(padx=5)

        self.text_button = tk.Button(self.master, text="Text Input", command=self.text_input)
        self.text_button.pack(padx=5)

    def voice_input(self):
        self.voice_input_handler.start_voice_input_thread()
        return '2'

    def process_voice_input(self, query):
        self.master.after(0, self.display_message, "You", query)
        self.handle_voice_command(query)

    def handle_voice_command(self, command):
        if command.lower().startswith("open "):
            resource = command[5:].strip()
            system_response = open_resource(resource)
        elif "calculate" in command.lower() or "math" in command.lower():
            system_response = calculate(command)
        elif "date" in command.lower():
            system_response = watch(command)
        else:
             system_response = "Sorry, I couldn't understand that."

        self.display_message("System", system_response)

    def calculate(self, query):
        system_response = calculate(query)
        self.display_message("System", system_response)

    def watch(self, query):
        system_response = watch(query)
        self.display_message("System", system_response)

    def text_input(self):
        user_text = self.user_input.get()
        self.display_message("You", user_text)

        if user_text.lower().startswith("open "):
            resource = user_text[5:].strip()
            system_response = open_resource(resource)
        elif "calculate" in user_text.lower() or "math" in user_text.lower():
            system_response = calculate(user_text)
        elif "date" in user_text.lower():
            system_response = watch(user_text)
        else:
            system_response = "Sorry, I couldn't understand that."

        self.display_message("System", system_response)

        self.user_input.delete(0, tk.END)
        return '1'

    def display_message(self, sender, message):
        self.chat_history.configure(state="normal")
        self.chat_history.insert(tk.END, f"{sender}: {message}\n")
        self.chat_history.configure(state="disabled")
        self.chat_history.yview(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
