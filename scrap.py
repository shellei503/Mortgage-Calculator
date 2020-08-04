h_l = 700
o_s = 650
m = 550
a = 450

property_taxes = 4000
homeowners = 880
water = 100
gas = 15
electric = 500
internet = 100
landscaping = 600
# mortgage = 1122
mortgage = 1221


monthly_expense = mortgage - property_taxes/12 + homeowners/12 + water + gas + electric + internet + landscaping
revenue = h_l + o_s + m + a
profit = revenue - monthly_expense
annual_home_cost = property_taxes + homeowners + landscaping + mortgage*12
recommended_home_rental_rate_9= annual_home_cost/9
recommended_home_rental_rate_12= annual_home_cost/12

print('monthly_expense',monthly_expense)
print('revenue',revenue)
print('profit',profit)
print('recommended_home_rental_rate_12',recommended_home_rental_rate_12)
print('recommended_home_rental_rate_9',recommended_home_rental_rate_9)