import sys
import pandas as pd
from UI.Error_Window import ErrWindow
from Data_Access.SAP_Transactions import SAP_Transactions

class SAP_Orders:
    def __init__(self):
        self.errwindow = ErrWindow()
        self.transactions = SAP_Transactions()

    def Get_Orders(self, transaction_type):
        orders = self.transactions.Get_Transaction_Data_Frame(transaction_type)
        return orders
