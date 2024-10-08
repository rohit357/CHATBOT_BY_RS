import pyttsx3
import datetime
import os
import webbrowser
import wikipedia


engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

    
def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")


def open_application(app_name):
    if "notepad" in app_name.lower():
        os.system("notepad")
        speak("Opening Notepad")
    elif "calculator" in app_name.lower():
        os.system("calc")
        speak("Opening Calculator")
    else:
        speak("Sorry, I can't open that application.")


def open_website(website_name):
    websites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "github": "https://www.github.com"
    }
    url = websites.get(website_name.lower())
    if url:
        webbrowser.open(url)
        speak(f"Opening {website_name}")
    else:
        speak("Sorry, I don't know that website.")


def search_wikipedia(query):
    try:
        
        summary = wikipedia.summary(query, sentences=2)  
        speak(summary)
        print(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("There are multiple pages for that topic. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("I couldn't find any information on that topic.")
    except Exception as e:
        speak("An error occurred while searching Wikipedia.")

# Main chatbot function
def chatbot():
    speak("Hello! How can I assist you today?")
    
    while True:
        user_input = input("Type here: ").lower()

        if "time" in user_input:
            tell_time()

        elif "what is your name" in user_input:
            speak("my name is ultron")

        elif "tell me something about yourself" in user_input:
            speak("I am ultron an advanced chatbot developed by Rohit Sharma, a class eleventh computer science student. I am programmed in python language. I have been developed as an project for SLC. There are various tasks that i can perform. Be free to use me")
            print("I am ultron an advanced chatbot developed by Rohit Sharma, a class eleventh computer science student. I am programmed in python language. I have been developed as an project for SLC. There are various tasks that i can perform. Be free to use me")

        elif "happy model school principal name" in user_input:
            speak("mineesh sir")
        
        elif "open" in user_input:
            if "website" in user_input:
                website_name = user_input.replace("open website", "").replace("open", "").strip()
                open_website(website_name)
            else:
                app_name = user_input.replace("open", "").strip()  # Extract the app name
                open_application(app_name)

        elif "search wikipedia" in user_input:
            query = user_input.replace("search wikipedia", "").strip()
            search_wikipedia(query)

        elif "exit" in user_input or "quit" in user_input:
            speak("Goodbye!")
            break

        else:
            speak("I'm sorry, I didn't understand that.")

# Run the chatbot
if __name__ == "__main__":
    chatbot()
