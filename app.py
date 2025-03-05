# Run the app using: streamlit run app.py
import streamlit as st
import re
import random
import string

# --- Custom Styling ---
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stApp {
            background: url('https://static.vecteezy.com/system/resources/previews/007/278/150/non_2x/dark-background-abstract-with-light-effect-vector.jpg') no-repeat center center fixed;
            background-size: cover;
            padding: 20px;
        }
        .password-strength {
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            margin-top: 10px;
        }
        .progress-container {
            width: 100%;
            height: 10px;
            background-color: #333;
            border-radius: 5px;
            overflow: hidden;
            margin-top: 5px;
        }
        .progress-bar {
            height: 100%;
            transition: width 0.5s ease-in-out;
        }
        .copy-button {
            background-color: #00bfff;
            color: white;
            border-radius: 5px;
            padding: 5px 10px;
            border: none;
            cursor: pointer;
            display: block;
            margin: 10px auto;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 14px;
            color: #bbb;
        }
    </style>
""", unsafe_allow_html=True)

# --- Common Weak Passwords List ---
COMMON_PASSWORDS = {
    "123456", "password", "123456789", "12345678", "12345", "1234567", "qwerty",
    "abc123", "password1", "111111", "123123", "admin", "letmein", "welcome"
}

# --- Password Strength Function ---
def check_password_strength(password: str):
    score = 0
    errors = []

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        errors.append("Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        errors.append("Include both uppercase and lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        errors.append("Add at least one number (0-9).")

    if re.search(r"[!@#$%^&*()_+{}|:<>?]", password):
        score += 1
    else:
        errors.append("Include at least one special character (!@#$%^&*).")

    if password.lower() not in COMMON_PASSWORDS:
        score += 1
    else:
        errors.append("Avoid using common passwords like 'password123'.")

    if not re.search(r"(.)\1{2,}", password):
        score += 1
    else:
        errors.append("Avoid repeating characters like 'aaa' or '111'.")

    return score, errors

# --- Generate a Strong Password ---
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+{}|:<>?"
    return "".join(random.choice(characters) for _ in range(length))

# --- UI Layout ---
st.title("🔐 Password Strength Meter")
st.write("Enter a password below to check its strength:")

password = st.text_input("Enter Password", type="password")

if password:
    strength, errors = check_password_strength(password)
    color = "red" if strength < 3 else "orange" if strength < 5 else "green"
    width = (strength / 7) * 100

    st.markdown(f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {width}%; background-color: {color};"></div>
        </div>
        <div class="password-strength" style="color: {color};">
            {'❌ Weak' if strength < 3 else '⚠️ Moderate' if strength < 5 else '✅ Strong'}
        </div>
    """, unsafe_allow_html=True)

    if errors:
        st.warning("Suggestions to improve your password:")
        for err in errors:
            st.write(f"- {err}")

# --- Password Generator ---
st.write("---")
st.subheader("🔑 Generate a Strong Password")
password_length = st.slider("Select Password Length", min_value=8, max_value=20, value=12)
if st.button("Generate Password"):
    new_password = generate_password(password_length)
    st.success(f"Generated Password: `{new_password}`")
    
     # Add a button to copy the password to the clipboard    
    st.markdown(f"""
        <div style="display: flex; justify-content: center; margin-top: 10px;">
            <button class="copy-button" onclick="navigator.clipboard.writeText('{new_password}')">Copy Password</button>
        </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
    <div class="footer">
        Created by 💖 Zahoor Fatima
    </div>
""", unsafe_allow_html=True)