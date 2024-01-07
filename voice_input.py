import threading
from main import take_command, process_command


class VoiceInputHandler:
    def __init__(self, callback):
        self.callback = callback
        self.last_command = None

    def start_voice_input_thread(self):
        threading.Thread(target=self.process_voice_input).start()

    def process_voice_input(self):
        try:
            query = take_command()
            if query != self.last_command:
                self.last_command = query
                process_command(user_input=query)
                self.callback(query)
        except Exception as e:
            print(f"Exception in Voice input thread: {e}")
