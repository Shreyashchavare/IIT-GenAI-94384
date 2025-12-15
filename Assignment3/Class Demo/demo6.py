import streamlit as st

st.title("DKTE")

def show_aboutus_page():
    st.header("About Us")
    st.write("At DKTE we believe retaining a competitve edge is imperative for any individual in today's professional world. ")

def show_courses_page():
    st.header("Courses")
    st.write("We provide the different undergraduate, postgraduate and diploma courses in various sectors. We provide industry related knowledge and skills")
    st.write("""
    *BTech: 
            1.Computer Science and Engineering
            2.Artificial Intelligence and Machine Learning
            3.Artificial Intelligence and Data Science
            4.Electronics and Telecommunication        
     """)
    
def show_contactus_page():
    st.header("Contact Us")
    st.markdown("##DKTE Ichalkaranji")
    st.write("""
    P. O. Box = 130, Rajwada, Ichalkaranji-416 115, MH-INDIA
""")
    
if 'page' in st.session_state:
    st.session_state.page = "About Us"

with st.sidebar:
    if st.button("About us", width="stretch"):
        st.session_state.page = show_aboutus_page()
    if st.button("Courses", width="stretch"):
        st.session_state.page = show_courses_page()
    if st.button("Contact Us",width="stretch"):
        st.session_state.page = show_contactus_page()