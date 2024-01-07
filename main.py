
import datetime
import speech_recognition as sr
import win32com.client
import webbrowser
import time
import math
import subprocess
import re

speaker = win32com.client.Dispatch("SAPI.SpVoice")

# Speech Input Function --->


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio, language="en_in")
            print(f"User is saying: {text}")

            if text.lower().startswith("open "):
                command = text.lower().split("open", 1)[1].strip()
                open_resource(command)

            elif "date" in text.lower():
                watch(text)
            elif "calculate" in text.lower() or "math" in text.lower():
                calculate(text)
            else:
                print("Voice error")

            return text

        except sr.UnknownValueError:
            return handle_exceptions('UnknownValueError')

        except sr.WaitTimeoutError:
            return handle_exceptions('WaitTimeoutError')

        # Final message --->
        finally:
            print("Function executed successfully.")


# Validation check function --->

def validate_command(command):
    command = command.strip()
    command = ' '.join(command.split())
    return command


# Process command function --->

def process_command():
    while True:
        choice = input("Enter 1 to enter your request in text or enter 2 for voice input.")
        if choice == '1':
            query = input("Please enter your command: ")
            if query.lower().startswith("open "):
                command = query[5:].strip()
                open_resource(command)
            else:
                speaker.speak(query)
            break
        elif choice == '2':
            query = take_command()
            print(validate_command(query))
            break
        else:
            print("Looks like you have pressed wrong button. Please try again.")
            print("Press 1 on your num-pad to enter your request in text or press 2 on your num-pad for voice input.")


# Open resources function --->
def watch(text):

    def get_current_time():
        return datetime.datetime.now().strftime("%H:%M")

    def check_current_date():
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        speak(f"Today's date is {current_date}")

    def check_yesterday_date():
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        yesterday_date = yesterday.strftime("%Y-%m-%d")
        speak(f"Yesterday's date was {yesterday_date}")

    def check_tomorrow_date():
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        tomorrow_date = tomorrow.strftime("%Y-%m-%d")
        speak(f"Tomorrow's date will be {tomorrow_date}")

    def check_past_date(days_ago):
        past_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
        past_date_str = past_date.strftime("%Y-%m-%d")
        speak(f"The date {days_ago} days ago was {past_date_str}")

    def check_future_date(days_ahead):
        future_date = datetime.datetime.now() + datetime.timedelta(days=days_ahead)
        future_date_str = future_date.strftime("%Y-%m-%d")
        speak(f"The date {days_ahead} days ahead will be {future_date_str}")

    def speak(message):
        speaker.speak(message)

    def check_time():
        current_time = get_current_time()
        speak(f"Sir, the time is {current_time}")

    if "the time" in text:
        check_time()
    elif "today's date" in text:
        check_current_date()
    elif "yesterday's date" in text:
        check_yesterday_date()
    elif "tomorrow's date" in text:
        check_tomorrow_date()
    elif "days ago" in text:
        try:
            days_ago = int(next((word for word in text.split() if word.isdigit()), None))
            if days_ago:
                check_past_date(days_ago)
            else:
                speak("Sorry, I couldn't understand the number of days.")
        except ValueError:
            speak("Sorry, I didn't understand that. Please try again.")
    elif "days ahead" in text:
        try:
            days_ahead = int(next((word for word in text.split() if word.isdigit()), None))
            if days_ahead:
                check_future_date(days_ahead)
            else:
                speak("Sorry, I didn't understand it.")
        except ValueError:
            speaker.speak("Sorry, I couldn't understand the number of days.")


def calculate(text):
    try:
        text = text.lower()
        text = text.replace('X', '*')
        text = text.replace('into', '*')

        # Handling Square root:-

        square_root_match = re.search(r'square root of (.*)', text, re.IGNORECASE)
        if square_root_match:
            expression = square_root_match.group(1).strip()
            result = math.sqrt(float(expression))
            speaker.speak(f"The square root of {expression} is {result}")
        else:
            cube_root_match = re.search(r'cube root of (.*)', text, re.IGNORECASE)
            if cube_root_match:
                expression = cube_root_match.group(1).strip()
                result = round(math.pow(float(expression), 1 / 3), 2)
                #todo work here:
                speaker.speak(f"The cube root of {expression} is {result}")
            else:
                text = text.replace('pi', 'math.pi')
                match = re.search(r'calculate(.*)', text, re.IGNORECASE)
                if match:
                    expression = match.group(1).strip()
                    result = eval(expression)
                    speaker.speak(f"The result of {expression} is {result}")
    except Exception as e:
        speaker.speak(f"Sorry I couldn't calculate that. Please try again.")


def open_resource(resource):
    websites = ['amazon', 'youtube', 'wikipedia', 'facebook', 'instagram', 'whatsapp']
    apps = ['msword', 'excel', 'powerpoint', 'calc', 'notepad', 'mspaint']
    if resource.lower() in websites:
        speaker.speak(f"Opening {resource}.")
        time.sleep(1)
        webbrowser.open(f'http://{resource}.com')
    elif resource.lower() in apps:
        if resource.lower() == 'msword':
            speaker.speak("Opening MS-WORD")
            time.sleep(1)
            subprocess.call(['start', 'winword'], shell=True)
        elif resource.lower() == 'excel':
            speaker.speak("Opening MS-Excel")
            time.sleep(1)
            subprocess.call(['start', 'excel'], shell=True)
        elif resource.lower() == 'powerpoint':
            speaker.speak("Opening MS-Powerpoint")
            time.sleep(1)
            subprocess.call(['start', 'powerpnt'], shell=True)
        elif resource.lower() == 'calc':
            speaker.speak("Opening calculator")
            time.sleep(1)
            subprocess.call(['calc'])
        elif resource.lower() == 'notepad':
            speaker.speak("Opening Notepad")
            time.sleep(1)
            subprocess.call(['notepad'])
        elif resource.lower() == 'mspaint':
            speaker.speak("Opening MS-paint")
            time.sleep(1)
            subprocess.call(['mspaint'])
    else:
        print(f"Unknown request: {resource}")
        speaker.speak("Sorry, I didn't catch that. Could you please repeat your request?")


# Error Handling --->


def handle_exceptions(exception_type):
    def handle_unknown_value_error():
        print("Unknown command.")
        return "Sorry, I didn't get it. Could you please try again. "

    def handle_wait_timeout_error():
        print("Timeout.")
        return "Sorry, I didn't catch that. Could you please repeat your request?"

    def default_handler():
        print(f"An error of type {exception_type} occurred.")
        return "An error occurred. Please try again."

    handlers = {
        'UnknownValueError': handle_unknown_value_error,
        'WaitTimeoutError': handle_wait_timeout_error,
        # ToDo: add more handlers
    }
    return handlers.get(exception_type, default_handler)()


# Main Function:-


if __name__ == '__main__':
    speaker.speak("Hello")
    print("Tip: Press '1' on your num-pad for Text input and Press '2' on your num-pad for voice-input.")
    process_command()
