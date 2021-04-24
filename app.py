from predictor import predict, load_model
import streamlit as st
import json, uuid

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

firebase_login_details = {
  "type": st.secrets['TYPE'],
  "project_id": st.secrets['PROJECT_ID'],
  "private_key_id": st.secrets['PRIVATE_KEY_ID'],
  "private_key": st.secrets['PRIVATE_KEY'],
  "client_email": st.secrets['CLIENT_EMAIL'],
  "client_id": st.secrets['CLIENT_ID'],
  "auth_uri": st.secrets['AUTH_URI'],
  "token_uri": st.secrets['TOKEN_URI'],
  "auth_provider_x509_cert_url": st.secrets['AUTH_PROVIDER_CERT_URL'],
  "client_x509_cert_url": st.secrets['CLIENT_CERT_URL'],
}

# save to file
with open('firebase_login.json', 'w+') as output:
	# dump to JSON
	json.dump(firebase_login_details, output)

# login to firebase
# must check if already initialized
# somehow streamlit loves to rerun the
# code. idk why
if not firebase_admin._apps:
	cred = credentials.Certificate('firebase_login.json')
	firebase_admin.initialize_app(cred)

db = firestore.client()

# set page config
st.set_page_config(
	page_title="Detect Clickbait with Ease",
	page_icon="😎"
)

# load model
with st.spinner("Loading our awesome ML model. Please wait ..."):
	model = load_model()

@st.cache
def handle_text(text):
	return predict(model, text)

# title and subtitle
st.title("Painless Way to Detect Clickbait 😎")
st.write("Do you think your favorite news portal is credible, trustworthy, and not using clickbait?")
st.write("Well, just ask the machine if they think so 😆")
st.write("It's easy and (hopefully 😛) fast. Put news' title down below and we will take care the rest 😉")

# user input
news_title = st.text_area(
	label="News Title:",
	help="Input your news' title here, then click anywhere outside the box. We'll take care the rest 😀"
)

if news_title != "":
	prediction = handle_text(news_title)

	# check prediction
	if prediction > 50:
		st.write("NOOOO! It's a clickbait 😱😱")
		st.write(f"We're {round(prediction, 3)}% sure it's a clickbait")
	else:
		st.write("YAY! It's not a clickbait 🥰🥰")
		st.write(f"We're {round(100-prediction, 3)}% sure it's not a clickbait")