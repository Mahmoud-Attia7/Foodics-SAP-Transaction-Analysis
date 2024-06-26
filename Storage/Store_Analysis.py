import os
import pandas as pd
from datetime import datetime

class Store_Analysis:
    def __init__(self):
        folder_path = 'Result'
        os.makedirs(folder_path, exist_ok=True)
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.non_matching_transactions_excel_path = os.path.join(folder_path, f'transactions_{current_time}.xlsx')

    def Store_Non_Matching_Transactions(self, non_matching_transactions, transaction_type):
        with pd.ExcelWriter(self.non_matching_transactions_excel_path, engine='xlsxwriter') as writer:
            non_matching_transactions.to_excel(writer, sheet_name=transaction_type, index=False)
