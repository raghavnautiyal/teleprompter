import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont

def extract_phrases(textfile):
    try:
        with open(file_path, 'r') as file:
            phrases = [line.strip() for line in file if line.strip()]
        return phrases
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

file_path = 'utterances.txt'

words = extract_phrases(file_path)

class Teleprompter(QWidget):
    def __init__(self):
        super().__init__()

        self.word_list = words

        self.current_index = 0

        self.initUI()

    def initUI(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showWord)

        self.layout = QVBoxLayout()
        self.setFixedWidth(500)  
        self.setFixedHeight(500)  

        font = QFont()
        font.setPointSize(25)  

        self.label = QLabel(self.word_list[self.current_index], self)
        self.label.setFont(font)  
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.startStopButton = QPushButton('Start', self)
        self.startStopButton.clicked.connect(self.startStopTimer)
        self.layout.addWidget(self.startStopButton)

        self.resetButton = QPushButton('Reset', self)
        self.resetButton.clicked.connect(self.resetSequence)
        self.layout.addWidget(self.resetButton)

        self.setLayout(self.layout)
        self.setWindowTitle('Teleprompter')
        self.show()

    def showWord(self): 
        self.current_index = (self.current_index + 1) % len(self.word_list) # reset the index if it gets to the last element
        self.label.setText(self.word_list[self.current_index])

    def startStopTimer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.startStopButton.setText('Start')
        else:
            self.timer.start(5000)  # 5000 milliseconds = 5 seconds
            self.startStopButton.setText('Pause')

    def resetSequence(self):
        self.timer.stop()
        self.current_index = 0
        self.label.setText(self.word_list[self.current_index])
        self.startStopButton.setText('Start')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Teleprompter()
    sys.exit(app.exec_())