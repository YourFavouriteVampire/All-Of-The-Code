import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileReader
from tkinter.colorchooser import askcolor

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text_editor.get("1.0", tk.END))
        messagebox.showinfo("Save", "File saved successfully.")

def save_as_pdf():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf")
    if file_path:
        pdf = canvas.Canvas(file_path)
        pdf.saveState()
        pdf.setFont("Helvetica", 12)
        lines = text_editor.get("1.0", tk.END).split("\n")
        y = 720
        for line in lines:
            pdf.drawString(50, y, line)
            y -= 20
            if y <= 50:
                y = 720
                pdf.showPage()
        pdf.save()
        messagebox.showinfo("Save as PDF", "File saved as PDF successfully.")

def open_file():
    if text_editor.get("1.0", tk.END).strip():
        result = messagebox.askyesnocancel("Open", "Do you want to save the current file before opening a new one?")
        if result is None:
            return
        elif result:
            save_file()

    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("PDF Files", "*.pdf")])
    if file_path:
        if file_path.endswith(".txt"):
            with open(file_path, 'r') as file:
                text_editor.delete("1.0", tk.END)
                text_editor.insert(tk.END, file.read())
        elif file_path.endswith(".pdf"):
            pdf = PdfFileReader(file_path)
            text = ""
            for page_num in range(pdf.getNumPages()):
                page = pdf.getPage(page_num)
                text += page.extract_text()
            text_editor.delete("1.0", tk.END)
            text_editor.insert(tk.END, text)
        else:
            messagebox.showwarning("Open", "Unsupported file format.")

def new_file():
    if text_editor.get("1.0", tk.END).strip():
        result = messagebox.askyesnocancel("New File", "Do you want to save the current file before creating a new one?")
        if result is None:
            return
        elif result:
            save_file()
    text_editor.delete("1.0", tk.END)

def set_font_size(event=None):
    selected_size = font_size_var.get()
    text_editor.configure(font=("Helvetica", selected_size))

def set_font_type(event=None):
    selected_font = font_type_var.get()
    text_editor.configure(font=(selected_font, font_size_var.get()))

def set_font_color():
    color = askcolor()
    if color:
        text_editor.configure(fg=color[1])

def show_right_click_menu(event):
    right_click_menu.tk_popup(event.x_root, event.y_root)

def cut_text():
    text_editor.event_generate("<<Cut>>")

def copy_text():
    text_editor.event_generate("<<Copy>>")

def paste_text():
    text_editor.event_generate("<<Paste>>")

def delete_text():
    text_editor.delete("sel.first", "sel.last")

root = tk.Tk()
root.title("Text Editor")
root.geometry("800x600")

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New File", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save as PDF", command=save_as_pdf)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Create a toolbar frame
toolbar_frame = tk.Frame(root)
toolbar_frame.pack(side=tk.TOP, fill=tk.X)

# Font toolbar
font_toolbar = tk.Frame(toolbar_frame)
font_toolbar.pack(side=tk.LEFT, padx=5, pady=5)

font_size_var = tk.IntVar()
font_size_var.set(12)
font_size_label = tk.Label(font_toolbar, text="Font Size:", padx=5)
font_size_label.pack(side=tk.LEFT)
font_size_combo = ttk.Combobox(font_toolbar, textvariable=font_size_var, width=5, state="readonly")
font_size_combo['values'] = (5, 8, 10, 12, 14, 16, 18, 20, 24, 28)
font_size_combo.current(3)
font_size_combo.pack(side=tk.LEFT)
font_size_combo.bind("<<ComboboxSelected>>", set_font_size)

font_type_var = tk.StringVar()
font_type_var.set("Helvetica")
font_type_label = tk.Label(font_toolbar, text="Font Type:", padx=5)
font_type_label.pack(side=tk.LEFT)
font_type_combo = ttk.Combobox(font_toolbar, textvariable=font_type_var, width=10, state="readonly")
font_type_combo['values'] = ("Helvetica", "Arial", "Courier", "Times New Roman")
font_type_combo.current(0)
font_type_combo.pack(side=tk.LEFT)
font_type_combo.bind("<<ComboboxSelected>>", set_font_type)

font_color_button = tk.Button(font_toolbar, text="Font Color", command=set_font_color, width=10)
font_color_button.pack(side=tk.LEFT, padx=5)

# Create a canvas frame for the writable document area
canvas_frame = tk.Frame(root, bg="light grey")
canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Create a text editor
text_editor = tk.Text(canvas_frame, wrap=tk.WORD, undo=True)
text_editor.pack(fill=tk.BOTH, expand=True)
text_editor.focus()

# Right-click menu
right_click_menu = tk.Menu(root, tearoff=False)
right_click_menu.add_command(label="Cut", command=cut_text)
right_click_menu.add_command(label="Copy", command=copy_text)
right_click_menu.add_command(label="Paste", command=paste_text)
right_click_menu.add_command(label="Delete", command=delete_text)

# Bind right-click event to the text editor
text_editor.bind("<Button-3>", show_right_click_menu)

root.mainloop()
