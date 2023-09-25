#!/usr/bin/python3
'''
By Huafeng Yu, hfyu.hzcn@gmail.com

Description: The purpose of writing this program is for my own French learning. The program translates text, which can be in any language, into English and adds HTML styling to color the text differently for different speaking roles in Joplin.

Input: Paste the text into the top input box. The text can be in any language, and the program will automatically detect it. However, the format must be in the form of 'Character Name: Dialogue,' and you cannot use a Chinese colon.
Character1: Dialogue1
Dialogue1.1
Dialogue1.2
Character2: Dialogue2
Character3: Dialogue3
Input text

Output: After pasting the text into the input box, click the 'Stylize' button, then click the 'Copy to Clipboard' button to copy the HTML content to the clipboard. Next, go to Joplin and paste it.

说明:写这个程序的目的是为了我自己学习法语。程序把法语文本翻译成英语, 并且加上HTML STYLE以便在Joplin中按不同的说话角色对文本进行着色。
输入：把文本粘帖到最上面的输入框中, 文本可以是任何语言, 程序自动检测, 但格式必须是“角色名:台词”的形式，不能用中文的冒号
角色1:台词1
台词1.1
台词1.2
角色2:台词2
角色3:台词3
输入的文本

输出: 在输入框粘帖文本后, 点击Stylize按钮, 然后点击Copy to Clipboard按钮拷贝HTML内容到粘贴板, 接下来去Joplin中去粘帖即可。

'''

import sys
#import nltk
#nltk.download('punkt')  # Download the Punkt tokenizer models (if not already downloaded)
from googletrans import Translator
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit, QPushButton, QTextEdit, QHBoxLayout
def capitalizeTheFirstLetter(str):
    if len(str)>1:
        return str[0].upper() + str[1:] 
    elif len(str) == 1:
        return str[0].upper()
    else:
        return str

class TextStylizerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Text Stylizer App')
        self.setGeometry(100, 100, 800, 600)

        self.input_text = QPlainTextEdit(self)
        self.clear_button = QPushButton('Clear ↑ ', self)
        self.stylize_button = QPushButton('Stylize ↓ ', self)
        self.copy_button = QPushButton('Copy To Clipboard ↓ ', self)  # 更改按钮文本
        self.output_text = QTextEdit(self)
        self.output_stylize_text = QTextEdit(self)

        self.clear_button.clicked.connect(self.clearClick)
        self.stylize_button.clicked.connect(self.stylizeClick)
        self.copy_button.clicked.connect(self.copyToClipboard)  # 修改点击处理函数

        layout = QVBoxLayout()
        layout.addWidget(self.input_text)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addWidget(self.stylize_button)
        buttons_layout.addWidget(self.copy_button)
        layout.addLayout(buttons_layout)
        
        layout.addWidget(self.output_text)
        layout.addWidget(self.output_stylize_text)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def clearClick(self):
        '''called when the Clear button is clicked'''
        self.input_text.clear()
        self.output_text.clear()
        self.output_stylize_text.clear()
    def _capitalize_first_letter(self, input_string: str) -> str:
        '''capitalize the first letter of a string'''
        if not input_string:
            return input_string
        return input_string[0].upper() + input_string[1:]

    def _stylize( self, original_text:list, translated_text:list) -> tuple:
        '''generate HTML code for the text
        input: the original text and the translation
        return: three stylized texts: the mixed text of the original text and the translation; the translation; the original text
        '''
        colors = ['CadetBlue','DarkGoldenRod','DarkGreen','DeepSkyBlue','BlueViolet','Brown','Coral','Chocolate','DarkOrange','DarkSalmon','Pink','Blue']
        translation_style = 'style="color:#5a5a5a;"'
        indent_style = 'margin-left:30px;'
        speaker_colors = {}
        color = colors[-1]
        stylized_mixed_text = []
        stylized_original_text = []
        stylized_trans_text = []
        for origin,trans in zip(original_text, translated_text):
            if ':' in origin: #speaker
                speaker = origin.split(':')[0].strip()
                tmp = trans.split(':')
                speaker_trans = tmp[0].strip()
                trans_without_speaker = self._capitalize_first_letter(tmp[1].strip())
                if speaker not in speaker_colors:
                    speaker_colors[speaker] = colors[len(speaker_colors) % len(colors)]
                color = speaker_colors[speaker]
                stylized_mixed_text.append(f'<span style="color:{color};">{origin}&nbsp;&nbsp;<span {translation_style}>{trans_without_speaker}</span></span>')
                stylized_trans_text.append(f'<span style="color:{color};">{trans}</span>')
                stylized_original_text.append(f'<span style="color:{color};">{origin}</span>')
            else:
                if not speaker:
                    color = color_map[-1]
                stylized_mixed_text.append(f'<span style="color:{color};">&nbsp;&nbsp;&nbsp;&nbsp;{origin}&nbsp;&nbsp;<span {translation_style}>{trans}</span></span>')
                stylized_trans_text.append(f'<span style="color:{color};">&nbsp;&nbsp;&nbsp;&nbsp;{trans}</span>')
                stylized_original_text.append(f'<span style="color:{color};">&nbsp;&nbsp;&nbsp;&nbsp;{origin}</span>')
            
        
        return (stylized_mixed_text, stylized_trans_text, stylized_original_text)
    
    def _clean_string(self, input_string:str) -> list:
        '''delete empty lines, strip leading and ending spaces and TABs'''
        lines = input_string.split('\n')
        # Remove empty lines and strip leading/trailing spaces and tabs from each line
        cleaned_lines = [self._capitalize_first_letter(line.strip(' \t')) for line in lines if line.strip()]
        return cleaned_lines
    
    def _translate(self, input_text:str) -> tuple:
        '''translate the text into english
        return: a tuple of two lists, which are the original text and the translation'''
        translator = Translator()
        # 使用Google Translate进行翻译
        translation = translator.translate(input_text, src='auto', dest='en')  # 将目标语言改为你想要的语言

        # 获取翻译结果
        translated_text = translation.text

        # 将翻译结果按行拆分
        translated_lines = translated_text.strip().split('\n')

        # 将翻译结果附在原始文本每一行的后面
        original_lines = input_text.strip().split('\n')
        #mixed_text = [f"{original_line} | {translated_line}\n" for original_line, translated_line in zip(original_lines, translated_lines)]

        return (original_lines, translated_lines)
    
    def stylizeClick(self):
        '''called when the Stylize button is clicked'''
        text = self._clean_string(self.input_text.toPlainText())
        origin_text, trans_text = self._translate('\n'.join(text))
        stylized_mixed_text, stylized_trans_text, stylized_original_text = self._stylize( origin_text, trans_text )
            
        self.output_text.setPlainText('\n'.join(stylized_mixed_text) + '\n\n<hr>\n\n' + '\n'.join(stylized_trans_text) + '\n\n<hr>\n\n' + '\n'.join(stylized_original_text))
        #QT's renderer does not break lines for SPAN elements, but Joplin's renderer does. So, to display correctly in QT, we need to add <br> at the end of the line.
        self.output_stylize_text.setHtml('<br>\n'.join(stylized_mixed_text) + '\n\n<hr>\n\n' + '\n'.join(stylized_trans_text) + '\n\n<hr>\n\n' + '\n'.join(stylized_original_text)) 

    def copyToClipboard(self):
        '''called when the Copy to Clipboard button is clicked'''
        text_to_copy = self.output_text.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(text_to_copy)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextStylizerApp()
    ex.show()
    sys.exit(app.exec_())
