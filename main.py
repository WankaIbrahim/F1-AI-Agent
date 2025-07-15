import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl
from app import ChatBotBackend
from dotenv import load_dotenv

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

if __name__ == "__main__":
    load_dotenv()
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    chatbot = ChatBotBackend()
    engine.rootContext().setContextProperty("chatbotBackend", chatbot)

    engine.load("main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
