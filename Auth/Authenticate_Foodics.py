import os
import sys
import time
import json
import base64
import webbrowser
from requests.exceptions import HTTPError, RequestException
from authlib.integrations.requests_client import OAuth2Session
from Auth.Symmetric_Data_Encryption_Decryption import SymmetricDataED
from UI.Error_Window import ErrWindow


class AuthFoodics:
    def __init__(self):
        self.file_path = 'Auth/XJEHTY.json'
        self.client_ID = '9bac1607-0aa3-430e-8f28-a3308d32c4bf'
        self.client_secret = 'rbWGDQxZse5YphnvJyUxuV7zFw3MGEJ5IQK04V6E'
        self.redirect_uri = 'https://console-sandbox.foodics.com/dashboard'
        self.token_endpoint = 'https://api-sandbox.foodics.com/oauth/token'
        self.authorization_endpoint = 'https://console-sandbox.foodics.com/authorize'
        self.client = OAuth2Session(self.client_ID, self.client_secret, redirect_uri=self.redirect_uri)
        self.errwindow = ErrWindow()

    def BrowsLoginFoodics(self):
        try:
            uri, state = self.client.create_authorization_url(self.authorization_endpoint)
            webbrowser.open(uri)
        except Exception as e:
            self.errwindow.show_error(f"An unexpected error occurred: {e}.")
            sys.exit()

    def IsTokenAvailable(self):
        is_available = False
        current_time = time.time()
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                expires_at = SymmetricDataED.decrypt(base64.b64decode(data['expires_at']))
                if current_time <= int(expires_at):
                    is_available = True
        return is_available

    def GetFoodicsToken(self, redirect_url='', counter=0):
        expires_at = 'none'
        token_type = 'none'
        access_token = 'none'
        current_time = time.time()
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                access_token = SymmetricDataED.decrypt(base64.b64decode(data['access_token']))
                token_type = SymmetricDataED.decrypt(base64.b64decode(data['token_type']))
                expires_at = SymmetricDataED.decrypt(base64.b64decode(data['expires_at']))

        if not os.path.exists(self.file_path) or current_time >= int(expires_at):
            self.BrowsLoginFoodics()
            try:
                if os.path.exists(self.file_path):
                    os.remove(self.file_path)
                    self.errwindow.show_error("access token is expired.")
                authorization_response = redirect_url
                token = self.client.fetch_token(self.token_endpoint, authorization_response=authorization_response)
                access_token = base64.b64encode(SymmetricDataED.encrypt(token['access_token'])).decode('utf-8')
                token_type = base64.b64encode(SymmetricDataED.encrypt(token['token_type'])).decode('utf-8')
                expires_at = base64.b64encode(SymmetricDataED.encrypt(str(token['expires_at']))).decode('utf-8')
                data = {
                    "access_token": access_token,
                    "token_type": token_type,
                    "expires_at": expires_at,
                }

                access_token = token['access_token']
                token_type = token['token_type']

                with open(self.file_path, 'w') as json_file:
                    json.dump(data, json_file, indent=3)

                counter = 0

            except HTTPError as http_err:
                status_code = http_err.response.status_code
                max_retries = {404: 1, 422: 1, 429: 2, 500: 4}

                if status_code in max_retries and counter < max_retries[status_code]:
                    return self.GetFoodicsToken(redirect_url, counter + 1)  # Correct function name
                elif status_code == 401:
                    self.errwindow.show_error(f"No valid Access Token was given. Attempt {counter}")
                elif status_code == 403:
                    self.errwindow.show_error(f"You do not have permission to access this resource. Attempt {counter}")
                elif status_code == 503:
                    self.errwindow.show_error(f"Foodics is offline for maintenance. Attempt {counter}")
                else:
                    self.errwindow.show_error(f"An error occurred: {status_code}. Attempt {counter}")

            except RequestException as e:
                self.errwindow.show_error(f"A request error occurred: {e}. Attempt {counter}")

            except Exception as e:
                self.errwindow.show_error(f"An unexpected error occurred: {e}. Attempt {counter}")

        return access_token, token_type
