import os
from twilio.rest import Client
import streamlit as st 

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['AC7f2519f83b89dfc14bf4f9f5de79e627']
auth_token = os.environ['9d02b0abb343f657e1d7ce37caa6d016']
client = Client(account_sid, auth_token)

token = client.tokens.create()

st.write(token.username)
