import pandas as pd


def get_fed_taxes(taxable_income, file_single=True):
    if file_single:
        taxable_income = max(taxable_income - 12550, 0)
        if taxable_income <= 10275:
            return .10 * taxable_income
        elif taxable_income <= 41775:
            return 1275 + .12 * (taxable_income - 10275)
        elif taxable_income <= 89075:
            return 4807.5 + .22 * (taxable_income - 41775)
        elif taxable_income <= 170050:
            return 15213.5 + .24 * (taxable_income - 89075)
        elif taxable_income <= 215950:
            return 34647.5 + .32 * (taxable_income - 170050)
        elif taxable_income <= 539900:
            return 49335.5 + .35 * (taxable_income - 215950)
        else:
            return 162718.5 + .37 * (taxable_income - 539900)
    else:
        taxable_income = max(0, taxable_income - 25100)
        if taxable_income <= 20550:
            return .10 * taxable_income
        elif taxable_income <= 83550:
            return 2055 + .12 * (taxable_income - 20550)
        elif taxable_income <= 178150:
            return 9615 + .22 * (taxable_income - 83550)
        elif taxable_income <= 340100:
            return 30427 + .24 * (taxable_income - 178150)
        elif taxable_income <= 431900:
            return 69295 + .32 * (taxable_income - 340100)
        elif taxable_income <= 647850:
            return 98671 + .35 * (taxable_income - 431900)
        else:
            return 174253.5 + .37 * (taxable_income - 647850)


def get_az_state_taxes(taxable_income, file_single=True):
    if file_single:
        taxable_income = max(taxable_income - 12550, 0)
        if taxable_income <= 27808:
            return .0259 * taxable_income
        elif taxable_income <= 55615:
            return 720 + .0334 * (taxable_income - 27808)
        elif taxable_income <= 166843:
            return 1649 + .0417 * (taxable_income - 55615)
        elif taxable_income <= 250000:
            return 6287 + .045 * (taxable_income - 166843)
        else:
            return 10029 + .01 * (taxable_income - 250000) + .035 * (taxable_income - 250000)
    else:
        taxable_income = max(taxable_income - 25100, 0)
        if taxable_income <= 55615:
            return .0259 * taxable_income
        elif taxable_income <= 111229:
            return 1440 + .0334 * (taxable_income - 55615)
        elif taxable_income <= 333684:
            return 3298 + .0417 * (taxable_income - 111229)
        elif taxable_income <= 500000:
            return 12574 + .045 * (taxable_income - 333684)
        else:
            return 20059 + .01 * (taxable_income - 500000) + .035 * (taxable_income - 500000)


def get_medicare_tax(fica_taxable_income, file_single=True):
    if file_single:
        if fica_taxable_income < 200000:
            return .0145 * fica_taxable_income
        else:
            return 3062 + .009 * (fica_taxable_income - 200000)
    else:
        if fica_taxable_income < 250000:
            return .0145 * fica_taxable_income
        else:
            return .0145 * 250000 + .009 * (fica_taxable_income - 250000)


def get_social_security_tax(fica_taxable_income):
    if fica_taxable_income < 147000:
        social_security_owed = 0.0625 * fica_taxable_income
    else:
        social_security_owed = 0.0625 * 147000
    return social_security_owed


def get_taxable_income(gross, pre_tax_retirement, pre_tax_hsa, pre_tax_medical, pre_tax_dental, pre_tax_vision):
    fed_taxable_income = gross - pre_tax_retirement - pre_tax_hsa - pre_tax_medical - pre_tax_dental - pre_tax_vision
    fica_taxable_income = gross - pre_tax_hsa - pre_tax_medical - pre_tax_dental - pre_tax_vision
    return fed_taxable_income, fica_taxable_income


def get_amortization_df(file_name, purchase_price, down_payment_percent):
    n = num_years * 12  # number of payment periods
    r = annual_rate / 12  # monthly interest rate
    down_payment = purchase_price * down_payment_percent
    principal_amount = purchase_price - down_payment

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
    extra_payment_lst = []
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
        interest_paid_lst.append(round(monthly_interest_amount, 2))

        # amount paid (towards principal)
        monthly_principal_paid = monthly_payment - monthly_interest_amount
        principal_paid_lst.append(round(monthly_principal_paid, 2))

        # extra amount paid
        extra_payment_lst.append(extra_monthly)

        # total towards principal
        total_towards_principal = extra_monthly + monthly_principal_paid
        total_towards_principal_lst.append(total_towards_principal_lst)

        # ending balance
        remaining_balance = remaining_balance - total_towards_principal
        remaining_balance_lst.append(round(remaining_balance, 2))

        # total interest
        total_interest = round(sum(interest_paid_lst), 2)
        total_interest_lst.append(total_interest)

    amortization_df = pd.DataFrame(
        {
            'month': month_lst,
            'starting balance': starting_balance_lst,
            'monthly payment': monthly_payment,
            'extra payment': extra_monthly,
            'total payment': total_monthly_payment,
            'interest paid': interest_paid_lst,
            'principal paid': principal_paid_lst,
            'extra payment': extra_payment_lst,
            'ending balance': remaining_balance_lst
            # 'tracker lst': tracker_lst
            # 'total interest paid': total_interest_lst
        })

    amortization_df.to_csv(f'{file_name}_amortization.csv', index=False)

    print("**********************************************************************************************")
    print(f"Amortization for file_name = {file_name_lst[i]}")
    print("**********************************************************************************************")
    print()
    print(f'home price = ${int(purchase_price)}')
    print(f'down_payment amount = ${int(down_payment)}')
    print(f'down_payment percentage = {int(down_payment_percent * 100)}%')
    print(f'principal amount =  ${int(principal_amount)}')
    print(f'monthly payment amount = {int(monthly_payment)}')
    print(f'extra monthly payment amount = ${int(extra_monthly)}')
    print(f'original term length (months) = {n}')
    num_payments = len(month_lst)
    print('years to pay off = ', round(len(month_lst) / 12, 2))
    print('years paid off early = ', round((n - len(month_lst)) / 12, 2))
    print('percentage of original loan term = ', round(num_payments / n, 2))
    print('')
    print(f'total interest paid = ${int(total_interest_lst[-1])}')
    print()
    return amortization_df


# inventment property info
file_name_lst = ['triplex']
purchase_price_lst = [1000000]
rental_income_lst = [6000 * 12]
insurance_lst = [5000]
property_tax_lst = [2000]
maintenance_lst = [2000]
landscaping_lst = [3000]
management_fee_lst = [2500]

# depreciation info
acc_dep_pct = .25

# loan info
down_payment_percent = .25
annual_rate = .04125
num_years = 30
extra_monthly = 0
lender_fees = 0

# w2 info
w2_income1 = 300000
w2_income2 = 300000
w2_pre_tax_401k1 = 21500
w2_pre_tax_401k2 = 21500
total_pre_tax_health1 = 4000
total_pre_tax_health2 = 4000
w2_income = w2_income1 + w2_income2
w2_pre_tax_401k = w2_pre_tax_401k1 + w2_pre_tax_401k2
w2_pre_tax_health = total_pre_tax_health1 + total_pre_tax_health2

for i in range(len(file_name_lst)):
    purchase_price = purchase_price_lst[i]
    file_name = file_name_lst[i]
    rental_income = rental_income_lst[i]

    # get first year interest
    amortization_df = get_amortization_df(file_name, purchase_price, down_payment_percent)
    mask = amortization_df['month'] <= 12
    df = amortization_df[mask]
    year1_interest = df['interest paid'].sum()

    # get acceleration depreciation
    acc_dep = acc_dep_pct * purchase_price

    # get total expense
    total_expenses = year1_interest + insurance_lst[i] + maintenance_lst[i] + landscaping_lst[i] + management_fee_lst[i]

    # fed taxes
    fed_income_no_rental = w2_income - w2_pre_tax_401k - w2_pre_tax_health
    fed_income = fed_income_no_rental - total_expenses + rental_income
    fed_income_acc = max(fed_income - acc_dep, 0)
    fed_taxes_no_rental = get_fed_taxes(fed_income_no_rental, False)
    fed_taxes = get_fed_taxes(fed_income, False)
    fed_taxes_acc = get_fed_taxes(fed_income_acc, False)

    # state taxes
    state_taxes_no_rental = get_az_state_taxes(fed_income_no_rental, False)
    state_taxes = get_az_state_taxes(fed_income, False)
    state_taxes_acc = get_az_state_taxes(fed_income_acc, False)

    # medicare taxes
    fica_income1 = w2_income1 - total_pre_tax_health1
    fica_income2 = w2_income2 - total_pre_tax_health2
    fica_income = fica_income1 + fica_income2
    medicare_taxes = get_medicare_tax(fica_income, False)

    # ss taxes
    ss_taxes1 = get_social_security_tax(fica_income1)
    ss_taxes2 = get_social_security_tax(fica_income2)
    ss_taxes = ss_taxes1 + ss_taxes2

    # total taxes
    total_taxes_no_rental = fed_taxes_no_rental + state_taxes_no_rental + medicare_taxes + ss_taxes
    total_taxes = fed_taxes + state_taxes + medicare_taxes + ss_taxes
    total_taxes_acc = fed_taxes_acc + state_taxes_acc + medicare_taxes + state_taxes

    # summary
    delta = total_taxes_no_rental - total_taxes
    delta_acc = total_taxes_no_rental - total_taxes_acc
    effective_tax_rate_no_rental = total_taxes_no_rental / w2_income
    effective_tax_rate = total_taxes / (w2_income + rental_income)
    effective_tax_rate_acc = total_taxes_acc / (w2_income + rental_income)

    print("**********************************************************************************************")
    print(f"Taxes for file_name = {file_name_lst[i]}")
    print("**********************************************************************************************")
    print()
    print(f"Taxable federal income without rental = ${int(fed_income_no_rental)}")
    print(f"Taxable federal income with rental = ${int(fed_income)}")
    print(f"Taxable federal income with rental and accelerated deprecation = ${int(fed_income_acc)}")
    print('----------------------------------------------------------------------')
    print(f"Effective tax rate without without rental = {int(effective_tax_rate_no_rental * 100)}%")
    print(f"Effective tax rate with rental = {int(effective_tax_rate * 100)}%")
    print(f"Effective tax rate with rental and accelerated deprecation = {int(effective_tax_rate_acc * 100)}%")
    print('----------------------------------------------------------------------')
    print(f"Fed taxes without rental = ${int(fed_taxes_no_rental)}")
    print(f"Fed taxes with rental = ${int(fed_taxes)}")
    print(f"Fed taxes with rental and accelerated deprecation = ${int(fed_taxes_acc)}")
    print('----------------------------------------------------------------------')
    print(f"State taxes without rental = ${int(state_taxes_no_rental)}")
    print(f"State taxes with rental = ${int(state_taxes)}")
    print(f"State taxes with rental and accelerated deprecation = ${int(state_taxes_acc)}")
    print('----------------------------------------------------------------------')
    print(f"Total taxes without rental = ${int(total_taxes_no_rental)}")
    print(f"Total taxes with rental = ${int(total_taxes)}")
    print(f"Total taxes with rental and accelerated deprecation = ${int(total_taxes_acc)}")
    print('----------------------------------------------------------------------')
    print(f"Total saved with rental = ${max(int(delta),0)}")
    print(f"Total saved with rental and accelerated depreciation = ${int(delta_acc)}")
    print()
    print()
