from predictor import predict, load_model
import streamlit as st

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