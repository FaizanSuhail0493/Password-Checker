import streamlit as st
import re
import random
import string

# Initialize session state
if 'saved_passwords' not in st.session_state:
    st.session_state.saved_passwords = set()
if 'show_generate_section' not in st.session_state:
    st.session_state.show_generate_section = False

# Function to check password strength
def check_password_strength(password):
    if len(password) < 8:
        return "Weak", "❌ Password must be at least 8 characters long."
    has_upper = re.search(r'[A-Z]', password)
    has_lower = re.search(r'[a-z]', password)
    has_digit = re.search(r'\d', password)
    has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    
    if has_upper and has_lower and not (has_digit and has_special):
        return "Moderate", "⚠️ Consider adding digits and special characters."
    if has_upper and has_lower and has_digit and has_special:
        return "Strong", "✅ This is a strong password!"
    return "Weak", "❌ Password must contain uppercase, lowercase, numbers, and symbols."

# Function to generate a secure password
def generate_password(length):
    if length < 8:
        return "Password length must be at least 8 characters."
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Function to save password
def save_password(password):
    if password in st.session_state.saved_passwords:
        return "❌ This password has already been used! Choose a new one."
    if len(st.session_state.saved_passwords) >= 10:
        st.session_state.saved_passwords.pop()
    st.session_state.saved_passwords.add(password)
    return "✅ Password saved successfully!"

# Tailwind CSS Styling
st.markdown("""
    <style>
        body {
            background: #3f3f3f;
            font-family: 'Inter', sans-serif;
            color: white;
        }
        .stApp {
            background: linear-gradient(135deg, #bcbcbc, #cfe2f3);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
        }
        .password-input {
            width: 100%;
            padding: 12px;
            border: 3px solid #38bdf8;
            border-radius: 8px;
            font-size: 16px;
        }
        .stButton>button {
            background: linear-gradient(45deg, brown, #351c75);
            color: white;
            font-size: 18px;
            padding: 10px, 20px;
            transition: 0.3s;
            box-shadow: 0px 5px 15px rgba(0, 201, 255, 0.4);
        }
        .stButton>button:hover {
            transform: scale(1.05);
            background: linear-gradient(45deg, grey, #00c9ff);
            color: black;
        }
        .alert {
            padding: 10px;
            margin-top: 10px;
            border-radius: 5px;
            font-weight: bold;
            text-align: center;
        }
        .weak { background: #dc2626; color: white; }
        .moderate { background: #d97706; color: white; }
        .strong { background: #047857; color: white; }
        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: black;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="password-container">', unsafe_allow_html=True)
st.title("🔐 Password Strength Checker & Generator")
st.markdown("### Ensure your passwords are strong and unique!")

# Password Input
password = st.text_input("Enter your password", type="password", key="password_input")

# Buttons in a Row
st.markdown('<div class="btn-container">', unsafe_allow_html=True)
if st.button("Check Password Strength", key="check"):
    rating, message = check_password_strength(password)
    color_class = rating.lower()
    if not password:
        st.markdown('<div class="alert weak">❌ Please enter a password.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert {color_class}">{message}</div>', unsafe_allow_html=True)

if st.button("Save Password", key="save"):
    if not password:
        st.markdown('<div class="alert weak">❌ Enter a password first.</div>', unsafe_allow_html=True)
    else:
        message = save_password(password)
        color_class = "weak" if "already been used" in message else "strong"
        st.markdown(f'<div class="alert {color_class}">{message}</div>', unsafe_allow_html=True)

if st.button("Generate Password", key="generate"):
    st.session_state.show_generate_section = not st.session_state.show_generate_section
st.markdown('</div>', unsafe_allow_html=True)

# Show Password Generator Section
if st.session_state.show_generate_section:
    st.markdown("### Generate a Secure Password")
    password_length = st.number_input("Select password length", min_value=8, max_value=32, value=12)
    if st.button("Generate Now"):
        new_password = generate_password(password_length)
        st.text_input("Generated Password", new_password, type="default")

# Password Strength Suggestions
st.markdown("### Tips for a Strong Password")
st.markdown("✅ Use at least 12-16 characters.")
st.markdown("✅ Include uppercase and lowercase letters.")
st.markdown("✅ Add numbers and special characters.")
st.markdown("✅ Avoid using personal information.")
st.markdown("✅ Do not reuse old passwords.")

st.markdown('</div>', unsafe_allow_html=True)

# Display Stored Passwords Count
st.markdown(f"**Stored Passwords Count:** {len(st.session_state.saved_passwords)}/10")

#Footer
st.markdown("<div class='footer'>Created with ❤ by Faizan Suhail</div>", unsafe_allow_html=True)
