import os
import math
from PyQt5.QtWidgets import (
    QApplication, QWidget, 
    QLabel, QPushButton, 
    QLineEdit, QMessageBox,
    QHBoxLayout, QVBoxLayout
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        # To make it possible for any computers to access the icon image
        folder_path = os.path.dirname(os.path.abspath(__file__))  
        icon_path = os.path.join(folder_path, 'myIcon.png')  
        
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle("Let's math")
        self.setFixedSize(420, 620)
     
        self.setStyleSheet("background-color: #2c2c2c;")
        
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        
        # Display both for input and output
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(70)
        self.display.setReadOnly(True)  # Keyboard is off to avoid errors :)
        self.display.setStyleSheet("""
            font-size: 36px;
            color: #E6E6E6;
            background-color: #1e1e1e;
            border: none;
            border-radius: 30px;
            padding: 10px;
        """)
    
        main_layout.addWidget(self.display)
        
        def create_button(text, color='#f1f2f3', text_color='#000000', fontWeight="None", text_size="36px"):
            button = QPushButton(text)
            button.setFixedSize(80, 80)
            button.setStyleSheet(f"font-size: {text_size}; font-weight: {fontWeight}; border-radius: 40px; background-color: {color}; color: {text_color};")
            if text == '0':
                button.setFixedSize(160, 80)  
                button.setStyleSheet(f"""
                    font-size: 36px;
                    border-radius: 40px;
                    background-color: {color};
                    color: {text_color};
                    text-align: left;
                    padding-left: 20px;
                """)
            button.clicked.connect(self.press)  
            return button
        
    
        row1 = QHBoxLayout()
        row1.addWidget(create_button('AC', text_color='#3d3d3d', text_size="28px"))
        row1.addWidget(create_button('√', text_color='#3d3d3d', text_size="30px"))
        row1.addWidget(create_button('%', text_color='#3d3d3d', text_size="30px"))
        row1.addWidget(create_button('÷', color='#ff9500', text_color='#ffffff'))

        row2 = QHBoxLayout()
        row2.addWidget(create_button('7', color='#4A4A4A', text_color='#ffffff'))
        row2.addWidget(create_button('8', color='#4A4A4A', text_color='#ffffff'))
        row2.addWidget(create_button('9', color='#4A4A4A', text_color='#ffffff'))
        row2.addWidget(create_button('×', color='#ff9500', text_color='#ffffff'))

        row3 = QHBoxLayout()
        row3.addWidget(create_button('4', color='#4A4A4A', text_color='#ffffff'))
        row3.addWidget(create_button('5', color='#4A4A4A', text_color='#ffffff'))
        row3.addWidget(create_button('6', color='#4A4A4A', text_color='#ffffff'))
        row3.addWidget(create_button('-', color='#ff9500', text_color='#ffffff'))

        row4 = QHBoxLayout()
        row4.addWidget(create_button('1', color='#4A4A4A', text_color='#ffffff'))
        row4.addWidget(create_button('2', color='#4A4A4A', text_color='#ffffff'))
        row4.addWidget(create_button('3', color='#4A4A4A', text_color='#ffffff'))
        row4.addWidget(create_button('+', color='#ff9500', text_color='#ffffff'))

        row5 = QHBoxLayout()
        zero_button = create_button('0', color='#4A4A4A', text_color='#ffffff')
        zero_button.setFixedSize(160, 80) 
        row5.addWidget(zero_button)
        row5.addWidget(create_button(',', color='#4A4A4A', text_color='#ffffff', fontWeight="bold"))
        equal_button = create_button('=', color='#ff9500', text_color='#ffffff')
        equal_button.setFixedSize(80, 80)
        row5.addWidget(equal_button)


        main_layout.addLayout(row1)
        main_layout.addLayout(row2)
        main_layout.addLayout(row3)
        main_layout.addLayout(row4)
        main_layout.addLayout(row5)
        
        self.setLayout(main_layout)

    def press(self):
        button = self.sender()
        button_text = button.text()
        if button_text == 'AC':
            self.display.clear()
        elif button_text=="=":
            self.display.setText(self.get_result())
            
        elif button_text=='%':
            current=self.get_result()
            if current=="No expression!":
                self.display.setText("No expression!")
            else:
                self.display.setText(f"{float(current)/100}")
            
        elif button_text=='√':
            current=self.get_result()
            if current=="No expression!":
                self.display.setText("No expression!")
            else:
                self.display.setText(f"{math.sqrt(float(current))}")
            
        else:
            current_text = self.display.text()
            if len(current_text) < 16:  # Limit the display text length
                self.display.setText(current_text + button_text)
    
    def get_result(self):
        expression = self.display.text()
        if not expression:
            return "No expression!"
        else:
            try:
                while not expression[-1].isdigit():
                    expression=expression[:len(expression)-1]  # To get rid of operation signs at the end of the expression
                    
                while not expression[0].isdigit():
                    expression=expression[1:] # To get rid of operation signs at the beginning of the expression
                    
                result = str(eval(expression.replace('×', '*').replace('÷', '/').replace(",", ".")))
                
                if len(result) > 16:  # Round the result if it's too lengthy
                    result = f"{float(result):.10g}" 
                return result
            
            except Exception:
                return "Error"


if __name__ == "__main__":
 
    app = QApplication([])
    win = Window()
    win.show()
    app.exec_()
