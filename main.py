import sys
from PyQt6.QtWidgets import QApplication
from logwidget.widget import LsyncdWidget
from dotenv import load_dotenv

load_dotenv()

LOG_FILE = './logs/lsyncd.log'

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = LsyncdWidget(LOG_FILE)
    
    widget.show()

    sys.exit(app.exec())