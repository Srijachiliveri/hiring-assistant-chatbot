import streamlit as st
import openai
import json


def initialize_session():
    if 'messages' not in st.session_state:
        st.session_state.messages = []


def chat_with_ai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system",
                   "content": "You are a hiring assistant helping candidates with initial screening."}] +
                 st.session_state.messages + [{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']


def main():
    st.title("TalentScout Hiring Assistant")
    st.write("Welcome! I'll assist with your job application process.")

    initialize_session()

    with st.form("user_input_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
        position = st.text_input("Desired Position(s)")
        location = st.text_input("Current Location")
        tech_stack = st.text_area("Tech Stack (e.g., Python, Django, React, AWS)")
        submit = st.form_submit_button("Submit")

    if submit:
        user_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "experience": experience,
            "position": position,
            "location": location,
            "tech_stack": tech_stack
        }
        st.session_state.messages.append({"role": "user", "content": json.dumps(user_data)})

        st.write("Thank you! Generating your technical questions...")

        tech_prompt = f"Generate 3-5 technical interview questions for a candidate proficient in {tech_stack}."
        response = chat_with_ai(tech_prompt)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)

    for msg in st.session_state.messages:
        st.write(f"{msg['role'].capitalize()}: {msg['content']}")


if __name__ == "__main__":
    main()
