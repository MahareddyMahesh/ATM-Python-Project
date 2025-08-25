# Project Name: Piggy ATM Machine
# pip install streamlit
# pip show streamlit  
# streamlit run atm.py


import streamlit as st


# creating some initial accounts
# if "accounts" is not already in session state, create default accounts
if "accounts" not in st.session_state:
    st.session_state.accounts = {
        "491" : {"pin": "1234", "balance" : 5000, "transactions" : []},
        "984" : {"pin" : "1912", "balance" : 1000, "transactions" : []}
    }


# opening the login page
if "page" not in st.session_state:
    st.session_state.page = "login"


# initializing the account number to None
if "acc_no" not in st.session_state:
    st.session_state.acc_no = None


# Changing the page
def go_to(page):
    st.session_state.page = page
    st.rerun()


if st.session_state.page == "login":
    st.title("💰 Piggy ATM MAchine")
    st.subheader("🔐 Login to your Account")


    acc_no = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN Number", type = "password")


    if st.button("login"):
        if acc_no in st.session_state.accounts and st.session_state.accounts[acc_no]["pin"] == pin:
            st.session_state.acc_no = acc_no  # saving our active account number
            go_to("menu")  # helping to change the page from login to menu
        else:
            st.error(" Dear THEAF garu: Please Enter right account or Pin number")


    if st.button("Sign up"):
        go_to("signup")


elif st.session_state.page == "signup":
    st.title("Create New Account")
    new_acc_no = st.text_input("Enter new account number")
    new_pin = st.text_input("Set PIN", type = "password")
    initial_deposit = st.number_input("Enter opening amount", min_value = 0, step = 10)


    if st.button("Create account"):
        if new_acc_no in st.session_state.accounts:
            st.error("Account number already exists")
        elif new_acc_no == "" or new_pin == "":
            st.error("Mandatory to fill account number and pin")
        else:
            st.session_state.accounts[new_acc_no] = {
                "pin" : new_pin,
                "balance" : initial_deposit,
                "transactions" : [f"Initial deposit: {initial_deposit}"] if initial_deposit > 0 else []
            }
            st.success(f" Account {new_acc_no} created successfully")
            st.session_state.acc_no = new_acc_no
            go_to("menu")
   
    if st.button("Back to Login"):
        go_to("login")


elif st.session_state.page == "menu":
    st.title("☰ MAIN MENU")
    st.write(f"Welcome to Account no: {st.session_state.acc_no}")


    if st.button("💰 Check Balance"):
        go_to("balance")
    if st.button("💰 Deposit Money"):
        go_to("deposit")
    if st.button("💰 Withdraw Money"):
        go_to("withdraw")
    if st.button("🗃 Mini Statement"):
        go_to("statement")
    if st.button("💸 Money Transfer"):
        go_to("Transfer")
    if st.button("🚀 EXIT"):
        go_to("login")
   
elif st.session_state.page == "balance":
    st.title("Total Balance available")
    bal = st.session_state.accounts[st.session_state.acc_no]["balance"]
    st.info(f"Your current Balance is: {bal}")
    if st.button("Back to Menu"):
        go_to("menu")
elif st.session_state.page == "deposit":
    st.title("Deposit Money")
    amount = st.number_input("Enter amount to deposit", min_value = 1, step = 1)
    if st.button("Deposit"):
        st.session_state.accounts[st.session_state.acc_no]["balance"] += amount
        st.session_state.accounts[st.session_state.acc_no]["transactions"].append(f"Deposited: {amount}")
        st.success(f"Successfully deposited {amount}")
    if st.button("Back to Menu"):
        go_to("menu")
elif st.session_state.page == "withdraw":
    st.title("Withdraw Money")
    amount = st.number_input("Enter amount to withdraw", min_value=1, step=1)
    if st.button("Withdraw"):
        bal = st.session_state.accounts[st.session_state.acc_no]["balance"]
        if amount > bal:
            st.error("Insufficient balance")
        else:
            st.session_state.accounts[st.session_state.acc_no]["balance"] -= amount
            st.session_state.accounts[st.session_state.acc_no]["transactions"].append(f"Withdrew: {amount}")
            st.success(f"Successfully withdrew {amount}")
    if st.button("Back to Menu"):
        go_to("menu")
elif st.session_state.page == "Transfer":
    st.title("Money Transfer")
    target_acc_no = st.text_input("Enter recipient account number")
    amount = st.number_input("Enter amount to transfer", min_value=1, step=1)
    sender_acc = st.session_state.acc_no
    sender_bal = None
    if sender_acc is not None and sender_acc in st.session_state.accounts:
        sender_bal = st.session_state.accounts[sender_acc]["balance"]
    if st.button("Transfer"):
        if sender_acc is None or sender_acc not in st.session_state.accounts:
            st.error("No sender account selected. Please login again.")
        elif target_acc_no == "":
            st.error("Please enter recipient account number")
        elif target_acc_no not in st.session_state.accounts:
            st.error("Recipient account does not exist")
        elif target_acc_no == sender_acc:
            st.error("Cannot transfer to your own account")
        elif amount > sender_bal:
            st.error("Insufficient balance")
        else:
            st.session_state.accounts[sender_acc]["balance"] -= amount
            st.session_state.accounts[target_acc_no]["balance"] += amount
            st.session_state.accounts[sender_acc]["transactions"].append(f"Transferred {amount} to {target_acc_no}")
            st.session_state.accounts[target_acc_no]["transactions"].append(f"Received {amount} from {sender_acc}")
            st.success(f"Successfully transferred {amount} to account {target_acc_no}")
    if st.button("Back to Menu"):
        go_to("menu")

elif st.session_state.page == "statement":
    st.title("Mini Statement")
    transactions = st.session_state.accounts[st.session_state.acc_no]["transactions"]
    if transactions:
        for t in transactions[-10:]:
            st.write(t)
    else:
        st.info("No transactions yet.")
    if st.button("Back to Menu"):
        go_to("menu")