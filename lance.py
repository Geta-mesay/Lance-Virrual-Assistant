import sys
import datetime
import speech_recognition as sr
from PyQt5.QtCore import Qt, QUrl, QTimer, QThread, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from features import Lance  # Importing the Lance class from the new file

class SpeechThread(QThread):
    speech_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.lance_instance = Lance(openai_api_key="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")
        self.online = True  # Flag to determine if the assistant is online

    def run(self):
        # Initial greeting without waiting for wake word
        self.lance_instance.greet_custom_response()
        self.take_command_and_wait_for_wake_word()

    def take_command_and_wait_for_wake_word(self):
        while self.online:  # Keep running while online
            # Start actively listening for commands
            command = self.lance_instance.takeCommand()

            # Check if the user wants to go offline
            if "go offline" in command.lower():
                self.go_offline()
            else:
                # Listen for the wake word ("Lance" or "Buddy")
                wake_word = self.listen_for_wake_word()

                if wake_word:
                    # Respond to the wake word
                    self.lance_instance.greet_custom_response()

                    # Continue listening for commands
                    self.take_command_and_wait_for_wake_word()
                

    def listen_for_wake_word(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening for wake word...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=5)  # Set a timeout for listening

        try:
            print("Recognizing wake word...")
            wake_word = r.recognize_google(audio, language='en-US')
            print(wake_word)

            if any(keyword in wake_word.lower() for keyword in ["lance", "buddy"]):
                return True
        except sr.UnknownValueError:
            pass  # Ignore if the recognizer could not understand the audio

        return False

    def go_offline(self):
        self.lance_instance.go_offline()
        self.online = False

class WebApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lance: Virtual AI Assistant")
        self.setGeometry(-10, -10, 2580, 450)
        self.setWindowFlag(Qt.FramelessWindowHint)  # Borderless window

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        # Replace "path/to/your/index.html" with the actual path to your HTML file
        self.web_view.setUrl(QUrl.fromLocalFile("/index.html"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WebApp()
    window.show()

    speech_thread = SpeechThread()
    speech_thread.speech_signal.connect(app.quit)

    timer = QTimer()
    timer.singleShot(1000, speech_thread.start)

    sys.exit(app.exec_())
