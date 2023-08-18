
from os import uname_result
import streamlit as st
import pandas as pd



def page_designs():
    st.markdown(
        r"""
        # Contact :phone:"""
    )
    st.markdown("---")

page_designs()


def mail_contact():

    st.caption("Need help? Contact us through email or phone!Our customer support team will contact you within 24 hours")
    st.subheader("Contact through mail :mailbox:")
    contact_form = '''
    <form action="https://formsubmit.co/customerhelp.ssncms@gmail.com" method="POST">
        <input type="text" name="name" placeholder = "Your name" required>
        <input type="email" name="email" placeholder = "Your email" required>
        <textarea name="message" placeholder="What issue are you facing?"></textarea>
        <button type="submit">Send</button>
        <input type="hidden" name="_captcha" value="false">
    </form>
    '''

    st.markdown(contact_form,unsafe_allow_html = True)


mail_contact()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

local_css("C:/Users/Lenovo/Desktop/endsem_project/style/style.css")

def phone_contact():
    st.subheader("Contact through phone :phone:")
    col1,col2 = st.columns(2)
    with col1:
        st.write("Contact number  1: 7010821856")
        st.write("Contact number  2: 9092093093")

    with col2:
        st.write("Name: Aditi Rajesh")
        st.write("Name: Adharsh Gurudev")

    st.caption("Thank you for using SSN CMS!")

phone_contact()
