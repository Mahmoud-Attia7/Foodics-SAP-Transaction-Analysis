import sys
from UI.Error_Window import ErrWindow
from Storage.Foodics_API_Methods import FoodAPIMethods


class FoodicsTransaction:
    def __init__(self):
        self.foodics_api_methods = FoodAPIMethods()
        self.errwindow = ErrWindow()

    def PrepareFoodicsMethods(self, authURL):
        self.foodics_api_methods.PrepareFoodicsToken(authURL)

    def IsTokenAvailable(self):
        is_available = self.foodics_api_methods.IsTokenAvailable()
        return is_available

    def GetTransactionJSON(self, url, current_page=1):
        try:
            print(url + f'&page={str(current_page)}')
            endpointURL = url + '&' + 'page=' + str(current_page)
            data_json = self.foodics_api_methods.GetTransaction(endpointURL)
            if current_page < data_json['meta']['last_page']:
                next_page = current_page + 1
                new_json = self.GetTransactionJSON(url, current_page=next_page)
                data_json['data'] = data_json['data'] + new_json['data']
            return data_json
        except Exception as e:
            self.errwindow.show_error(f"An unexpected error occurred: {e}.")
            sys.exit()

