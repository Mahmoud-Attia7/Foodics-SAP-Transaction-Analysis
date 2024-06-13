from tkinter import ttk
from tkinter import messagebox

from UI.ParametersWindow import BusinessDateWindow

class AuthCodeWindow:
    def __init__(self, root, analysis):
        self.root = root
        self.root.title("Auth Code Window")
        self.CenterWindow(300, 200)
        self.CreateWidgets()

        self.analysis = analysis

    def CenterWindow(self, width, height):
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set the geometry of the window
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def CreateWidgets(self):
        # Configure the style
        style = ttk.Style()
        style.configure("TLabel", foreground="white", background="darkblue", padding=10)
        style.configure("TEntry", padding=10)
        style.configure("TButton", padding=10, background="darkblue", foreground="darkblue")

        # Create and place the label
        self.label = ttk.Label(self.root, text="Auth Code", style="TLabel")
        self.label.pack(pady=10)

        # Create and place the entry widget
        self.entry = ttk.Entry(self.root)
        self.entry.pack(pady=10)

        # Create and place the submit button
        self.submit_button = ttk.Button(self.root, text="Submit", command=self.SubmitCode, style="TButton")
        self.submit_button.pack(pady=10)

    def SubmitCode(self):
        auth_code = self.entry.get()
        self.analysis.PrepareFoodicsAnalysis(auth_code)
        messagebox.showinfo("Submitted", f"Auth Code submitted: {auth_code}")
        BusinessDateWindow(self.root, self.analysis)
