def get_fed_taxes_2021(taxable_income, filing_status, use_standard_deduction=True):
    standard_deduction = 12550
    lst = [.1, .12, .22, .24, .32, .35, .37]
    single_bracket = {0: 9950, 1: 40535, 2: 86375, 3: 164925, 4: 209425, 5: 523600}
    joint_bracket = {0: 19900, 1: 81050, 2: 172750, 3: 329850, 4: 418850, 5: 628300}

    # get filing status 
    if filing_status == 'single':
        b = single_bracket

        # get standard deduction
        if use_standard_deduction:
            taxable_income = max(0, taxable_income - standard_deduction)

    elif filing_status == 'joint':
        b = joint_bracket

        # get standard deduction
        if use_standard_deduction:
            taxable_income = max(0, taxable_income - standard_deduction * 2)

    b0 = lst[0] * b.get(0)
    b1 = b0 + lst[1] * (b.get(1) - b.get(0))
    b2 = b1 + lst[2] * (b.get(2) - b.get(1))
    b3 = b2 + lst[3] * (b.get(3) - b.get(2))
    b4 = b3 + lst[4] * (b.get(4) - b.get(3))
    b5 = b4 + lst[5] * (b.get(5) - b.get(4))

    # get tax amount
    if taxable_income <= b.get(0):
        return lst[0] * taxable_income
    elif taxable_income <= b.get(1):
        return b0 + lst[1] * (taxable_income - b.get(0))
    elif taxable_income <= b.get(2):
        return b1 + lst[2] * (taxable_income - b.get(1))
    elif taxable_income <= b.get(3):
        return b2 + lst[3] * (taxable_income - b.get(2))
    elif taxable_income <= b.get(4):
        return b3 + lst[4] * (taxable_income - b.get(3))
    elif taxable_income <= b.get(5):
        return b4 + lst[5] * (taxable_income - b.get(4))
    else:
        return b5 + lst[6] * (taxable_income - b.get(5))
