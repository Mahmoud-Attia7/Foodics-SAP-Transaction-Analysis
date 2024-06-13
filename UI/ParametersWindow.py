import tkinter as tk

from tkinter import ttk
from tkinter import messagebox


class BusinessDateWindow:
    def __init__(self, parent, analysis):
        self.analysis = analysis

        self.window = tk.Toplevel(parent)
        self.window.title("Business Dates")

        self.CenterWindow(400, 300)
        self.CreateWidgets()

    def CenterWindow(self, width, height):
        # Get the screen width and height
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set the geometry of the window
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def CreateWidgets(self):
        # Configure the style
        style = ttk.Style()
        style.configure("TLabel", foreground="white", background="darkblue", padding=10)
        style.configure("TEntry", padding=10)
        style.configure("TButton", padding=10, background="darkblue", foreground="darkblue")

        # Create and place the labels and entry widgets
        self.label_from = ttk.Label(self.window, text="Business Date From", style="TLabel")
        self.label_from.pack(pady=10)

        self.entry_from = ttk.Entry(self.window)
        self.entry_from.pack(pady=5)

        self.label_to = ttk.Label(self.window, text="Business Date To", style="TLabel")
        self.label_to.pack(pady=10)

        self.entry_to = ttk.Entry(self.window)
        self.entry_to.pack(pady=5)

        # Create and place the submit button
        self.submit_button = ttk.Button(self.window, text="Submit", command=self.SubmitDates, style="TButton")
        self.submit_button.pack(pady=20)

    def SubmitDates(self):
        date_from = self.entry_from.get()
        date_to = self.entry_to.get()
        self.analysis.SetBusinessDateAfter(date_from)
        self.analysis.SetBusinessDateBefore(date_to)
        self.analysis.OrderAnalysis("SR", 5)
        self.analysis.OrderAnalysis("SO")
        messagebox.showinfo("Submitted", f"Data is now Available at result folder")
