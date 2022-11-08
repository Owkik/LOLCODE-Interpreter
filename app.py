from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename      # for choosing file
from tkinter import ttk  # for tables of lexemes and symbols
from tkinter import messagebox
from lexical_analyzer import *
from syntax_analyzer import *
import tkinter.font as tkfont

inputList = list()


def openFile():  # for opening file
    fp = askopenfilename(
        filetypes=[("LOL CODE Files", "*.lol"), ("All Files", "*.*")]
    )
    if not fp:
        return
    txt_edit.delete(1.0, END)
    with open(fp, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(END, text)
    window.title(f"Text Editor Application - {fp}")


def saveFile():  # for saving file
    fp = asksaveasfilename(
        defaultextension="lol",
        filetypes=[("LOL CODE Files", "*.lol"), ("All Files", "*.*")],
    )
    if not fp:
        return
    with open(fp, "w") as output_file:
        text = txt_edit.get(1.0, END)
        output_file.write(text)
    window.title(f"Text Editor Application - {fp}")


# called to executed the program in the text box
def execute():
    global txt_edit
    lexemes = tokenize(txt_edit.get("1.0", 'end-1c'))

    inputList = list()  # reset inputList

    # get inputs
    for i in lexemes:
        if i[0] == "GIMMEH":
            label3 = Label(window, text="Waiting for input.",
                           background="gray")
            label3.place(x=820, y=313)
            inputButton.wait_variable(var)
            inputList.append(inputField.get("1.0", 'end-1c'))
            label3.place_forget()

    syntax = program(lexemes.copy(), inputList.copy())
    lexemeTable.delete(*lexemeTable.get_children())  # reset lexeme table
    symbolTable.delete(*symbolTable.get_children())  # reset symbol table
    execBox.delete(0, END)  # reset execbox

    if isinstance(syntax, str):  # catch if error
        messagebox.showinfo("Error", syntax)
    else:
        for syn in syntax[0]:  # insert symbols
            symbolTable.insert(parent='', index='end', values=(syn[0], syn[1]))

    if isinstance(lexemes, str):  # catch if error
        messagebox.showinfo("Error", lexemes)
    else:
        for lex in lexemes:  # insert values of lexemes
            lexemeTable.insert(parent='', index='end', values=(lex[0], lex[1]))

    for elem in syntax[1]:
        execBox.insert("end", elem)


window = Tk()
window.title("LOL CODE Interpreter")
window.configure(background="gray")
window.geometry("1200x700")

# labels
label1 = Label(window, text="LEXEMES", background="gray")
label2 = Label(window, text="SYMBOL TABLE", background="gray")

# flag for enter button
var = IntVar()

# text editor
txt_edit = Text(window, height=18, width=53)
font = tkfont.Font(font=txt_edit['font'])
tab = font.measure('    ')
txt_edit.config(tabs=tab)
fr_buttons = Frame(window, relief=RAISED, bd=2)
btn_open = Button(fr_buttons, text="Open", command=openFile, height=1)
btn_save = Button(fr_buttons, text="Save As...", command=saveFile)

executeButton = Button(window, text="Execute", command=execute)
executeButton.place(x=500, y=313)

btn_open.grid(row=0, column=0, sticky="ew")
btn_save.grid(row=0, column=1, sticky="ew")

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=1, column=0, sticky="nsew")


# input field and enter button
inputField = Text(window, height=1.3, width=15)
inputButton = Button(window, text="Enter",
                     command=lambda: var.set(1))
inputField.place(x=590, y=313)
inputButton.place(x=710, y=313)


# lexemes
lexemeTable = ttk.Treeview(window, height=13)

lexemeTable['column'] = ("Lexeme", "Classification")
lexemeTable.column("#0", width=0, stretch=NO)
lexemeTable.column("Lexeme", anchor=W, width=180)
lexemeTable.column("Classification", anchor=W, width=180)
lexemeTable.heading("#0", text="", anchor=W)
lexemeTable.heading("Lexeme", text="Lexeme", anchor=W)
lexemeTable.heading("Classification", text="Classification", anchor=W)

# symbols
symbolTable = ttk.Treeview(window, height=13)

symbolTable['column'] = ("Identifier", "Value")
symbolTable.column("#0", width=0, stretch=NO)
symbolTable.column("Identifier", anchor=W, width=180)
symbolTable.column("Value", anchor=W, width=180)
symbolTable.heading("#0", text="", anchor=W)
symbolTable.heading("Identifier", text="Identifier", anchor=W)
symbolTable.heading("Value", text="Value", anchor=W)

# listbox for execution
execBox = Listbox(window, height=22, width=190)

# placing to gui
lexemeTable.place(x=430, y=28)
symbolTable.place(x=800, y=28)
execBox.place(x=5, y=340)

label1.place(x=580, y=3)  # lexemes label
label2.place(x=930, y=3)  # symbol table label

mainloop()
