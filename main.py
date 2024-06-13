import tkinter as tk
from UI.Auth_Code_Window import AuthCodeWindow
from Application.Analysis import TransactionsAnalysis
from UI.Boot_Window import BootWindow

# authURL = 'https://console-sandbox.foodics.com/dashboard?code=def5020082c06093752f02e896626304960e4ba87003b6b8b01' \
#           '23e753f5f70f4439c996c5de910d06f60b5bd5b346617429425b67c3a9b9f06af2702478d2c2cedf7b64278ccfdf3d571848e107' \
#           '1a83109b44f3d599fd8465b92b2c7a0307da00a452489756d9bfebe3e45e983d28463d588996b610074b66190d40b0f72769b22dee' \
#           '86e02e4809ba1c0354a24f5472fcad4436067474268f56dadd15471fdfc8d446c45179d328be88585fc92a696d7968e348950eb95' \
#           'f5da809fdca12f2d20917d0ad797c71c6bcad5ee38157ac741bfa511ffbce38b1011f9218848c6978f2bc34d56a3ed1195547d8dd' \
#           '655a39712fe661eeedfb7f75680be1bef7b18e1a3fc971ed3ee056634890b10ddd22b6acfe545ded668a2c980cde0a0994f88962e' \
#           '5b342303cd6b2eaeb2b411010bed8facb86d6d172eb289f1ce8b31c2f7db2fb1e080f8e47533f6042ec9ccc8c303097263d1595c' \
#           '3d0253b69d8da9ba7f62291e9f52a7784cfed932f31a9b227d33ae47f59a21f5e3fa95888bedbce281b0594341a9f4e82bec7fe4' \
#           'e8d82899784c8c318e01fa7906207923ff5eb283a41b9491792dea1c64142ececc8b197d1bf96beedda16cf28e&state=random_string'
# b_date_after = '2024-5-28'
# b_date_before = '2024-06-06'
# OT = TransactionsAnalysis(authURL)
# return_transactions = OT.Order_Analysis("SR", 5)
# order_transactions = OT.Order_Analysis("SO")
# print(order_transactions)

root = tk.Tk()
BootWindow(root)
root.mainloop()
