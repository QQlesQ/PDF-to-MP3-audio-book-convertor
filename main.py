import os
import gtts.lang
from gtts import gTTS
from tkinter import Tk, Button, Canvas, StringVar, PhotoImage, Label, ttk
from tkinter.filedialog import askopenfilename
import pdfplumber

dict_of_languages = gtts.lang.tts_langs()
list_of_languages = []
for lang in dict_of_languages.values():
    list_of_languages.append(lang)


def open_file():
    global file_location
    file_location = askopenfilename(title="Open file")


def get_pages():
    open_file()
    file_name = file_location.split('/')[-1]
    file_name_label.config(text=file_name)
    with pdfplumber.open(file_location) as pdf:
        total_pages = len(pdf.pages)
        pages_list = []
        for page in range(1, total_pages + 1):
            pages_list.append(page)
        page_from_combobox['values'] = pages_list
        page_to_combobox['values'] = pages_list


def get_text():
    page_from = (int(page_from_combobox.get()) - 1)
    page_to = (int(page_to_combobox.get()))
    book = ""
    with pdfplumber.open(file_location) as pdf:
        for pages in range(page_from, page_to):
            page_to_print = pdf.pages[pages]
            book += page_to_print.extract_text()
    return book


def make_mp3():
    tag = "en"
    name = file_name_label.cget('text').split('.')
    selected_language = lang_combobox.get()
    for short, language in dict_of_languages.items():
        if language == selected_language:
            tag = short
    book = get_text()
    tts = gTTS(text=book, lang=tag)
    print("Generating Speech.....")
    filename = f"{name[0]}.mp3"
    tts.save(filename)
    os.system(f"start {filename}")
    print("Successfully Generated!")

# final_output.save(f"{name}.mp3")


file_location = ""

# GUI
window = Tk()
window.title("PDF to MP3")
window.config(padx=20, pady=20)

variable_lang = StringVar(window)
variable_lang.set("English")

# Canvas
canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Label
file_label = Label(text="File:")
file_label.grid(row=1, column=0)
file_name_label = Label(text="")
file_name_label.grid(row=1, column=1)
page_from_label = Label(text="Page from:")
page_from_label.grid(row=2, column=0)
page_to_label = Label(text="Page to:")
page_to_label.grid(row=3, column=0)
language_label = Label(text="Language:")
language_label.grid(row=4, column=0)

# ComboBox
lang_combobox = ttk.Combobox(window, textvariable=variable_lang, values=list_of_languages, state='readonly')
# lang_combobox.bind('<<ComboboxSelected>>')
lang_combobox.grid(row=4, column=1)

page_from_combobox = ttk.Combobox(window, textvariable="", state='readonly')
page_from_combobox.grid(row=2, column=1)

page_to_combobox = ttk.Combobox(window, textvariable="", state='readonly')
page_to_combobox.grid(row=3, column=1)

# Button
open_button = Button(text="Open file", width=8, command=get_pages)
open_button.grid(row=1, column=2)
save_button = Button(text="Save MP3", width=8, command=make_mp3)
save_button.grid(row=4, column=2)


window.mainloop()
