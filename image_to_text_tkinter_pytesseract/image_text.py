import tkinter
from tkinter import *
from tkinter import filedialog
from PIL import Image
from pytesseract import pytesseract
from tkinter import messagebox


def open_file():
    path_to_tesseract = r'C:\Users\35yearsago\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    path_to_image = filedialog.askopenfilename(title="Open Image File",
                                               initialdir='C:\Desktop',
                                               filetypes=[('JPG files', '*.jpg'), ('PNG files', '*.png')])
    filename_label.configure(text=path_to_image)
    outputfile_text.delete("1.0", tkinter.END)
    pytesseract.tesseract_cmd = path_to_tesseract
    img = Image.open(path_to_image)
    text = pytesseract.image_to_string(img)
    outputfile_text.insert(tkinter.END, text)


def clear():
    outputfile_text.delete('1.0', tkinter.END)
    filename_label.configure(text="No File Selected")


def on_closing():
    if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
        root.destroy()


# TODO create odject
root = tkinter.Tk()
root.title("Extract Text From Image")
root.eval("tk::PlaceWindow . center")
root.protocol("WM_DELETE_WINDOW", on_closing)
root.resizable(0, 0)

root.configure(bg='#000000')
root['bg'] = '#D7C0AE'

# TODO widgets
filename_label = tkinter.Label(root, text="No File Selected", fg='#967E76', bg='#D7C0AE')
outputfile_text = tkinter.Text(root, height=25, font=('Arial', 18), bg='#EEE3CB')
openfile_button = tkinter.Button(root, text="Open Image", cursor='hand2', font=('Arial', 12),
                                 command=open_file, bg='#967E76')
clear_b = tkinter.Button(root, text="Clear", cursor='hand2', font=('Arial', 12), command=clear, bg='#967E76')

filename_label.pack()
outputfile_text.pack()
openfile_button.pack(side="left")
clear_b.pack(side="left", padx=0.5)

root.mainloop()
