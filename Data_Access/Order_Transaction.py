from Data_Access.Foodics_Transactions import FoodicsTransaction


class OrderTransactions(FoodicsTransaction):
    def __init__(self, authURL):
        super().__init__(authURL)
