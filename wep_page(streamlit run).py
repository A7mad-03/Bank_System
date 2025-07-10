## Recall files ##

import streamlit as st
from sdk_bank import SDKBank
from efawateer import EFAWATEER
from clicker import Click
from currency_converter import convert_from_jod, get_currency_options

                            
import base64 ###لتشفير الصورة ووضعها خلفية 


import os#//////    
#/////////////// --## use it after the user choose exit to close the page ###
import signal#//




###### هون بفحص إذا أول مرة بشغل الصفحة وما في بنك مخزن بالسيشن
if "bank" not in st.session_state:
    ######  بعمل إنشاء للملفات وبستخدم تبع البنك للكليك واي فواتير وبخزنه بالسيشن عشان يضل ثابت 
    st.session_state.bank = SDKBank()
    st.session_state.efawateer = EFAWATEER(st.session_state.bank)
    st.session_state.clicker = Click(st.session_state.bank)


##### هون بس بربط الملفات اللي بالسيشن بمتغيرات  عشان أسهل للاستخدام 
bank = st.session_state.bank
efawateer = st.session_state.efawateer
clicker = st.session_state.clicker




def set_bg_image(local_image_path): #### to background image ####
    with open(local_image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """, unsafe_allow_html=True)
set_bg_image(r"background_image.jpg")


###### ملاحظة #########
### I Using ChatGPT to generate HTML tags within markdown and other function ###


### to style the tilte ###
st.markdown("<h1 style='text-align: center; color: white;'>Welcome to SDK BANK</h1>", unsafe_allow_html=True)

st.markdown("""
    <style>
    input, textarea, select { color: white !important; background-color: #333 !important; }
    label { color: white !important; }
    .stApp { background-color: #1E1E1E; }
    [data-testid="stSidebar"] { background-color: #1f2937; color: white; }
    </style>
""", unsafe_allow_html=True)


# menu
menu = st.sidebar.selectbox("Choose Action", ["Create Account", "Login","Forgot Password", "Exit"])


### Create Account
if menu == "Create Account":
    st.markdown("<h3 style='color: yellow; text-align: center;'>🔐 Create a New Account</h3>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    phone = st.text_input("Phone Number")
    question = st.text_input("Security Question (e.g. Your pet's name?)")
    answer = st.text_input("Answer")

    if st.button("Create"):
        if username and password and phone and question and answer:
            try:
                created = bank.create_account(
                    username.lower(),
                    int(password),
                    int(phone),
                    question.strip(),
                    answer.strip().lower()
                )
                if created:
                    st.success("✅ Account created successfully!")
                else:
                    st.error("❌ Username already exists")

            except ValueError:
                st.error("❌ Enter numbers for phone and password")
        else:
            st.warning("⚠️ Fill all fields")

### Login
elif menu == "Login":
    st.markdown("<h3 style='color: yellow; text-align: center;'>🔑 Login to Your Account</h3>", unsafe_allow_html=True)
    login_method = st.radio("Login using", ["Username", "Phone Number"])

    if login_method == "Username":
        username_input = st.text_input("Username").strip().lower()
        password_input = st.text_input("Password", type="password")

        if st.button("Login"):
            if username_input and password_input:
                try:
                    index = bank.login_by_username(username_input, int(password_input))
                    if index != -1:
                        st.session_state.user_index = index
                        st.success(f"✅ Welcome, {bank.customers[index].capitalize()}!")
                    else:
                        st.error("❌ Invalid credentials")

                except ValueError:
                    st.error("❌ Password must be a number")
            else:
                st.warning("⚠️ Fill in all fields.")

    else:
        phone_input = st.text_input("Phone Number")
        password_input = st.text_input("Password", type="password")
        if st.button("Login"):
            if phone_input and password_input:
                try:
                    index = bank.login_by_phone(int(phone_input), int(password_input))
                    if index != -1:
                        st.session_state.user_index = index
                        st.success(f"  ✅ Welcome, {bank.customers[index].capitalize()}!")
                    else:
                        st.error(" ❌ Invalid credentials.")
                except ValueError:
                    st.error(" ❌  Phone and password must be numbers")
            else:
                st.warning(" ⚠️ Fill in all fields  ")


### Forgot ### 
elif menu == "Forgot Password":
    st.markdown("<h3 style='color: red; text-align: center;'>🔒 Recover Password</h3>", unsafe_allow_html=True)
    username = st.text_input("Enter your username").strip().lower()

    if username:
        if username in bank.to_forget_pass:
            question = bank.to_forget_pass[username]["question"]
            st.markdown(f"<h5 style='color: purple;'>Security Question: {question}</h5>", unsafe_allow_html=True)
            sec_ans = st.text_input("Answer").strip().lower()

            if st.button("Recover"):
                if sec_ans:
                    if bank.to_forget_pass[username]["answer"] == sec_ans:
                        idx = bank.customers.index(username)
                        st.warning(f"Your password is: {bank.passwords[idx]}")
                    else:
                        st.error("Incorrect answer.")
                else:
                    st.warning("Please enter your answer.")
        else:
            st.warning("Username not found.")


### Exit #####
elif menu == "Exit":
    st.balloons()
    st.markdown("<h3 style='color: red; text-align: center;'>🎉 Thank you for using SDK Bank!</h3>", unsafe_allow_html=True)
    os.kill(os.getpid(), signal.SIGTERM)  ##\\\ i used it as if I pressed (ctrl+c) in terminal because turn off the streamlit 



### Logged-in dashboard
if "user_index" in st.session_state:
    index = st.session_state.user_index
    st.sidebar.success(f"Logged in as: {bank.customers[index].capitalize()}")
    st.markdown("<h3 style='color:#87CEEB;'>📋 Your Dashboard</h3>", unsafe_allow_html=True)

    action = st.selectbox("Choose Service", 
        [ "Deposit", "Withdraw", "Check Balance","Click Transfer", "EFAWATEER","Currency Converter","Transaction History","Logout"])

    if action == "Deposit":
        st.markdown("<h5 style='color:#FFA500;'> Deposit </h5>", unsafe_allow_html=True)

        amt = st.number_input("Amount to deposit", min_value=0.0)
        if st.button("Deposit Now"):
            st.success(bank.deposit(index, amt))

    elif action == "Withdraw":
        st.markdown("<h5 style='color:#FFA500;'> Withdraw </h5>", unsafe_allow_html=True)

        amt = st.number_input("Amount to withdraw", min_value=0.0)
        if st.button("Withdraw Now"):
            st.success(bank.withdraw(index, amt))

    elif action == "Check Balance":
        st.markdown("<h5 style='color:#FFA500;'>Check Balance </h5>", unsafe_allow_html=True)

        st.info(f"💰 Your Balance: {bank.balances[index]} JD")
        

    elif action == "Click Transfer":
        st.markdown("<h5 style='color:#FFA500;'> Click Transfer </h5>", unsafe_allow_html=True)

        phone = st.text_input("Recipient's Phone Number")
        amt = st.number_input("Amount to transfer", min_value=0.0)
        if st.button("Transfer"):
            try:
                result = clicker.transfer(index, int(phone), amt)
                if result.startswith("✅"):
                    st.success(result )
                else:
                    st.error(result)
            except ValueError:
                st.error("Invalid phone number.")

    elif action== "EFAWATEER":
        st.markdown("<h5 style='color:#FFA500;'> E_FAWATEER </h5>", unsafe_allow_html=True)

        action_efawateer=st.selectbox("Select sector",["Pay Electricity","Pay Water","Pay Telecom"])


        if action_efawateer == "Pay Electricity":
            st.markdown("<h6 style='color:#A52A2A;'> Pay Electricity </h6>", unsafe_allow_html=True)

            efawateer.electricity(index)

        elif action_efawateer == "Pay Water":
            st.markdown("<h6 style='color: #A52A2A;'> Pay Water </h6>", unsafe_allow_html=True)

            efawateer.water(index)

        elif action_efawateer == "Pay Telecom":
            st.markdown("<h6 style='color:#A52A2A;'> Pay Telecom </h6>", unsafe_allow_html=True)

            efawateer.telecom(index)

    elif action == "Currency Converter":
        st.markdown("<h5 style='color:#FFA500;'> Convert JOD to selected currency </h5>", unsafe_allow_html=True)

        amount_jod = st.number_input("Amount in JOD", min_value=0)
        country = st.selectbox("Select a country", get_currency_options())

        if st.button("Convert"):
            currency_code, converted = convert_from_jod(amount_jod, country)
            if currency_code:
                st.success(f"{amount_jod:.2f} JOD = {converted:.2f} {currency_code}")
            else:
                st.error("Invalid country selection.")


    elif action == "Transaction History":
        st.markdown("<h5 style='color:#FFA500;'>Transaction History</h5>", unsafe_allow_html=True)
        transactions = bank.get_user_transactions(index)
        if transactions:
            for t in reversed(transactions):  # Show most recent first
               st.markdown(f"<span style='color: purple;'>📅 {t['timestamp']} - {t['type'].replace('_', ' ').title()}: {t['amount']} JD</span>", unsafe_allow_html=True)
               if t['details']:
                  st.markdown(f"<span style='color: purple;'>Details: {t['details']}</span>", unsafe_allow_html=True)
               st.markdown("<hr>", unsafe_allow_html=True)

        else:
                      st.info("No transactions yet")

    
###logout#####
    elif action == "Logout":
        
        del st.session_state.user_index
        st.success("Logged out successfully!")
    







    