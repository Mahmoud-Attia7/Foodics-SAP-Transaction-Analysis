import pandas as pd
from UI.Error_Window import ErrWindow

class SAP_API_Methods:
    def __init__(self):
        self.errwindow = ErrWindow()
        self.sap_transactions = None
        self.sap_file_path = 'Storage/SAPFOODICSTRANSACTIONSCOMPARISON.xlsx'

    def Get_Transactions(self, transaction_type):
        try:
            self.sap_transactions = pd.ExcelFile(self.sap_file_path)
            unsorted_SAP_order = self.sap_transactions.parse(transaction_type)[['Foodics Ref']]
            return unsorted_SAP_order
        except Exception as e:
            self.errwindow.show_error(f"An unexpected error occurred: {e}")
