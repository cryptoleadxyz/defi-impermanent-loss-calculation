# Objectives:
# This .py is based on 1_impermanent_loss_calculator.py but incorporating % from total pool and trading fee

from math import sqrt

# Input parameters
initial_token_a_price = 100
initial_token_b_price = 1
initial_token_a_quantity = 1

final_token_a_price = 200
final_token_b_price = 1

user_holding_as_percent_of_total_pool = 0.1 # user's initial holding is {i.e.,10%} of that of the total pool
final_trading_fee_collected_as_token_a = 1
final_trading_fee_collected_as_token_b = 100

# Impermanent loss calculation, based on 2 fomulas
# 1) Equal value of LP token-pair: after change in price, both assets must be equal in value (price * quantity)
# 2) Constant product formuula: after change in price, quantities of A and B in the pool remains constant, regardless of the changes in their individual prices

# Find initial quantity of token b; and initial product of token a and token b
initial_price_ratio = initial_token_a_price / initial_token_b_price
initial_token_b_quantity = (
    initial_token_a_price * initial_token_a_quantity
) / initial_token_b_price
k = initial_token_a_quantity * initial_token_b_quantity

print("Price of Token A at time_1:", initial_token_a_price)
print("Quantity of Token A at time_1:", initial_token_a_quantity)
print(
    "Total value of Token A in LP pool at time_1:",
    initial_token_a_price * initial_token_a_quantity,
)
print()
print("Price of Token B at time_1:", initial_token_b_price)
print("Quantity of Token B at time_1:", initial_token_b_quantity)
print(
    "Total value of Token B in LP pool at time_1:",
    initial_token_b_price * initial_token_b_quantity,
)
print()
print("Price tatio at time_1:", initial_price_ratio)
print(
    "Total value of both tokens in LP pool at time_1:",
    (initial_token_a_price * initial_token_a_quantity)
    + (initial_token_b_price * initial_token_b_quantity),
)
print("Constant K in constant product formula:", k)

# (quantity of token a) * (quantity of token b) = k
# (price ratio of token a) = (quantity of token b)/(quantity of token a)
# Derivation using the above two formulas:
# 1.1) (quantity of token a) = k/(quantity of token b)
# 1.2) Because, (quantity of token b) = (price ratio of token a) * (quantitfy of token a)
# 1.3) Thus, (quantity of token a) = k/((price ratio of token a) * (quantitfy of token a))
# 1.4) (quantity of token a)^2 = k/(price ratio of token a)
# 1.5) Finally, (quantity of token a) = sqrt(k/(price ratio of token a))

# 2.1) (quantity of token b) = k/(quantity of token a)
# 2.2) Because, (quantity of token b) = (price ratio of token a) * (quantitfy of token a)
# 2.3) Thus, (quantity of token b)^2 = (price ratio of token a) * (quantitfy of token a) * k/(quantity of token a)
# 2.4) Finally, (quantity of token b) = sqrt(k*(price ratio of token a))

# Factor into the change in price
initial_token_a_quantity_check = sqrt(k / initial_price_ratio)
initial_token_b_quantity_check = sqrt(k * initial_price_ratio)

assert initial_token_a_quantity == initial_token_a_quantity_check
assert initial_token_b_quantity == initial_token_b_quantity_check

final_price_ratio = final_token_a_price / final_token_b_price
final_token_a_quantity = sqrt(k / final_price_ratio)
final_token_b_quantity = sqrt(k * final_price_ratio)

print()
print("Price of Token A at time_2:", final_token_a_price)
print("Quantity of Token A at time_2:", final_token_a_quantity)
print(
    "Total value of Token A in LP pool at time_2:",
    final_token_a_price * final_token_a_quantity,
)
print()
print("Price of Token B at time_2:", final_token_b_price)
print("Quantity of Token B at time_2:", final_token_b_quantity)
print(
    "Total value of Token B in LP pool at time_2:",
    final_token_b_price * final_token_b_quantity,
)
print()
print("Price tatio at time_2:", final_price_ratio)
print(
    "Total value of both tokens in LP pool at time_2:",
    (final_token_a_price * final_token_a_quantity)
    + (final_token_b_price * final_token_b_quantity),
)
print("Constant K in constant product formula:", k)


# Option 1 - impermanent loss calculation
# Subtract the total LP pool value for hodling the original tokens with new prices by the total LP pool value from providing LP
impermanent_loss_in_value = (
    (final_token_a_price) * (final_token_a_quantity)
    + (final_token_b_price) * (final_token_b_quantity)
) - (
    (final_token_a_price) * (initial_token_a_quantity)
    + (final_token_b_price) * (initial_token_b_quantity)
)
impermanent_loss_in_percent = impermanent_loss_in_value / (
    (final_token_a_price) * (initial_token_a_quantity)
    + (final_token_b_price) * (initial_token_b_quantity)
)

print()
print("Impermanent loss in value:", impermanent_loss_in_value)
print("Impermanent loss in percent:", impermanent_loss_in_percent)


# Option 2 - impermanent loss calculation
# Once you have the change in price ratio, you can plug it into this formula and compute IL directly
def impermenant_loss_calculator(initial_token_price, final_token_price):
    price_ratio = final_token_price / initial_token_price
    return (2 * sqrt(price_ratio)) / (1 + price_ratio) - 1


print()
print(
    "Impermanent loss in percent:",
    impermenant_loss_calculator(initial_token_a_price, final_token_a_price),
)

# Calculate impermenant loss by including % of fee collected by LP pool
final_user_collected_fee_in_token_a = user_holding_as_percent_of_total_pool * final_trading_fee_collected_as_token_a
final_user_collected_fee_in_token_b = user_holding_as_percent_of_total_pool * final_trading_fee_collected_as_token_b

final_token_a_quantity_with_fee = final_token_a_quantity + final_user_collected_fee_in_token_a
final_token_b_quantity_with_fee = final_token_b_quantity + final_user_collected_fee_in_token_b

impermanent_loss_in_value_with_fee = (
    (final_token_a_price) * (final_token_a_quantity_with_fee)
    + (final_token_b_price) * (final_token_b_quantity_with_fee)
) - (
    (final_token_a_price) * (initial_token_a_quantity)
    + (final_token_b_price) * (initial_token_b_quantity)
)
impermanent_loss_in_percent_with_fee = impermanent_loss_in_value_with_fee  / (
    (final_token_a_price) * (initial_token_a_quantity)
    + (final_token_b_price) * (initial_token_b_quantity)
)

print()
print("Impermanent loss (with fee) in value:", impermanent_loss_in_value_with_fee )
print("Impermanent loss (with fee) in percent:", impermanent_loss_in_percent_with_fee)
