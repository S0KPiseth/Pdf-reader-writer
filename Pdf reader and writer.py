from tkinter import *
from tkinter import ttk, filedialog, messagebox
import PyPDF2
from fpdf import FPDF
import os
from PIL import Image, ImageTk


class FileName:
    def __init__(self):
        self.open_status = False
        self.file_set_name = ""
        if len(notebook.tabs()) != 0 and not self.open_status:
            file.delete("Save")
            file.insert_command(2, label="Save", command=self.create_write_pdf)
            self.ask_name()
        else:
            self.default_tab()

    def ask_name(self):
        self.name = Toplevel()
        self.name.geometry("270x90")
        self.name.title("New Files")
        self.enter_name = Label(
            self.name, text=" Enter Name ", font=("Helvetica", 11)
        ).grid(row=0, column=0, pady=5)
        self.sth = ttk.Entry(self.name)
        self.sth.grid(row=0, column=1, padx=15, pady=5)

        ttk.Button(
            self.name,
            text="Enter",
            width=10,
            style="Accent.TButton",
            command=self.enter,
        ).grid(row=1, column=0, columnspan=2, pady=10)

        self.name.wm_iconphoto(False, pop_upIcon)

    def default_tab(self):
        self.tab = Frame(notebook)
        notebook.add(self.tab, text="Untitled")
        v = Scrollbar(self.tab, orient="vertical")
        v.pack(side=RIGHT, fill=Y)
        self.text = Text(self.tab, undo=True, yscrollcommand=v.set)
        self.text.pack(expand=True, fill="both")

        v.config(command=self.text.yview)
        text_areas[self.tab] = self.text

    def enter(self):
        tab1 = Frame(notebook)
        notebook.add(tab1, text=self.sth.get() or "Untitled")
        v = Scrollbar(tab1, orient="vertical")
        v.pack(side=RIGHT, fill=Y)
        text1 = Text(tab1, undo=True, yscrollcommand=v.set)
        text1.pack(expand=True, fill="both")

        v.config(command=text1.yview)
        text_areas[tab1] = text1
        self.file_set_name = self.sth.get()
        self.name.destroy()

    # create pdf file

    def create_write_pdf(self):
        try:
            current = notebook.nametowidget(notebook.select())
            initial_name = None

            if current in text_areas:
                plain_text = text_areas[current].get(1.0, END)
                # save newly created file
                if notebook.index(notebook.select()) != 0:
                    initial_name = self.file_set_name
                # modify the existing file

                if notebook.tab(notebook.select(), "text") == os.path.basename(
                    open_file_path
                ):
                    file_name = open_file_path
                # save the default file
                else:

                    file_Name = filedialog.asksaveasfile(
                        mode="wb",
                        filetypes=(("PDF files", (".pdf")), ("all files", ".*")),
                        initialdir="C:\\Users\\User\\Desktop\\deskstop icon\\Piseth-SoK\\01 Project\\COSC 121\\4_Assignments\\new\\pdf files",
                        initialfile=initial_name,
                    )

                    file_name = file_Name.name
                    file_name += ".pdf"

                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, plain_text)
                pdf.output(file_name, "F")
        except Exception:
            messagebox.showerror("Error", "You haven't chosen any file to save!")


def new_file():

    filename = FileName()


def open_file():
    global file_image, open_file_path

    image = Image.open("32px-PDF_icon.png")
    image_resize = image.resize((10, 10))

    file_image = ImageTk.PhotoImage(image_resize)
    filename.open_status = True

    open_file_path = filedialog.askopenfilename(
        defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
    )
    if open_file_path:
        file_name = os.path.basename(open_file_path)
        with open(open_file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            page = reader.pages[0]
            content = page.extract_text()

            open_tap = Frame(notebook)
            notebook.add(open_tap, text=file_name, image=file_image, compound="left")
            v = Scrollbar(open_tap, orient="vertical")
            v.pack(side=RIGHT, fill=Y)
            text = Text(open_tap, undo=True, yscrollcommand=v.set)
            text.pack(expand=True, fill="both")
            v.config(command=text.yview)

            text_areas[open_tap] = text
            text.insert(END, content)
    else:
        messagebox.showerror("Error", "You didn't chose any PDF file!")


def exit():
    window.destroy()


class Edit:
    def __init__(self):
        self.cut_status = False
        self.paste_status = False
        self.undo_status = False
        self.redo_status = False
        self.copy_status = False

    def action(self):
        try:
            current = notebook.nametowidget(notebook.select())
            widget = current.winfo_children()[1]
            if self.copy_status:
                window.clipboard_append(widget.get(SEL_FIRST, SEL_LAST))
            if self.cut_status:
                window.clipboard_clear()
                window.clipboard_append(widget.get(SEL_FIRST, SEL_LAST))
                widget.delete(SEL_FIRST, SEL_LAST)
            if self.paste_status:
                clipboard = window.clipboard_get()
                widget.insert(INSERT, clipboard)
            if self.undo_status:
                widget.edit_undo()
            if self.redo_status:
                widget.edit_redo()
        except Exception as e:
            messagebox.showerror("Error", "An error occurred!")


def copy():
    Copy = Edit()
    Copy.copy_status = True
    Copy.action()


def cut():
    Cut = Edit()
    Cut.cut_status = True
    Cut.action()


def paste():
    Paste = Edit()
    Paste.paste_status = True
    Paste.action()


def undo():
    Undo = Edit()
    Undo.undo_status = True
    Undo.action()


def redo():
    Redo = Edit()
    Redo.redo_status = True
    Redo.action()


window = Tk()

window.title("PDCreator")


img = ImageTk.PhotoImage(Image.open("icon.png"))
pop_upIcon = ImageTk.PhotoImage(Image.open("popup.png"))
window.wm_iconphoto(False, img)


window.call("source", "Azure/azure.tcl")
window.call("set_theme", "light")

open_file_path = ""
text_areas = {}

menu = Menu(window, font=("Helvetica", 11))
window.configure(menu=menu)


file = Menu(menu, tearoff=0)
menu.add_cascade(label="Files", menu=file)
file.add_command(label="New file", command=new_file)


file.add_separator()

file.add_command(label="Open", command=open_file)
file.add_separator()
file.add_command(label="Exit", command=exit)

edit = Menu(menu, tearoff=0)

menu.add_cascade(label="Edit", menu=edit)
edit.add_command(label="Undo", command=undo)
edit.add_command(label="Redo", command=redo)
edit.add_separator()
edit.add_command(label="Copy", command=copy)
edit.add_command(label="Cut", command=cut)
edit.add_command(label="Paste", command=paste)

notebook = ttk.Notebook(window)
notebook.pack(expand=True, fill="both")


filename = FileName()
file.insert_command(2, label="Save", command=filename.create_write_pdf)


window.mainloop()
