import pyttsx3
import speech_recognition as sr
import requests
import webbrowser


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listinig....")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""


def get_Weather(api_key, city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        weather_desc = data['weather'][0]['description']
        city_name = data['name']
        weather_info = f"The temperature in {city_name} is {temp} degree cleius with {weather_desc}."
        speak(weather_info)
        print(weather_info)
    else:
        speak("I couldn't fetch the weather information")
        speak("Error Fetching weather app")


def search_web(query):
    url = f"https://duckduckgo.com/?q={query}"
    webbrowser.open(url)
    speak(f"searching for {query} on Google")
    print(f"searching for {query} on Google")


def main():
    API_KEY = "2cd887781e28691cabbbffe5546bda84"  # Replace with your actual API key
    speak(
        "Hello! I am your assistant. Say 'weather' followed by the city name to get the weather, or say 'search' followed by your query to search the web.")
    while True:
        speak("Would you like to check the weather or search the web?")
        command = recognize_speech().lower()
        if "weather" in command:
            speak("Please provide the city name.")
            city_name = recognize_speech()
            get_Weather(API_KEY, city_name)
        elif "search" in command:
            speak("Please provide your search query.")
            query = recognize_speech()
            search_web(query)
        elif "exit" in command:
            speak("Thank You For Choosing 'AI', Any Query Please tell me!")
            break
        else:
            speak("I didn't understand. Please try again.")
            print("Unrecognized command.")


if __name__ == "__main__":
    main()
