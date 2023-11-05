#!/usr/bin/env python
# coding: utf-8
# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

homeBuyer = pd.read_csv("HackUTD-2023-HomeBuyerInfo.csv")

homeBuyer.head()

homeBuyer.columns

def calc_LTV(appraisal, downPayment):
    loan_amount = appraisal - downPayment
    LTV = (loan_amount / appraisal) * 100
    return LTV

def calc_DTI(grossIncome, creditCardPMT, carPMT, studentPMT, mortgagePMT):
    totalPMT = creditCardPMT + carPMT + studentPMT + mortgagePMT
    DTI = (totalPMT / grossIncome) * 100
    return DTI


def calc_FEDTI(grossIncome, mortgagePMT):
    FEDTI = (mortgagePMT / grossIncome) * 100
    return FEDTI


def valid_credit_score(creditScore):
    return creditScore >= 640

def calc_PMI(LTV, appraisal):
    if 80 <= LTV < 95:
        PMI = appraisal * 0.01 / 12  # 1% of home value per year, divided by 12 months
    else:
        PMI = 0
    return PMI


def valid_LTV(LTV):
    return LTV < 95


def valid_DTI(DTI, FEDTI):
    if DTI < 44:
        if FEDTI < 29:
            return True
    return False


def can_buy_house(grossIncome, creditCardPMT, carPMT, studentPMT, appraisal, downPMT, loanAmt, mortgagePMT,
                  creditScore):
    LTV = calc_LTV(appraisal, downPMT)
    DTI = calc_DTI(grossIncome, creditCardPMT, carPMT, studentPMT, mortgagePMT)
    FEDTI = calc_FEDTI(grossIncome, mortgagePMT)
    PMI = calc_PMI(LTV, appraisal)

    is_LTV = valid_LTV(LTV)
    is_DTI = valid_DTI(DTI, FEDTI)
    is_credit = valid_credit_score(creditScore)

    approval_status = "Y"
    reasons = []

    if not is_credit:
        approval_status = "N"
        reasons.append("Credit Score")
    if not is_LTV:
        approval_status = "N"
        reasons.append("LTV")
    if not is_DTI:
        approval_status = "N"
        reasons.extend(["DTI" if DTI > 43 else None, "FEDTI" if FEDTI > 28 else None])

    return approval_status, reasons


# In[96]:


approval_data = []

# Loop through the DataFrame
for index, row in homeBuyer.iterrows():
    # Get the row data
    grossIncome = row['GrossMonthlyIncome']
    creditPMT = row['CreditCardPayment']
    carPMT = row['CarPayment']
    studentPMT = row['StudentLoanPayments']
    appraisal = row['AppraisedValue']
    downPMT = row['DownPayment']
    loanAmt = row['LoanAmount']
    mortgagePMT = row['MonthlyMortgagePayment']
    creditScore = row['CreditScore']

    # Apply the function
    status, reasons = can_buy_house(grossIncome, creditPMT, carPMT, studentPMT, appraisal, downPMT, loanAmt,
                                    mortgagePMT, creditScore)

    # Store the results
    approval_data.append({
        'ApprovalStatus': status,
        'Reasons': reasons
    })

# Convert the list to a DataFrame
approval_df = pd.DataFrame(approval_data)
def show_graphs():
    approval_count = approval_df['ApprovalStatus'].value_counts()
    non_approval_reasons = approval_df[approval_df['ApprovalStatus'] == 'N']['Reasons'].explode().value_counts(
        normalize=True) * 100

    # Create a summary DataFrame for plotting
    summary_df = non_approval_reasons.reset_index().rename(columns={'index': 'Reason', 'Reasons': 'Percentage'})
    summary_df = summary_df.rename(columns={'Percentage': 'Reason', 'proportion': 'Percentage'})

    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,6))  # 1 row, 2 columns, 1st subplot = count plot
    sns.countplot(x='ApprovalStatus', data=approval_df, palette='dark', ax=ax1)
    ax1.set_title('Distribution of Eligible and Ineligible Home Buyers', fontsize=18, weight='bold')
    ax1.set_xlabel('Approval Status', fontsize=15, weight='bold')
    ax1.set_ylabel('Count', fontsize=15, weight='bold')
    ax1.set_xticklabels(['Ineligible', 'Eligible'])

    # Annotating the count plot
    for p in plt.gca().patches:
        plt.gca().annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()-1),
                    ha='center', va='center', fontsize=13, color='black', weight='bold', xytext=(0, 10),
                    textcoords='offset points')

    # Second graph: Percentage of Non-Approvals by Reason

    sns.barplot(data=summary_df, x='Reason', y='Percentage', palette='pastel', ax=ax2)
    ax2.set_title('Percentage of Non-Approvals by Reason', fontsize=18, weight='bold')
    ax2.set_xlabel('Reason for Non-Approval', fontsize=15, weight='bold')
    ax2.set_ylabel('Percentage', fontsize=15, weight='bold')
    ax2.tick_params(axis='x', rotation=45)

    # Annotating the reasons bar plot
    for p in plt.gca().patches:
        plt.gca().annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()-0.5),
                    ha='center', va='center', fontsize=13, color='black', weight='bold', xytext=(0, 10),
                    textcoords='offset points')

    plt.tight_layout()

    graph_window = tk.Toplevel()
    graph_window.title("Graphs")
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

import tkinter as tk
from tkinter import ttk

class HomeBuyerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Home Buyer Eligibility Calculator")
        self.geometry("500x350")
        # Input fields and sliders
        self.create_widgets()

    def create_widgets(self):
        self.inputs = {}

        # Define a list of (label, min, max) tuples for the sliders
        attributes = [
            ("Gross Monthly Income", 1000, 30000),
            ("Credit Card Payment", 0, 5000),
            ("Car Payment", 0, 2000),
            ("Student Loan Payment", 0, 2000),
            ("Appraised Value of Property", 50000, 1000000),
            ("Down Payment", 0, 200000),
            ("Loan Amount", 10000, 500000),
            ("Mortgage Payment", 0, 10000),
            ("Credit Score", 300, 850)
        ]

        # Create sliders for each attribute
        self.value_labels = {}
        for i, (label, min_val, max_val) in enumerate(attributes):
            ttk.Label(self, text=f"{label}:").grid(column=0, row=i, sticky='w')
            slider = ttk.Scale(self, from_=min_val, to=max_val, orient='horizontal')
            slider.set((min_val + max_val) / 2)  # Default value is the midpoint
            slider.grid(column=1, row=i, sticky='ew')
            self.inputs[label] = slider
            value_label = ttk.Label(self, text=f"{(min_val + max_val) / 2:.2f}")
            value_label.grid(column=2, row=i, sticky='w')
            self.value_labels[label] = value_label
            slider['command'] = lambda value, lbl=label: self.update_slider_label(lbl)

        # Button to calculate eligibility
        self.check_button = ttk.Button(self, text="Check Eligibility", command=self.check_eligibility)
        self.check_button.grid(column=0, row=len(attributes), columnspan=2)

        # Label to display result
        self.result_label = ttk.Label(self, text="Eligibility result will be shown here.")
        self.result_label.grid(column=0, row=len(attributes) + 1, columnspan=2, sticky='ew')

        self.graph_button = ttk.Button(self, text="Show Graphs", command=show_graphs)
        self.graph_button.grid(column=0, row=len(self.inputs) + 2, columnspan=2, pady=10)
    def update_slider_label(self, label):
        value = self.inputs[label].get()
        self.value_labels[label].config(text=f"{value:.2f}")

    def check_eligibility(self):
        # Retrieve values from sliders
        gross_income = self.inputs["Gross Monthly Income"].get()
        credit_card_payment = self.inputs["Credit Card Payment"].get()
        car_payment = self.inputs["Car Payment"].get()
        student_loan_payment = self.inputs["Student Loan Payment"].get()
        appraisal = self.inputs["Appraised Value of Property"].get()
        down_payment = self.inputs["Down Payment"].get()
        loan_amount = self.inputs["Loan Amount"].get()
        mortgage_payment = self.inputs["Mortgage Payment"].get()
        credit_score = self.inputs["Credit Score"].get()


        approval_status, reasons = can_buy_house(
            gross_income,
            credit_card_payment,
            car_payment,
            student_loan_payment,
            appraisal,
            down_payment,
            loan_amount,
            mortgage_payment,
            credit_score
        )

        if approval_status == 'Y' and not reasons:
            result_message = "Eligible for a house loan."
        else:
            # Join the reasons list into a string
            reasons_str = ", ".join(filter(None, reasons))  # This filters out any None values before joining
            result_message = f"Ineligible for a house loan due to: {reasons_str}"

            # Display the result
        self.result_label.config(text=result_message)


# Main function to run the application
def main():
    app = HomeBuyerApp()
    app.mainloop()


if __name__ == "__main__":
    main()

# In[ ]:




