import sys
import requests
from UI.Error_Window import ErrWindow
from requests.exceptions import HTTPError
from Auth.Authenticate_Foodics import AuthFoodics


class FoodAPIMethods:
    def __init__(self):
        self.errwindow = ErrWindow()
        self.auth = AuthFoodics()
        self.access_token = None
        self.token_type = None
        self.headers = None

    def PrepareFoodicsToken(self, authURL):
        self.access_token, self.token_type = self.auth.GetFoodicsToken(authURL)
        self.headers = {
            'Authorization': f'{self.token_type} {self.access_token}',
            'Content-Type': 'application/json'
        }

    def IsTokenAvailable(self):
        is_available = self.auth.IsTokenAvailable()
        return is_available

    def GetTransaction(self, end_point, counter=0):
        max_retries = {404: 1, 422: 1, 429: 2, 500: 4}

        try:
            response = requests.get(end_point, headers=self.headers)
            response.raise_for_status()

            if response.status_code == 200:
                return response.json()

        except HTTPError as http_err:
            status_code = http_err.response.status_code
            if status_code in max_retries and counter < max_retries[status_code]:
                return self.GetTransaction(end_point, counter + 1)
            elif status_code == 401:
                self.errwindow.show_error("No valid Access Token was given.")
                sys.exit()
            elif status_code == 403:
                self.errwindow.show_error("You do not have permission to access this resource.")
                sys.exit()
            elif status_code == 503:
                self.errwindow.show_error("Service is offline for maintenance.")
                sys.exit()
            else:
                self.errwindow.show_error(f"An error occurred: {status_code}. Attempt {counter}")
                sys.exit()

        except requests.RequestException as e:
            self.errwindow.show_error(f"A request error occurred: {e}. Attempt {counter}")
            sys.exit()

        except Exception as e:
            self.errwindow.show_error(f"An unexpected error occurred: {e}. Attempt {counter}")
            sys.exit()
