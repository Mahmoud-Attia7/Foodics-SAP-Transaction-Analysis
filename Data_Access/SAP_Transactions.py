import sys
from UI.Error_Window import ErrWindow
from Storage.SAP_API_Methods import SAP_API_Methods


class SAP_Transactions:
    def __init__(self):
        self.sap_api_methods = SAP_API_Methods()
        self.errwindow = ErrWindow()

    def Get_Transaction_Data_Frame(self, transaction_type):
        try:
            sap_transaction = self.sap_api_methods.Get_Transactions(transaction_type)
            return sap_transaction
        except Exception as e:
            self.errwindow.show_error(f"An unexpected error occurred: {e}.")
            sys.exit()
