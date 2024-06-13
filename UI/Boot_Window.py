from Application.Analysis import TransactionsAnalysis
from UI.Auth_Code_Window import AuthCodeWindow
from UI.ParametersWindow import BusinessDateWindow


class BootWindow:
    def __init__(self, root):
        self.root = root
        self.analysis = TransactionsAnalysis()
        self.BootUp()

    def BootUp(self):
        is_available = self.analysis.IsTokenAvailable()
        if not is_available:
            AuthCodeWindow(self.root, self.analysis)
        elif is_available:
            BusinessDateWindow(self.root, self.analysis)
