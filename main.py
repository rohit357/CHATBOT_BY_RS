import pyttsx3
import datetime
import os
import webbrowser
import wikipedia
import requests
from googletrans import Translator
import pyautogui
import time
import speech_recognition as sr
import cv2
import mediapipe as mp
import numpy as np

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        speak("Good Morning")
        print("Good Morning!")
    
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon")
        print("Good Afternoon!")
    else:
        speak("Good Evening")
        print("Good Evening!")

def usr_data_mngr():
    
    try:
        crt_fle = open("usr_data.txt", "x")  
        speak("Sign in or login as user")
    
    except FileExistsError: 
        speak("Sign in or login as user")
        usr_input = input("UserName : ")
        with open("usr_data.txt", "r+") as crt_fle:  
            file_content = crt_fle.read()  
            
            if usr_input not in file_content: 
                crt_fle.write(f"\n{usr_input}")  
                speak(f"Hello {usr_input}, welcome!")
                
                if "mineesh gulati" in usr_input or "mineesh" in usr_input:
                    print("Wait! you are the principal of happy model school, right . I am so glad you are here  (expressing happiness)")
                    speak("Wait! you are the principal of happy model school, right . I am so glad you are here")
            
            else:
                speak(f"Hey welcome back {usr_input}, nice to see you!")

def get_daily_quote():
    
    try:
        response = requests.get("https://zenquotes.io/api/random")
        quote_data = response.json()
        quote = quote_data[0]['q'] 
        author = quote_data[0]['a'] 
        speak(f"Here is your daily quote: {quote} by {author}")
        print(f"{quote} - {author}")
    except Exception as e:
        speak("Sorry, I couldn't retrieve a quote at the moment.")

def translate_text(text, target_language):
    translator = Translator()
    
    try:
        translation = translator.translate(text, dest=target_language)
        translated_text = translation.text
        speak(f"The translation in {target_language} is: {translated_text}")
        print(f"{text} -> {translated_text}")
    
    except Exception as e:
        speak("Sorry, I couldn't translate that at the moment.")
        print(f"Error: {e}")

def close_app_with_mouse():
    speak("Moving the mouse to close the application.")
    pyautogui.moveTo(1880, 10)
    time.sleep(1)
    pyautogui.click()

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
    
    elif "paint" in app_name:
        os.system("mspaint")
        speak("Opening Paint")
    
    elif "word" in app_name:
        os.system("start winword")
        speak("Opening Microsoft Word")
    
    elif "excel" in app_name:
        os.system("start excel")
        speak("Opening Microsoft Excel")
    
    elif "powerpoint" in app_name:
        os.system("start powerpnt")
        speak("Opening Microsoft PowerPoint")
    
    elif "task manager" in app_name:
        os.system("taskmgr")
        speak("Opening Task Manager")
    
    elif "command prompt" in app_name:
        os.system("cmd")
        speak("Opening Command Prompt")
   
    elif "file explorer" in app_name:
        os.system("explorer")
        speak("Opening File Explorer")
    
    elif "chrome" in app_name:
        os.system("start chrome")
        speak("Opening Google Chrome")
    
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
        print(summary)
        speak(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("There are multiple pages for that topic. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("I couldn't find any information on that topic.")
    except Exception as e:
        speak("An error occurred while searching Wikipedia.")

def take_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand. Could you please repeat?")
        return "none"
    except sr.RequestError:
        speak("Sorry, I couldn't reach the speech recognition service. Please check your network.")
        return "none"

def reco():
  
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    screen_width, screen_height = pyautogui.size()
   
    prev_x, prev_y = 0, 0
    smooth_factor = 0.7  

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

       
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
      
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

          
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

        
                index_x = int(index_finger_tip.x * screen_width)
                index_y = int(index_finger_tip.y * screen_height)
              
                index_x = int(prev_x * smooth_factor + index_x * (1 - smooth_factor))
                index_y = int(prev_y * smooth_factor + index_y * (1 - smooth_factor))

                pyautogui.moveTo(index_x, index_y)
             
                prev_x, prev_y = index_x, index_y

                thumb_x = int(thumb_tip.x * screen_width)
                thumb_y = int(thumb_tip.y * screen_height)
                distance = np.hypot(thumb_x - index_x, thumb_y - index_y)
               
                if distance < 50:
                    pyautogui.click()
        
        cv2.imshow("Hand Tracking Mouse", frame)
       
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Main chatbot function
def chatbot():
    wishme()
    usr_data_mngr()
    speak("How can I assist you today?")
    
    while True:
        print("Type or say your command:")
        user_input = input("Press Enter for voice input or type directly: ").strip()

        if user_input == "":
            user_input = take_voice_input()

        if "time" in user_input:
            tell_time()
        
        elif "your name" in user_input:
            speak("My name is Ultron")
        
        elif "yourself" in user_input:
            speak("I am Ultron, an advanced chatbot developed by Rohit Sharma and Team. for SLC")
        
        elif "mineesh sir" in user_input:
            speak("Mineesh Sir teaches Physics")
        
        elif "school" in user_input:
            speak("Happy Model Higher Secondary School")
        
        elif "principal" in user_input:
            speak("Mineesh Sir is the principal of happy model higher secondary school. he is also a brilliant physics teacher.")
        
        elif "quote" in user_input or "quotes" in user_input:
            get_daily_quote()

        elif "hand free" in user_input:
            speak("ok")
            reco()
        
        elif "translate" in user_input:
            speak("What would you like to translate?")
            text_to_translate = input("Enter the text: ").strip()
            speak("Which language would you like to translate to?")
            target_language = input("Enter the language code: ").lower()
            translate_text(text_to_translate, target_language)

            # 'en': English
            # 'es': Spanish
            # 'fr': French
            # 'de': German
            # 'hi': Hindi
            # 'zh-cn': Chinese 

        
        elif "open" in user_input:
            if "website" in user_input:
                website_name = user_input.replace("open website", "").replace("open", "").strip()
                open_website(website_name)
            else:
                app_name = user_input.replace("open", "").strip() 
                open_application(app_name)
        
        elif "search" in user_input:
            query = user_input.replace("search wikipedia", "").strip()
            search_wikipedia(query)
        
        elif "exit app" in user_input or "close app" in user_input:
            close_app_with_mouse()
        
        elif "exit" in user_input or "quit" in user_input:
            speak("Goodbye!")
            break
        
        else:
            speak("I'm sorry, I didn't understand that.")

# Run the chatbot
if __name__ == "__main__":
    chatbot()

# CODE AND LOGIC WRITTEN AND DEVELOPED BY ROHIT SHARMA .
# TESTED AND DEBUGGED BY RAJVEER KHAJURIA .
