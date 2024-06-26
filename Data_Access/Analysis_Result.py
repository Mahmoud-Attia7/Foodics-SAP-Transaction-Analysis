from  Storage.Store_Analysis import Store_Analysis

class Analysis_Result:
    def __init__(self):
        self.analysis_store = Store_Analysis()

    def Store_Result(self, non_matching_transactions, transaction_type):
        self.analysis_store.Store_Non_Matching_Transactions(non_matching_transactions, transaction_type)
