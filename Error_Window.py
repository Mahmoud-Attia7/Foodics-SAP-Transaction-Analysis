#!/usr/bin/env python
# coding: utf-8

# In[6]:


import ctypes


# In[7]:


class ErrWindow:
    def show_error(self, message):
        # Show the error message box
        ctypes.windll.user32.MessageBoxW(0, message, "Error", 0x10)

