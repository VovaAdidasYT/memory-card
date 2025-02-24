from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget, QListWidget, QTextEdit,QLineEdit,QButtonGroup,QGroupBox,QApplication,QWidget,QPushButton,QHBoxLayout,QVBoxLayout,QLabel,QMessageBox,QRadioButton,QInputDialog
import json

notes = {'В' : {'текст': 'asd', 'теги': ['ff', 'gg']}}

with open('notes.json', 'r', encoding= 'utf-8') as file:
    notes = json.load(file)
    

def show_note():
    name = list_zametki.selectedItems()[0].text()
    field_text.setText(notes[name]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[name]['теги'])

def read_text():
    with open('notes.json', 'r', encoding= 'utf-8') as file:
        notes = json.load(file)
        return notes

def write_json(notes):
    with open('notes.json', 'w', encoding= 'utf-8') as file:
        json.dump(notes, file)
    
def add_note():
    note_name, result = QInputDialog.getText(main_win, "Добавить заметку", "Название заметки:")
    if note_name != '':
        notes[note_name] = {'текст': '', 'теги': []}
        write_json(notes)
        list_zametki.addItem(note_name)

def del_note():
    if list_zametki.selectedItems():
        name = list_zametki.selectedItems()[0].text()
        del notes[name]
        write_json(notes)
        field_text.clear()
        list_tags.clear()
        list_zametki.clear()
        list_zametki.addItems(notes.keys())
    
def save_note():
    if list_zametki.selectedItems():
        name = list_zametki.selectedItems()[0].text()
        field_textinfo = field_text.toPlainText()
        notes[name]['текст'] = field_textinfo
        write_json(notes)
    
def add_tag():
    if list_zametki.selectedItems():
        tag = field_tag.text()
        name = list_zametki.selectedItems()[0].text()
        if  not (tag in notes[name]['теги']) and tag != '':
            notes[name]['теги'].append(tag)
            list_tags.addItem(tag)
            write_json(notes)
            field_tag.clear()

def del_tag():
    if list_zametki.selectedItems():
        if list_tags.selectedItems():
            name = list_zametki.selectedItems()[0].text()
            tag = list_tags.selectedItems()[0].text()
            for i in range(len(notes[name]['теги'])):
                if notes[name]['теги'][i] == tag:
                    del notes[name]['теги'][i]
                    write_json(notes)
                    list_tags.clear()
                    list_tags.addItems(notes[name]['теги'])

def search_tag():
    if btn6.text() == 'Искать заметки по тегу':
        tag = field_tag.text()
        if tag != '':
            res = []
            for k in notes:
                if tag in notes[k]['теги']:
                    res.append(k)
            list_zametki.clear()
            field_tag.clear()
            list_tags.clear()
            list_zametki.addItems(res)
            btn6.setText('Сбросить поиск')
    else:
        list_zametki.clear()
        field_tag.clear()
        list_tags.clear()
        list_zametki.addItems(notes.keys())
        btn6.setText('Искать заметки по тегу')


        
app = QApplication([])
main_win = QWidget()
main_win.resize(1000, 500)

list_tags = QListWidget()
list_zametki = QListWidget()
field_text = QTextEdit()
field_tag = QLineEdit()
btn1 = QPushButton('Создать заметку')
btn2 = QPushButton('Удалить заметку')
btn3 = QPushButton('Сохранить заметку')
btn4 = QPushButton('Добавить к заметке')
btn5 = QPushButton('Открепить от заметки')
btn6 = QPushButton('Искать заметки по тегу')

left = QVBoxLayout()
left.addWidget(field_text)

middlebtn1 = QHBoxLayout()
middlebtn1.addWidget(btn1)
middlebtn1.addWidget(btn2)

middlebtn2 = QHBoxLayout()
middlebtn2.addWidget(btn4)
middlebtn2.addWidget(btn5)

text1 = QLabel('Список заметок')
text2 = QLabel('Список тегов')

right = QVBoxLayout()
right.addWidget(text1)
right.addWidget(list_zametki)
right.addLayout(middlebtn1)
right.addWidget(btn3)
right.addWidget(text2)
right.addWidget(list_tags)
right.addWidget(field_tag)
right.addLayout(middlebtn2)
right.addWidget(btn6)

mainlayout = QHBoxLayout()
mainlayout.addLayout(left)
mainlayout.addLayout(right)

notes = read_text()
list_zametki.addItems(list(notes.keys()))

btn1.clicked.connect(add_note)
btn2.clicked.connect(del_note)
btn3.clicked.connect(save_note)
btn4.clicked.connect(add_tag)
btn5.clicked.connect(del_tag)
btn6.clicked.connect(search_tag)
write_json(notes)   
main_win.setLayout(mainlayout) 
list_zametki.itemClicked.connect(show_note)
main_win.show()
app.exec_()