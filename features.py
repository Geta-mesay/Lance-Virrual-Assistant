import speech_recognition as sr
import pyttsx3
import datetime
import requests
import wikipedia
import webbrowser
import subprocess
import pyautogui
import os
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from sympy import *
from bs4 import BeautifulSoup
import re
import openai

class Lance:
    
    def __init__(self,  openai_api_key):
        self.engine = pyttsx3.init()
        self.voice = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voice[0].id)
        self.newVoiceRate = 150
        self.engine.setProperty('rate', self.newVoiceRate)
        self.email_user = 'your_email@gmail.com'  # Replace with your email
        self.email_password = 'your_email_password'  # Replace with your email password
        self.email_host = 'imap.gmail.com'  # Change based on your email provider
        self.todo_list = []
          # Set your OpenAI API key
        openai.api_key = openai_api_key
    
    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def time(self):
        Time = datetime.datetime.now().strftime("%I:%M:%S")
        self.speak("The current time is ")
        self.speak(Time)

    def date(self):
        year = int(datetime.datetime.now().year)
        month = int(datetime.datetime.now().month)
        date = int(datetime.datetime.now().day)
        self.speak("The current date is")
        self.speak(date)
        self.speak(month)
        self.speak(year)

    def greet(self):
        hour = datetime.datetime.now().hour

        if 6 <= hour <= 12:
            self.speak("Good morning buddy, what a beautiful day to start, How can I help you.")
        elif 12 < hour < 18:
            self.speak("Good afternoon buddy, i hope you are having a good day, how can I help you?")
        else:
            self.speak("Good evening buddy, what great night it is, How can I help you")
        
    def greet_custom_response(self):
        self.speak("Yeah buddy, how can i help?")


    def get_weather(self, city):
        api_key = "edbe0e3baba12180aa7ed2b8a45388f3"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url)
        data = response.json()

        weather = data['weather'][0]['main']
        temp = round(data['main']['temp'] - 273.15, 2)
        return f"The weather in {city} is {weather} with a temperature of {temp} degrees Celsius"
    def get_news(self):
        # You can replace the API key and URL with a news API of your choice
        api_key = "06d32253e54e4ef1ad5a3f61efc0ae20"
        url = f"http://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        response = requests.get(url)
        data = response.json()

        headlines = [article['title'] for article in data['articles']]
        return headlines

    def get_info(self, query):
        try:
            results = wikipedia.summary(query, sentences=2)
            return results
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation errors if needed
            return f"Multiple results found. Please be more specific. {e}"
        except wikipedia.exceptions.PageError as e:
            # Handle page not found errors if needed
            return f"No information found for {query}. {e}"
    def open_website(self, url):
        try:
            webbrowser.open(url)
            self.speak(f"Opening {url}")
        except Exception as e:
            self.speak(f"Sorry, I couldn't open the website. {e}")

    def search_browser(self, query):
        search_url = f"https://www.google.com/search?q={query}"
        self.open_website(search_url)

    def open_youtube(self, query):
        youtube_url = "https://www.youtube.com"
        search_url = f"{youtube_url}/results?search_query={query}"

        try:
            webbrowser.open(search_url)
            self.speak(f"Searching for {query} on YouTube.")
        except Exception as e:
            self.speak(f"Sorry, I couldn't open YouTube. {e}")
    
    def open_app(self, app_name):
        try:
            subprocess.Popen([app_name], shell=True)
            self.speak(f"Opening {app_name}")
        except Exception as e:
            self.speak(f"Sorry, I couldn't open {app_name}. {e}")

    def take_screenshot(self):
        try:
            screenshot_path = "screenshot.png"
            pyautogui.screenshot(screenshot_path)
            self.speak("Taking a screenshot. Please check the screenshot file.")
            os.system(f'start {screenshot_path}')  # Open the screenshot file
        except Exception as e:
            self.speak(f"Sorry, I couldn't take a screenshot. {e}")
    

    def add_todo(self, task):
        self.todo_list.append(task)
        self.speak(f"Added '{task}' to your to-do list.")

    def show_todo_list(self):
        if not self.todo_list:
            self.speak("Your to-do list is empty.")
        else:
            self.speak("Here is your to-do list:")
            for idx, task in enumerate(self.todo_list, start=1):
                self.speak(f"{idx}. {task}")

    def clear_todo_list(self):
        self.todo_list = []
        self.speak("Your to-do list has been cleared.")

    def send_email(self, to, subject, body):
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Change based on your email provider
                server.starttls()
                server.login(self.email_user, self.email_password)
                
                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = self.email_user
                msg['To'] = to

                server.sendmail(self.email_user, to, msg.as_string())

            self.speak("Email sent successfully.")
        except Exception as e:
            self.speak(f"Sorry, I couldn't send the email. {e}")

    def read_emails(self):
        try:
            mail = imaplib.IMAP4_SSL(self.email_host)
            mail.login(self.email_user, self.email_password)
            mail.select('inbox')

            status, messages = mail.search(None, 'ALL')
            messages = messages[0].split()

            if not messages:
                self.speak("No new emails.")
                return

            for msg_id in messages:
                _, msg_data = mail.fetch(msg_id, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])
                subject = msg['Subject']
                sender = msg['From']
                self.speak(f"New email from {sender}. Subject: {subject}")

        except Exception as e:
            self.speak(f"Sorry, I couldn't read your emails. {e}")
        finally:
            mail.logout()
    def perform_calculation(self, expression):
        try:
            result = eval(expression)
            self.speak(f"The result of {expression} is {result}.")
        except Exception as e:
            self.speak(f"Sorry, I couldn't perform the calculation. {e}")
    def create_note(self, note_content):
        try:
            with open('notes.txt', 'a') as notes_file:
                notes_file.write(f"{datetime.datetime.now()}: {note_content}\n")
            self.speak("Note created successfully.")
        except Exception as e:
            self.speak(f"Sorry, I couldn't create the note. {e}")
    def read_notes(self):
        try:
            with open('notes.txt', 'r') as notes_file:
                notes = notes_file.readlines()
                if notes:
                    self.speak("Here are your notes:")
                    for note in notes:
                        self.speak(note)
                else:
                    self.speak("You don't have any notes.")
        except Exception as e:
            self.speak(f"Sorry, I couldn't read your notes. {e}")
    def tell_joke(self):
        try:
            # Fetch a joke from JokeAPI
            joke_response = requests.get('https://v2.jokeapi.dev/joke/Any')
            joke_data = joke_response.json()

            if 'joke' in joke_data:
                joke_text = joke_data['joke']
                self.speak(joke_text)
            elif 'setup' in joke_data and 'delivery' in joke_data:
                setup = joke_data['setup']
                delivery = joke_data['delivery']
                self.speak(f"{setup} {delivery}")
            else:
                self.speak("I couldn't fetch a joke at the moment. How about I tell you one later?")
        except Exception as e:
            self.speak(f"Sorry, I couldn't fetch a joke. {e}")

    def play_music(self):
        # Placeholder for playing music.
        # In a real-world scenario, you would integrate with a music service or player.
        self.speak("Sure, let me play some music for you.")
        webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')  # Placeholder link for demonstration
    def open_youtube_playlist(self, playlist_url):
        try:
            webbrowser.open(playlist_url)
            self.speak(f"Opening your YouTube playlist.")
        except Exception as e:
            self.speak(f"Sorry, I couldn't open the YouTube playlist. {e}")

    def math_operations(self, query):
        try:
            if 'calculate' in query:
                # Extract the expression after 'calculate'
                expression = query.split('calculate')[1].strip()
                result = eval(expression)
                self.speak(f"The result of {expression} is {result}")

            elif 'solve' in query:
                # Extract the equation after 'solve'
                equation = query.split('solve')[1].strip()
                x = symbols('x')
                solution = solve(equation, x)
                self.speak(f"The solution to the equation {equation} is {solution}")

        except Exception as e:
            self.speak(f"Sorry, I couldn't perform the calculation. {e}")
    
    def scrape_website(self, query):
        try:
            # Extract the website and search query
            website_match = re.search(r'from (.+?) about (.+)', query)
            if website_match:
                website = website_match.group(1)
                search_query = website_match.group(2)

                # Perform a web search using the provided query
                search_url = f'https://www.google.com/search?q={search_query}+site:{website}'
                response = requests.get(search_url)
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract relevant information (e.g., price from Amazon)
                # This example assumes that the price is inside a span element with a specific class
                price_element = soup.find('span', class_='price')
                if price_element:
                    price = price_element.text.strip()
                    self.speak(f"The {search_query} on {website} is priced at {price}")
                else:
                    self.speak(f"Sorry, I couldn't find information about {search_query} on {website}")

        except Exception as e:
            self.speak(f"Sorry, I couldn't perform the web search. {e}")
    def understand_and_respond(self, query):
        try:
            # Use OpenAI API to generate a response
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=query,
                max_tokens=100,
                n=1,
                stop=None
            )

            # Extract the generated response
            generated_response = response.choices[0].text.strip()

            # Speak the response
            self.speak(generated_response)

        except Exception as e:
            self.speak(f"Sorry, I couldn't understand that. {e}")
    def takeCommand(self,):
        r = sr.Recognizer()
        query = ""
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-US')
            print(query)

            if 'go offline' in query:
                self.speak("Going offline. Goodbye buddy!")
                self.go_offline()

            elif 'time' in query:
                self.time()

            elif 'date' in query:
                self.date()

            elif 'weather' in query:
                city = query.replace("what is the weather in", "")
                weather_res = self.get_weather(city)
                self.speak(weather_res)

            elif 'news' in query:
                news = self.get_news()
                for headline in news:
                    self.speak(headline)
            elif 'open my favorite playlist' in query:
                playlist_url = "https://www.youtube.com/watch?v=zABLecsR5UE&list=RDzABLecsR5UE"
                self.open_youtube_playlist(playlist_url)
            elif 'tell me about' in query:
                topic = query.replace("tell me about", "")
                info_res = self.get_info(topic)
                self.speak(info_res)

            elif 'open a website' in query:
                url = query.replace("open website", "")
                self.open_website(url)

            elif 'search on browser' in query:
                search_query = query.replace("search on browser", "")
                self.search_browser(search_query)

            elif 'open YouTube and search' in query:
                video_query = query.replace("open YouTube and search", "")
                self.open_youtube(video_query)

            elif 'open app' in query:
                app_name = query.replace("open app", "")
                self.open_app(app_name)

            elif 'take a screenshot' in query:
                self.take_screenshot()

            elif 'add to do list' in query:
                task = query.replace("add to-do", "")
                self.add_todo(task)

            elif 'show to do list' in query:
                self.show_todo_list()

            elif 'clear to do list' in query:
                self.clear_todo_list()

            elif 'send email' in query:
                self.send_email(to="recipient@example.com", subject="Test Email", body="This is a test email.")

            elif 'read my emails' in query:
                self.read_emails()

            elif 'perform calculation' in query:
                expression = query.replace("perform calculation", "")
                self.perform_calculation(expression)

            elif 'create a note' in query:
                note_content = query.replace("create note", "")
                self.create_note(note_content)

            elif 'read notes' in query:
                self.read_notes()

            elif 'tell a joke' in query:
                self.tell_joke()

            elif 'play music' in query:
                self.play_music()

            elif any(keyword in query for keyword in ['calculate', 'solve']):
                self.math_operations(query)

            elif 'search on internet' in query:
                search_query = query.replace("search internet", "")
                self.search_internet(search_query)

            elif 'scrape  a website' in query:
                website_query = query.replace("scrape website", "")
                self.scrape_website(website_query)

            elif 'understand and respond' in query:
                prompt = query.replace("understand and respond", "")
                self.understand_and_respond(prompt)

            else:
                #self.understand_and_respond(query)
                self.speak("Sorry, I didn't understand that. Can you please repeat?")

        except Exception as e:
            print(e)
            self.speak("Sorry, could you repeat that?")  
        

        return query