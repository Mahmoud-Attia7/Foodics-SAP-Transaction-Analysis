#!/usr/bin/env python
# coding: utf-8

# In[23]:


import requests
from Error_Window import ErrWindow
from requests.exceptions import HTTPError
from Authenticate_Foodics import AuthFoodics


# In[24]:


class FoodAPIMethods:
    def __init__(self, url):
        self.errwindow = ErrWindow()
        self.auth = AuthFoodics()
        self.access_token, self.token_type = self.auth.GetFoodicsToken(url)
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
            
    def Get_Transaction(self, end_point, counter=0):
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
            elif status_code == 403:
                self.errwindow.show_error("You do not have permission to access this resource.")
            elif status_code == 503:
                self.errwindow.show_error("Service is offline for maintenance.")
            else:
                self.errwindow.show_error(f"An error occurred: {status_code}. Attempt {counter}")

        except requests.RequestException as e:
            self.errwindow.show_error(f"A request error occurred: {e}. Attempt {counter}")

        except Exception as e:
            self.errwindow.show_error(f"An unexpected error occurred: {e}. Attempt {counter}")

        return None        

