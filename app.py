# ===============================================
# 🤖 FAQ Chatbot (Task 2 - NLP Project)
# Developed by Moaavea
# ===============================================

import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------
# 🧠 NLTK Setup (Fixed Downloader)
# -------------------------------
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("punkt_tab")

# -------------------------------
# 📘 Step 1: Collect FAQs
# -------------------------------
faqs = {
    "What is your return policy?": "You can return any item within 30 days of purchase with your receipt.",
    "How can I track my order?": "Once your order ships, you will receive a tracking link via email.",
    "Do you offer international shipping?": "Yes, we deliver to over 50 countries worldwide.",
    "How do I contact customer support?": "Our support team is available 24/7 via live chat or email.",
    "What payment methods are accepted?": "We accept Visa, MasterCard, PayPal, and Amazon Pay.",
    "How can I cancel my order?": "Orders can be canceled within 2 hours of purchase from your account.",
    "Can I change my shipping address after placing an order?": "Yes, you can update your shipping address within 1 hour of ordering.",
    "Is cash on delivery available?": "Yes, cash on delivery is available in selected regions.",
    "Do you have a mobile app?": "Yes, our mobile app is available on both Android and iOS platforms.",
    "What should I do if I received a damaged item?": "Please contact our support team immediately with a picture of the damaged item."
}

faq_questions = list(faqs.keys())
faq_answers = list(faqs.values())

# -------------------------------
# 🧹 Step 2: Preprocessing Function
# -------------------------------
def preprocess(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [
        t for t in tokens
        if t not in stopwords.words('english') and t not in string.punctuation
    ]
    return " ".join(tokens)

processed_questions = [preprocess(q) for q in faq_questions]

# -------------------------------
# 🔢 Step 3: TF-IDF + Cosine Similarity
# -------------------------------
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(processed_questions)

def get_best_answer(user_query):
    user_query_processed = preprocess(user_query)
    user_vector = vectorizer.transform([user_query_processed])
    similarity = cosine_similarity(user_vector, faq_vectors)
    best_index = similarity.argmax()
    best_score = similarity[0, best_index]

    if best_score < 0.3:
        return "🤔 Sorry, I’m not sure about that. Try rephrasing your question."
    else:
        return faq_answers[best_index]

# -------------------------------
# 💬 Step 4: Streamlit Chat UI
# -------------------------------
st.set_page_config(page_title="FAQ Chatbot", page_icon="🤖", layout="centered")

# Sidebar - settings
st.sidebar.title("⚙️ Chatbot Settings")

theme = st.sidebar.radio("🎨 Choose Page Color:", ["White", "Light Blue", "Light Green", "Lavender"])

# Background colors
bg_colors = {
    "White": "#FFFFFF",
    "Light Blue": "#E6F0FF",
    "Light Green": "#E9FFE8",
    "Lavender": "#F3E8FF"
}

# Apply improved color styles
page_bg = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-color: {bg_colors[theme]};
}}
[data-testid="stSidebar"] {{
    background-color: #144272;
    color: white;
}}
[data-testid="stSidebar"] .st-radio label {{
    color: white;
    font-weight: 500;
}}
[data-testid="stSidebar"] .stButton>button {{
    color: white;
    background-color: #205295;
    border-radius: 10px;
    border: none;
    transition: 0.3s;
}}
[data-testid="stSidebar"] .stButton>button:hover {{
    background-color: #2C74B3;
    transform: scale(1.03);
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -------------------------------
# 💾 Session State (Chat History)
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Sidebar Buttons
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state["chat_history"] = []

if st.sidebar.button("📥 Download Chat"):
    if st.session_state["chat_history"]:
        chat_text = "\n".join([f"{role}: {msg}" for role, msg in st.session_state["chat_history"]])
        st.sidebar.download_button(
            label="⬇️ Download as TXT",
            data=chat_text,
            file_name="chat_history.txt",
            mime="text/plain"
        )
    else:
        st.sidebar.warning("No chat history to download yet!")

if st.sidebar.button("📖 Show All FAQs"):
    st.sidebar.markdown("### 💡 Frequently Asked Questions:")
    for q in faq_questions:
        st.sidebar.markdown(f"- {q}")

# -------------------------------
# 🖥️ Main Page
# -------------------------------
st.title("🤖 Smart FAQ Chatbot")
st.caption("NLP Task 2 — Built with NLTK, TF-IDF, and Cosine Similarity")
st.markdown("---")

# User input
user_input = st.text_input("💬 Ask a question:")

if user_input:
    response = get_best_answer(user_input)
    st.session_state["chat_history"].append(("🧑‍💻 You", user_input))
    st.session_state["chat_history"].append(("🤖 Bot", response))

# Display chat history
for role, message in st.session_state["chat_history"]:
    st.markdown(f"**{role}:** {message}")
