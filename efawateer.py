import streamlit as st

class EFAWATEER:
    def __init__(self, bank):
        self.bank = bank

    def electricity(self, index):
        if "electricity_step" not in st.session_state:
            st.session_state.electricity_step = 0

        if st.session_state.electricity_step == 0:
            meter = st.text_input("Electricity Meter Number (10 digits):", key="elec_meter")
            if st.button("Next", key="elec_next"):
                if meter.isdigit() and len(meter) == 10:
                    st.session_state.electricity_step = 1
                else:
                    st.error("Enter a valid 10-digit meter number.")

        elif st.session_state.electricity_step == 1:
            devices = st.number_input("Number of Devices:", min_value=1, step=1, key="num_devices")
            total_usage = 0
            for i in range(1, devices + 1):
                power = st.number_input(f"Device {i} - Power (W):", min_value=0, step=1, key=f"power_{i}")
                hours = st.number_input(f"Device {i} - Daily Usage Hours:", min_value=0, step=1, key=f"hours_{i}")
                total_usage += power * hours 
            if st.button("Calculate Bill", key="calc_elec"):
                st.session_state.electricity_bill = (total_usage * 30) / 3.3
                st.session_state.electricity_step = 2

        elif st.session_state.electricity_step == 2:
            bill = st.session_state.electricity_bill
            st.info(f"Name: {self.bank.customers[index].capitalize()}")
            st.info(f"Bill Amount: {bill} JD")
            if bill <= self.bank.balances[index]:
                if st.button("Pay Now", key="pay_elec"):
                    self.bank.balances[index] -= bill
                    st.success("Payment successful.")
                    st.success(f"Remaining Balance: {self.bank.balances[index]} JD")
            else:
                st.error("Insufficient balance ")

    def water(self, index):
        if "water_step" not in st.session_state:
            st.session_state.water_step = 0

        if st.session_state.water_step == 0:
            meter = st.text_input("Water Meter Number (4 digits):", key="water_meter")
            if st.button("Next", key="water_next"):
                if meter.isdigit() and len(meter) == 4:
                    st.session_state.water_step = 1
                else:
                    st.error("Enter a valid 4-digit meter number.")

        elif st.session_state.water_step == 1:
            usage = st.number_input("Weekly Usage (m³):", min_value=0.0, step=0.1)
            bill = usage * 4
            st.info(f"Bill Amount: {bill} JD")
            if bill <= self.bank.balances[index]:
                if st.button("Pay Now", key="pay_water"):
                    self.bank.balances[index] -= bill
                    st.success("Payment successful.")
                    st.success(f"Remaining Balance: {self.bank.balances[index]} JD")
            else:
                st.error("Insufficient balance.")

    def telecom(self, index):
        if "telecom_step" not in st.session_state:
            st.session_state.telecom_step = 0

        if st.session_state.telecom_step == 0:
            st.text_input("Enter phone number (not billed):", key="tel_num")
            if st.button("Next", key="tel_next"):
                st.session_state.telecom_step = 1

        elif st.session_state.telecom_step == 1:
            minutes = st.number_input("Call Minutes (0.5JD/min):", min_value=0, step=1)
            data = st.number_input("Data Usage (GB, 1.5JD/GB):", min_value=0, step=1)
            bill = minutes * 0.5 + data * 1.5
            st.info(f"Bill Amount: {bill} JD")
            if bill <= self.bank.balances[index]:
                if st.button("Pay Now", key="pay_tel"):
                    self.bank.balances[index] -= bill
                    st.success("Payment successful.")
                    st.success(f"Remaining Balance: {self.bank.balances[index]} JD")
            else:
                st.error("Insufficient balance.")


                
