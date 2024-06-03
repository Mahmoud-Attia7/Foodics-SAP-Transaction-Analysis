#!/usr/bin/env python
# coding: utf-8

# In[13]:


import os
import json
import datetime
import webbrowser
import tkinter as tk
from tkinter import messagebox
from requests.exceptions import HTTPError
from authlib.integrations.requests_client import OAuth2Session


# In[14]:


class AuthFoodics:
    def __init__(self):
        self.file_path = 'XJEHTY.json'
        self.clien_ID = '********'
        self.client_secret = '********'
        self.redirect_uri = 'https://console-sandbox.foodics.com/dashboard'
        self.token_endpoint  = 'https://api-sandbox.foodics.com/oauth/token'
        self.authorization_endpoint  = 'https://console-sandbox.foodics.com/authorize'
    
    def Brows_Login_Foodics(self):
        self.client = OAuth2Session(self.clien_ID, self.client_secret, redirect_uri=self.redirect_uri)
        uri, state = self.client.create_authorization_url(self.authorization_endpoint)
        webbrowser.open(uri)
        
    def Get_Token(self, redirect_url=''):
        
        counter = 0
        expires_at = ''
        token_type = ''
        access_token = ''
        
        if os.path.exists(self.file_path):
            file = open(self.file_path, 'r')
            data = json.load(file)
            access_token = data['access_token']
            token_type = data['token_type']
            expires_at = data['expires_at']
            file.close()
            
        else:        
            try:
                authorization_response = redirect_url
                token = self.client.fetch_token(
                self.token_endpoint,
                authorization_response=authorization_response,
                )
                expires_at = token['expires_at'].strftime('%Y-%m-%d %H:%M:%S')
                data = {
                            "access_token": token['access_token'],
                            "token_type": token['token_type'],
                            "expires_at": expires_at,
                        }
                with open(self.file_path, 'w') as json_file:
                    json.dump(data, json_file, indent=3)
                counter = 0  

            except HTTPError as http_err:
                status_code = http_err.response.status_code
                if status_code == 404 and counter < 1:
                    counter += 1
                    self.Get_Token(redirect_url)
                elif status_code == 422 and counter < 1:
                    counter += 1
                    self.Get_Token(redirect_url)
                elif status_code == 429 and counter < 2:
                    counter += 1
                    self.Get_Token(redirect_url)
                elif status_code == 500 and counter < 4:
                    counter += 1
                    self.Get_Token(redirect_url)
                elif status_code == 503:
                    show_error("Foodics is offline for maintenance.")
                else:
                    show_error(f"An error occurred: {http_err}")
            except Exception as e:
                show_error(f"An error occurred: {e}")
            
        return access_token, token_type, expires_at
    
    def show_error(self, message):
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showerror("Error", message)
        root.destroy()


# In[ ]:




