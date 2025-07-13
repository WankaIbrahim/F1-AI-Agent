import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication, QIcon
os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"


if __name__ == "__main__":
    QGuiApplication.setApplicationName("F1 AI Agent")
    QGuiApplication.setOrganizationName("YourOrgName")
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("photos/icon.ico"))

    app.setWindowIcon(QIcon("photos/icon.ico"))


    engine = QQmlApplicationEngine()
    
    qml_file = os.path.join(os.path.dirname(__file__), "main.qml")
    engine.load(QUrl.fromLocalFile(qml_file))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
