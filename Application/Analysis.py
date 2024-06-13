import pandas as pd
from Application.Orders import Orders
from UI.Error_Window import ErrWindow


class TransactionsAnalysis:
    def __init__(self):
        self.errwindow = ErrWindow()
        self.sap_transactions = None
        self.orders = Orders()
        self.sap_file_path = 'Application/SAPFOODICSTRANSACTIONSCOMPARISON.xlsx'

    def PrepareFoodicsAnalysis(self, authURL=""):
        self.orders.PrepareFoodicsTransactions(authURL)

    def IsTokenAvailable(self):
        self.PrepareFoodicsAnalysis()
        is_available = self.orders.IsTokenAvailable()
        return is_available

    def SetBusinessDateAfter(self, business_date_after):
        self.orders.SetBusinessDateAfter(business_date_after)

    def SetBusinessDateBefore(self, business_date_before):
        self.orders.SetBusinessDateBefore(business_date_before)

    def NoneMatchingTransactions(food, sap, transaction_name):
        try:
            food['reference'] = food['reference'].astype(str)
            sap['Foodics Ref'] = sap['Foodics Ref'].astype(str)
            mask = ~food['reference'].isin(sap['Foodics Ref'])
            transactions = food[mask]
            return transactions
        except Exception as e:
            ErrWindow.show_error(f"An unexpected error occurred: {e}. {transaction_name}")

    def OrderAnalysis(self, sap_status, foodics_status=1):
        transaction_name = "unknown"
        if foodics_status == 4:
            transaction_name = "Orders"
        elif foodics_status == 5:
            transaction_name = "Return"

        try:
            self.sap_transactions = pd.ExcelFile(self.sap_file_path)
            foodics_orders = self.orders.GetOrders(foodics_status)
            unsorted_SAP_order = self.sap_transactions.parse(sap_status)[['Foodics Ref']]
            sorted_SAP_order = unsorted_SAP_order.sort_values(by='Foodics Ref')
            non_matching_orders = self.NoneMatchingTransactions(foodics_orders, sorted_SAP_order, transaction_name)
            print(non_matching_orders)
            return non_matching_orders
        except Exception as e:
            self.errwindow.show_error(f"An unexpected error occurred: {e}. {transaction_name}")
