# Importing required modules
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox, simpledialog
import os

# AutoHideScrollbar class to hide scrollbars when not needed
class AutoHideScrollbar(ttk.Scrollbar):
    def set(self, first, last):
        if float(first) <= 0.0 and float(last) >= 1.0:
            self.grid_remove()  # Hide scrollbar
        else:
            self.grid()  # Show scrollbar
        ttk.Scrollbar.set(self, first, last)

    def pack(self, **kw):
        raise TclError("Cannot use pack with this widget")  # Disable pack geometry manager

    def place(self, **kw):
        raise TclError("Cannot use place with this widget")  # Disable place geometry manager

# Function to create a new file
def newFile():
    global file
    root.title("Untitled - Notepad")
    file = None
    TextArea.delete(1.0, END)  # Clear the text area
    updateStatus()  # Update status bar

# Function to open an existing file
def openFile():
    global file
    file = askopenfilename(defaultextension=".txt", 
                           filetypes=[("All Files", "*.*"), 
                                      ("Text Documents", "*.txt")])
    if file:
        try:
            root.title(os.path.basename(file) + " - Notepad")
            TextArea.delete(1.0, END)  # Clear the text area
            with open(file, "r", encoding="utf-8") as f:
                TextArea.insert(1.0, f.read())  # Insert file contents into the text area
        except UnicodeDecodeError:
            with open(file, "r", encoding="latin-1") as f:
                TextArea.insert(1.0, f.read())  # Handle files with different encoding
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {e}")
            file = None
    updateStatus()  # Update status bar

# Function to save the current file
def saveFile():
    global file
    if file is None:
        file = asksaveasfilename(initialfile='Untitled.txt',
                                 defaultextension=".txt",
                                 filetypes=[("All Files", "*.*"),
                                            ("Text Documents", "*.txt")])
        if not file:
            file = None
            return
    with open(file, "w", encoding="utf-8") as f:
        f.write(TextArea.get(1.0, END))  # Write text area content to file
    root.title(os.path.basename(file) + " - Notepad")
    updateStatus()  # Update status bar

# Function to quit the application
def quitNotepad():
    root.destroy()

# Functions for text editing actions
def cut():
    TextArea.event_generate(("<<Cut>>"))

def copy():
    TextArea.event_generate(("<<Copy>>"))

def paste():
    TextArea.event_generate(("<<Paste>>"))

# Function to display information about the application
def about():
    messagebox.showinfo("About Notepad", "Notepad by Aman Gupta")

# Function to update status bar with line, column, and character count
def updateStatus(event=None):
    if statusBar:
        row, col = TextArea.index("insert").split(".")
        char_count = len(TextArea.get(1.0, END)) - 1  # Subtract 1 to exclude the newline character at the end
        statusVar.set(f"Line: {row} | Column: {col} | Characters: {char_count}")

# Function to find text in the text area
def findText():
    find_string = simpledialog.askstring("Find", "Enter text to find:")
    if find_string:
        text_data = TextArea.get(1.0, END)
        occurrences = text_data.upper().count(find_string.upper())
        
        if occurrences > 0:
            messagebox.showinfo("Result", f"Found '{find_string}' {occurrences} times.")
        else:
            messagebox.showinfo("Result", f"'{find_string}' not found.")

# Functions to apply different themes
def set_theme(bg_color, fg_color, menu_bg_color, menu_fg_color, status_bg_color, status_fg_color):
    TextArea.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
    statusBar.config(bg=status_bg_color, fg=status_fg_color)
    
    # Update menu bar color
    menu_frame.config(bg=menu_bg_color)
    
    # Update the color of custom menu labels
    for menu_label in menu_labels:
        menu_label.config(bg=menu_bg_color, fg=menu_fg_color)

def applyLightTheme():
    set_theme("white", "black", "lightgrey", "black", "lightgrey", "black")

def applyDarkTheme():
    set_theme("#2E2E2E", "white", "#1C1C1C", "white", "#3E3E3E", "white")

def applyBlueTheme():
    set_theme("light blue", "dark blue", "blue", "white", "light blue", "dark blue")

def applyGreenTheme():
    set_theme("light green", "dark green", "green", "white", "light green", "dark green")

def applyPurpleTheme():
    set_theme("lavender", "dark violet", "purple", "white", "lavender", "dark violet")

# Zoom functions for changing text size
def zoom_in(event=None):
    current_size = TextArea.cget("font").split()[1]
    new_size = int(current_size) + 2
    TextArea.config(font=f"lucida {new_size}")

def zoom_out(event=None):
    current_size = TextArea.cget("font").split()[1]
    new_size = int(current_size) - 2
    if new_size > 4:
        TextArea.config(font=f"lucida {new_size}")

# Mouse wheel zoom functions
def on_mouse_wheel(event):
    if event.delta > 0:  # Scroll up
        zoom_in()
    else:  # Scroll down
        zoom_out()

# Function to toggle the visibility of the status bar
def toggleStatusBar():
    global statusBar
    if statusBar:
        statusBar.grid_forget()
        statusBar = None
    else:
        statusBar = Label(root, textvariable=statusVar, anchor='w', bg="lightgrey", fg="black")
        statusBar.grid(row=3, column=0, columnspan=2, sticky='ew')

# Main application code
if __name__ == '__main__':
    root = Tk()
    root.title("Untitled - Notepad")
    root.geometry('644x788')
    root.iconbitmap('image/note.ico')

    # Adding Scrollbars
    ScrollY = AutoHideScrollbar(root)
    ScrollY.grid(row=1, column=1, sticky='ns')

    ScrollX = AutoHideScrollbar(root, orient=HORIZONTAL)
    ScrollX.grid(row=2, column=0, sticky='ew')

    # Adding Textarea
    TextArea = Text(root, font='lucida 13', undo=True, wrap=NONE, 
                    yscrollcommand=ScrollY.set, xscrollcommand=ScrollX.set)
    file = None
    TextArea.grid(row=1, column=0, sticky='nsew')

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    ScrollY.config(command=TextArea.yview)
    ScrollX.config(command=TextArea.xview)

    # Custom menu bar with colored background
    menu_labels = []

    # Create custom labels to represent menu items
    menu_frame = Frame(root, bg="lightgrey")
    menu_frame.grid(row=0, column=0, columnspan=2, sticky='ew')
    root.grid_columnconfigure(0, weight=1)

    file_menu_label = Label(menu_frame, text="File", bg="lightgrey", fg="black", font=("Arial", 12), padx=10, pady=5)
    file_menu_label.grid(row=0, column=0, sticky='w')
    file_menu_label.bind("<Button-1>", lambda e: FileMenu.post(e.x_root, e.y_root))
    menu_labels.append(file_menu_label)

    edit_menu_label = Label(menu_frame, text="Edit", bg="lightgrey", fg="black", font=("Arial", 12), padx=10, pady=5)
    edit_menu_label.grid(row=0, column=1, sticky='w')
    edit_menu_label.bind("<Button-1>", lambda e: EditMenu.post(e.x_root, e.y_root))
    menu_labels.append(edit_menu_label)

    view_menu_label = Label(menu_frame, text="View", bg="lightgrey", fg="black", font=("Arial", 12), padx=10, pady=5)
    view_menu_label.grid(row=0, column=2, sticky='w')
    view_menu_label.bind("<Button-1>", lambda e: ViewMenu.post(e.x_root, e.y_root))
    menu_labels.append(view_menu_label)

    theme_menu_label = Label(menu_frame, text="Theme", bg="lightgrey", fg="black", font=("Arial", 12), padx=10, pady=5)
    theme_menu_label.grid(row=0, column=3, sticky='w')
    theme_menu_label.bind("<Button-1>", lambda e: ThemeMenu.post(e.x_root, e.y_root))
    menu_labels.append(theme_menu_label)

    help_menu_label = Label(menu_frame, text="Help", bg="lightgrey", fg="black", font=("Arial", 12), padx=10, pady=5)
    help_menu_label.grid(row=0, column=4, sticky='w')
    help_menu_label.bind("<Button-1>", lambda e: HelpMenu.post(e.x_root, e.y_root))
    menu_labels.append(help_menu_label)

    # Make the menu frame visible
    menu_frame.grid(row=0, column=0, columnspan=2, sticky='ew')

    # Create the hidden menus
    MenuBar = Menu(root, tearoff=0)

    FileMenu = Menu(MenuBar, tearoff=0)
    FileMenu.add_command(label="New", command=newFile)
    FileMenu.add_command(label="Open", command=openFile)
    FileMenu.add_command(label="Save", command=saveFile)
    FileMenu.add_separator()
    FileMenu.add_command(label="Exit", command=quitNotepad)
    
    EditMenu = Menu(MenuBar, tearoff=0)
    EditMenu.add_command(label="Cut       Ctrl+X", command=cut)
    EditMenu.add_command(label="Copy     Ctrl+C", command=copy)
    EditMenu.add_command(label="Paste     Ctrl+V", command=paste)
    EditMenu.add_command(label="Find       Ctrl+F", command=findText)
    
    ViewMenu = Menu(MenuBar, tearoff=0)
    ViewMenu.add_command(label="Zoom In       Ctrl+Plus", command=zoom_in)
    ViewMenu.add_command(label="Zoom Out    Ctrl+Minus", command=zoom_out)
    ViewMenu.add_command(label="Status Bar", command=toggleStatusBar)
    
    ThemeMenu = Menu(MenuBar, tearoff=0)
    ThemeMenu.add_command(label="Light Theme", command=applyLightTheme)
    ThemeMenu.add_command(label="Dark Theme", command=applyDarkTheme)
    ThemeMenu.add_command(label="Blue Theme", command=applyBlueTheme)
    ThemeMenu.add_command(label="Green Theme", command=applyGreenTheme)
    ThemeMenu.add_command(label="Purple Theme", command=applyPurpleTheme)
    
    HelpMenu = Menu(MenuBar, tearoff=0)
    HelpMenu.add_command(label="About Notepad", command=about)

    root.config(menu=MenuBar)

    # Adding Status Bar
    statusVar = StringVar()
    statusVar.set("Line: 1 | Column: 1 | Characters: 0")
    statusBar = Label(root, textvariable=statusVar, anchor='w', bg="lightgrey", fg="black")
    statusBar.grid(row=3, column=0, columnspan=2, sticky='ew')

    TextArea.bind("<KeyRelease>", updateStatus)

    # Bind keyboard shortcuts for zoom
    root.bind("<Control-plus>", zoom_in)
    root.bind("<Control-minus>", zoom_out)

    # Bind mouse wheel for zooming
    root.bind_all("<MouseWheel>", on_mouse_wheel)
    root.bind_all("<Button-4>", on_mouse_wheel)  # Linux/Mac scroll up
    root.bind_all("<Button-5>", on_mouse_wheel)  # Linux/Mac scroll down

    # Set the default theme
    applyLightTheme()

    root.mainloop()
