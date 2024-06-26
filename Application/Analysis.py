from UI.Error_Window import ErrWindow
from Application.Foodics_Orders import Foodics_Orders
from Application.SAP_Orders import SAP_Orders
from Data_Access.Analysis_Result import Analysis_Result

class TransactionsAnalysis:
    def __init__(self):
        self.errwindow = ErrWindow()
        self.food_orders = Foodics_Orders()
        self.sap_orders = SAP_Orders()
        self.analysis_result = Analysis_Result()

    def PrepareFoodicsAnalysis(self, authURL=""):
        self.food_orders.PrepareFoodicsTransactions(authURL)

    def IsTokenAvailable(self):
        self.PrepareFoodicsAnalysis()
        is_available = self.food_orders.IsTokenAvailable()
        return is_available

    def SetBusinessDateAfter(self, business_date_after):
        self.food_orders.SetBusinessDateAfter(business_date_after)

    def SetBusinessDateBefore(self, business_date_before):
        self.food_orders.SetBusinessDateBefore(business_date_before)

    def NoneMatchingTransactions(self, food, sap, transaction_name):
        try:
            food['reference'] = food['reference'].astype(str)
            sap['Foodics Ref'] = sap['Foodics Ref'].astype(str)
            mask = ~food['reference'].isin(sap['Foodics Ref'])
            transactions = food[mask]
            return transactions
        except Exception as e:
            ErrWindow.show_error(f"An unexpected error occurred: {e}. {transaction_name}")

    def OrderAnalysis(self, sap_transaction_type, foodics_status=1):
        transaction_type = "unknown"
        if foodics_status == 4:
            transaction_type = "Orders"
        elif foodics_status == 5:
            transaction_type = "Return"

        try:
            foodics_orders = self.food_orders.GetOrders(foodics_status)
            unsorted_SAP_order = self.sap_orders.Get_Orders(sap_transaction_type)
            sorted_SAP_order = unsorted_SAP_order.sort_values(by='Foodics Ref')
            non_matching_orders = self.NoneMatchingTransactions(foodics_orders, sorted_SAP_order, transaction_type)
            self.analysis_result.Store_Result(non_matching_orders, transaction_type)
        except Exception as e:
            self.errwindow.show_error(f"An unexpected error occurred: {e}. {transaction_type}")
