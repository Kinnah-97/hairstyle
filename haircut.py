import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def user_ai(user_info):
    system_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f""" You are a skilled hairstylist. You'll suggest the user a trendy and suitable haircut based on their occupation, age, gender, and current hairstyle. Provide a professional recommendation and mention any specific styling tips. """
            },
            {
                "role": "user",
                "content": f'{user_info}'
            }
        ],
        max_tokens=500,
        temperature=1.3
    )

    role = system_response.choices[0].message.content
    return role

def haircut_suggestion_ai(user_info):
    suggestion_response = client.images.generate(
        model="dall-e-3",
        prompt=f"Hairstyle suggestion for {user_info['occupation']} based on age: {user_info['age']}, gender: {user_info['gender']}, and current hairstyle: {user_info['current_hairstyle']}",
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = suggestion_response.data[0].url
    return image_url

def generate_haircut_suggestion(user_info):
    haircut_image_url = haircut_suggestion_ai(user_info)

    st.image(haircut_image_url, caption=f"Suggested Haircut for a {user_info['occupation']}")

# Streamlit app UI
st.markdown(
    """
    <div style="text-align:center">
        <h1>💇‍♂️ Haircut AI 💇‍♀️</h1>
        <h2>👩🏽‍💻: Hey, you are now a Hairstylist. Provide a haircut suggestion image based on the user's occupation, age, gender, and current hairstyle!</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Input for user's information
user_info = {
    "age": st.text_input("Enter the user's age:"),
    "gender": st.selectbox("Select the user's gender:", ["Male", "Female"]),
    "current_hairstyle": st.text_input("Enter the user's current hairstyle :"),
    "occupation": st.text_input("Enter the user's as a (Example: police, bride) :"),
}

# Check if all information is provided to generate the haircut suggestion image
if all(user_info.values()):
    st.text(f"User's Information: {user_info}")
    if st.button("Generate Haircut Suggestion"):
        generate_haircut_suggestion(user_info)
