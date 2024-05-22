import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import zipfile
import os

class ZipFileApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Zipper")
        self.root.geometry("500x400")

        self.file_paths = []

        style = ttk.Style()
        style.configure("TFrame", background="white")
        style.configure("TLabel", background="white")
        style.configure("TButton", padding=6, relief="flat", background="#0078d7", foreground="white")
        style.map("TButton",
                  background=[('active', '#005a9e')])

        self.frame = ttk.Frame(root, padding=10)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.label = ttk.Label(self.frame, text="Select files to zip", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.select_button = ttk.Button(self.frame, text="Select Files", command=self.add_files)
        self.select_button.grid(row=1, column=0, pady=10)

        self.remove_button = ttk.Button(self.frame, text="Remove Selected Files", command=self.remove_files)
        self.remove_button.grid(row=1, column=1, pady=10)

        self.listbox_frame = ttk.Frame(self.frame)
        self.listbox_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)

        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.scrollbar = ttk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self.listbox_frame, selectmode=tk.MULTIPLE, bg='white', fg='black', selectbackground='#cce6ff', yscrollcommand=self.scrollbar.set)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.listbox.yview)

        self.zip_button = ttk.Button(self.frame, text="Generate ZIP", command=self.generate_zip)
        self.zip_button.grid(row=3, column=0, columnspan=2, pady=20)

    def add_files(self):
        files = filedialog.askopenfilenames()
        for file in files:
            if file not in self.file_paths:
                self.file_paths.append(file)
                self.listbox.insert(tk.END, os.path.basename(file))

    def remove_files(self):
        selected_indices = self.listbox.curselection()
        for index in reversed(selected_indices):
            self.listbox.delete(index)
            del self.file_paths[index]

    def generate_zip(self):
        if not self.file_paths:
            messagebox.showwarning("No files", "No files to zip!")
            return

        zip_path = filedialog.asksaveasfilename(defaultextension=".zip",
                                                filetypes=[("Zip files", "*.zip")])
        if not zip_path:
            return

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in self.file_paths:
                zipf.write(file, os.path.basename(file))

        messagebox.showinfo("Success", f"ZIP file created at {zip_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZipFileApp(root)
    root.mainloop()
