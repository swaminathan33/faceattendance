import os
from twilio.rest import Client
import streamlit as st 

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['']
auth_token = os.environ['']
client = Client(account_sid, auth_token)

token = client.tokens.create()

st.write(token.username)
