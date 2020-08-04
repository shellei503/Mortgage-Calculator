import pandas as pd
import os

# principal_amount = float(input ("Enter the principal amount of loan: "))
# annual_rate = float(input("Enter the annual interest rate as a decimal: "))
# num_years = float(input("Enter the number of years of the loan: "))
# extra_monthly = float(input("Enter the amount of extra monthly payment: "))

# inputs
# house_price = 340000
# downpayment_percent = .20
# annual_rate = .04
# 1221 (3.5%)
# 1299 (4%)

# house_price = 554000
# downpayment_percent = .10
# annual_rate = .06
# 1122 (4%)

#*****************************
# 4409 W MONTE Way
file_name = '4409 W MONTE Way'
house_price = 350000
downpayment_percent = .20
annual_rate = .0365
num_years = 30
extra_monthly = 0
# lender fees = $800
downpaymet = house_price*downpayment_percent

#*****************************
# Better rates
# file_name = '145k, 4.000pct, 30 yr, 1988 upfront'
# house_price = 145000
# downpayment_percent = .20
# annual_rate = .04
# num_years = 30
# extra_monthly = 0

# file_name = '145k, 15 yr, 3.625 pct, 72 upfront'
# house_price = 145000
# downpayment_percent = .20
# annual_rate = .03625
# num_years = 15
# extra_monthly = 0

# file_name = '145k, 4.000pct, 30 yr, 1988 upfront, 282 extra,
# house_price = 145000
# downpayment_percent = .20
# annual_rate = .04
# num_years = 30
# extra_monthly = 282


#*****************************
# Costco rates
# file_name = '145k, 30 yrs, 4.250pct, 800 upfront'
# house_price = 145000
# downpayment_percent = .20
# annual_rate = .04250
# num_years = 30
# extra_monthly = 0
# # lender fees = $800

# file_name = '145k, 30 yrs, 4.250pct, 108750 upfront, investment'
# house_price = 145000
# downpayment_percent = .25
# annual_rate = .04125
# num_years = 30
# extra_monthly = 0
# # lender fees = $800


# file_name = '145k, 30 yrs, 4.250pct, 2942 upfront, investment'
# house_price = 145000
# downpayment_percent = .20
# annual_rate = .0425
# num_years = 30
# extra_monthly = 0
# # lender fees = $800
# downpaymet = house_price*downpayment_percent
# principal_amount = 306000
principal_amount = house_price - downpaymet

#1112

# conversions to monthly values
n = num_years * 12  # number of payment periods
r = annual_rate / 12  # monthly interest rate

# initialization
remaining_balance = principal_amount
temp_r = ((1 + r) ** n)
monthly_payment = principal_amount / ((temp_r - 1) / (r * temp_r))
month = 1

# list for dataframe
month_lst = []
starting_balance_lst = []
monthly_payment_lst = []
monthly_payment_lst2 = []
amount_paid = []
principal_paid_lst = []
extra_payment_lst =[]
total_towards_principal_lst = []
interest_paid_lst = []
remaining_balance_lst = []
total_interest_lst = []
tracker_lst = []

# for i in range(n):
while remaining_balance > 0:
    # month number
    month_lst.append(month)
    month = month + 1

    # starting balance
    starting_balance_lst.append(remaining_balance)

    # amount paid
    if remaining_balance < monthly_payment + extra_monthly:
        monthly_payment_lst.append(remaining_balance)
        tracker_lst.append(1)
    else:
        total_monthly_payment = monthly_payment + extra_monthly
        monthly_payment_lst.append(total_monthly_payment)
        tracker_lst.append(0)

    # amount paid (in interest)
    monthly_interest_amount = (remaining_balance * r)
    interest_paid_lst.append(round(monthly_interest_amount,2))

    # amount paid (towards principal)
    monthly_principal_paid = monthly_payment - monthly_interest_amount
    principal_paid_lst.append(round(monthly_principal_paid,2))

    # extra amount paid
    extra_payment_lst.append(extra_monthly)

    # total towards principal
    total_towards_principal = extra_monthly + monthly_principal_paid
    total_towards_principal_lst.append(total_towards_principal_lst)


    # ending balance
    remaining_balance = remaining_balance - total_towards_principal
    remaining_balance_lst.append(round(remaining_balance,2))

    # total interest
    total_interest = round(sum(interest_paid_lst), 2)
    total_interest_lst.append(total_interest)

amortization_df = pd.DataFrame(
    {
        # 'month': month_lst,
     # 'starting balance': starting_balance_lst,
     # 'monthly payment': monthly_payment,
    # 'extra payment': extra_monthly,
    #     'total payment': total_monthly_payment,
     'interest paid': interest_paid_lst,
     'principal paid': principal_paid_lst,
    'extra payment': extra_payment_lst,
     'ending balance': remaining_balance_lst
        # 'tracker lst': tracker_lst
     # 'total interest paid': total_interest_lst
     })

print(amortization_df)

print('------------------------------------------------------')
print('home price:', house_price)
print('downpayment amount:', downpaymet)
print('downpayment percentage: ', downpayment_percent)
print('principal amount:', round(principal_amount, 2))
print('monthly payment amount:',round(monthly_payment),2)
print('extra monhtly payment amount:',extra_monthly )
print('original term length:', n)
num_payments = len(month_lst)
print('years to pay off: ', round(len(month_lst)/12,2))
print('years paid off early: ', round((n- len(month_lst))/12,2))
print('percentage of original loan term: ', round(num_payments/n,2))
print('')
print()

print('------------------------------------------------------')
print('total interest paid:',total_interest_lst[-1])
# print(sum(tracker_lst))

base_dir = os.getcwd()
def export_soln_to_csv(df, model_name = 'untitled'):
    """ model refers to model object from docplex.mp.model"""

    try:
        os.mkdir(os.path.join(base_dir, 'output'))
    except:
        pass

    filename = 'output/' + 'soln_' + model_name + '.csv'
    solution_output = os.path.join(os.getcwd(), filename)
    df.to_csv(solution_output, index=False)

def export_soln_to_excel(df, model_name = 'untitled'):
    """ model refers to model object from docplex.mp.model"""

    try:
        os.mkdir(os.path.join(base_dir, 'output'))
    except:
        pass

    filename = 'output/' + model_name + '.xlsx'
    solution_output = os.path.join(os.getcwd(), filename)
    df.to_excel(solution_output, index=False)

export_soln_to_excel(amortization_df, file_name)