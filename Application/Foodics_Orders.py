import sys
import pandas as pd
from UI.Error_Window import ErrWindow
from datetime import datetime, timedelta
from Data_Access.Foodics_Transactions import FoodicsTransaction


class Foodics_Orders:
    def __init__(self):
        self.errwindow = ErrWindow()
        self.transactions =  FoodicsTransaction()
        self.end_point = "https://api-sandbox.foodics.com/v5/orders"
        self.business_date_after = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
        self.business_date_before = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    def SetBusinessDateAfter(self, business_date_after):
        self.business_date_after = business_date_after

    def SetBusinessDateBefore(self, business_date_before):
        self.business_date_before = business_date_before

    def PrepareFoodicsTransactions(self, authURL):
        self.transactions.PrepareFoodicsMethods(authURL)

    def IsTokenAvailable(self):
        is_available = self.transactions.IsTokenAvailable()
        return is_available

    def GetOrders(self, status):
        try:
            URL = self.end_point + "?" + "sort=reference" + "&" + "filter[status]=" + str(status) + "&" + "filter[status]=" + str(1) \
                # + "&" + f"filter[business_date_after]={self.business_date_after}" + "&" +\
            # f"filter[business_date_before]={self.business_date_before}"
            orders_data_json = self.transactions.GetTransactionJSON(URL)
            orders_extracted_data = [{'id': row['id'], 'reference': row['reference'], 'business_date': row['business_date']} for row in orders_data_json['data']]
            if not orders_extracted_data:
                orders_extracted_data = [{'id': None, 'reference': None, 'business_date': None}]

            orders_data_frame = pd.DataFrame(orders_data_json['data'])
            return orders_data_frame

        except Exception as e:
            self.errwindow.show_error(f"An unexpected error occurred: {e}.")
            sys.exit()
