# joplin_stylizer
stylize a conversation text for displaying in Joplin with difference colors for each speaker

Description: The purpose of writing this program is for my own French learning. The program translates text, which can be in any language, into English and adds HTML styling to color the text differently for different speaking roles in Joplin.

Input: Paste the text into the top input box. The text can be in any language, and the program will automatically detect it. However, the format must be in the form of 'Character Name: Dialogue,' and you cannot use a Chinese colon.
Character1: Dialogue1
Dialogue1.1
Dialogue1.2
Character2: Dialogue2
Character3: Dialogue3
Input text

Output: After pasting the text into the input box, click the 'Stylize' button, then click the 'Copy to Clipboard' button to copy the HTML content to the clipboard. Next, go to Joplin and paste it.

the main window of the program:
<img width="801" alt="image" src="https://github.com/megatronComing/joplin_stylizer/assets/114308295/7ca508ef-1721-449f-8cf8-153cf202bab5">

the stylized text displyed in Joplin:
<img width="999" alt="image" src="https://github.com/megatronComing/joplin_stylizer/assets/114308295/ac4dd444-0385-4686-ad5e-6e8607f91148">

# required modules:
googletrans
pyqt5

# tested under
python 3.11.3
googletrans 4.0.0rc1
pyqt 5.15.2
macos Monterey 12.6.8

caution: 
Something is wrong with googletrans, DO NOT install it by executing "pip install googletrans"
Install it by "pip install googletrans==4.0.0-rc1"
