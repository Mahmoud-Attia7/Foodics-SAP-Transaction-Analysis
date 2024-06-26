from UI.Error_Window import ErrWindow
from Application.Foodics_Orders import Foodics_Orders
from Application.SAP_Orders import SAP_Orders

class TransactionsAnalysis:
    def __init__(self):
        self.errwindow = ErrWindow()
        self.food_orders = Foodics_Orders()
        self.sap_orders = SAP_Orders()

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

    def OrderAnalysis(self, transaction_type, foodics_status=1):
        transaction_name = "unknown"
        if foodics_status == 4:
            transaction_name = "Foodics_Orders"
        elif foodics_status == 5:
            transaction_name = "Return"

        try:
            foodics_orders = self.food_orders.GetOrders(foodics_status)
            unsorted_SAP_order = self.sap_orders.Get_Orders(transaction_type)
            sorted_SAP_order = unsorted_SAP_order.sort_values(by='Foodics Ref')
            non_matching_orders = self.NoneMatchingTransactions(foodics_orders, sorted_SAP_order, transaction_name)
            print(non_matching_orders)
            return non_matching_orders
        except Exception as e:
            self.errwindow.show_error(f"An unexpected error occurred: {e}. {transaction_name}")
