import streamlit as st
from datetime import datetime, timedelta
from dateparser import parse
import re

from langgraph_flow import app as langgraph_app
from calendar_helper import get_calendar_service, check_availability, book_event

uploaded_token = st.file_uploader(" Upload your token.pkl file to enable calendar access", type="pkl")

if uploaded_token:
    with open("token.pkl", "wb") as f:
        f.write(uploaded_token.read())
    st.success(" token.pkl uploaded successfully!")
else:
    st.warning(" Please upload your token.pkl file to proceed.")
    st.stop()


st.set_page_config(page_title="TailorTalk Agent", layout="centered")
st.title("🤖 TailorTalk - Appointment Booking Assistant")

# Load calendar service once
if "calendar_service" not in st.session_state:
    try:
        st.session_state.calendar_service = get_calendar_service()
    except Exception as e:
        st.error(f" Failed to load calendar: {e}")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
user_input = st.chat_input("When would you like to book an appointment?")

if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # LangGraph step
    state = {"input_text": user_input}
    output = langgraph_app.invoke(state)
    extracted = output.get("extracted_time", "Sorry, couldn't parse that.")
    st.chat_message("assistant").write(f"📅 I understood this time: **{extracted}**")

    # Clean and parse
    cleaned = re.sub(r"\bat\b", "", extracted).strip()
    dt = parse(cleaned)

    if dt:
        end_dt = dt + timedelta(minutes=30)

        try:
            # Use preloaded service
            service = get_calendar_service()#st.session_state.calendar_service
            if check_availability(dt, end_dt, service):
                link = book_event("TailorTalk Meeting", dt, end_dt,service)
                reply = f" Booking confirmed!\n[Join Link]({link})"
            else:
                reply = " That slot is already booked. Try another time."
        except Exception as e:
            reply = f" Error during booking: {e}"
    else:
        reply = " I couldn't understand the time."

    st.chat_message("assistant").write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

