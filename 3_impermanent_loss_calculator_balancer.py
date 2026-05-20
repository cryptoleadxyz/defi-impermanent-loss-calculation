# Objectives:
# Previous examples only deal with impermanent loss calculation with equal (or 50:50) token pair. In Balancer, token pairs can have different proportion and can have more than 2 tokens, this .py derives the "flexible" impermanent loss calculation based on the formulas of the following link
# Reference URL = https://chainbulletin.com/impermanent-loss-explained-with-examples-math


def k_calculator(token_quantity_weight_dict):
    """token_quantity_weight_dict: dictionary object that has 'quantity' and 'weight' for each token."""
    k = 1
    total_weight = 0

    for key, val in token_quantity_weight_dict.items():
        print(key, val)

        k = k * val["quantity"] ** val["weight"]

        total_weight += val["weight"]

    assert (total_weight >= 0.99) & (total_weight <= 1.01)

    return k


def flexible_impermanent_loss_calculator(token_price_change_weight_dict):
    """token_quantity_weight_dict: dictionary object that has 'price change' and 'weight' for each token."""
    numerator = 1
    denominator = 0
    total_weight = 0

    for key, val in token_price_change_weight_dict.items():
        print(key, val)

        numerator = numerator * val["price change"] ** val["weight"]
        denominator += val["price change"] * val["weight"]

        total_weight += val["weight"]

    assert (total_weight >= 0.99) & (total_weight <= 1.01)

    return (numerator / denominator) - 1


# Input parameters
token_quantity_weight_dict = {
    "token_a": {"quantity": 10, "weight": 0.2},
    "token_b": {"quantity": 100, "weight": 0.4},
    "token_c": {"quantity": 50, "weight": 0.4},
}

initial_token_a_price = 10
initial_token_b_price = 1
initial_token_c_price = 100

final_token_a_price = 10
final_token_b_price = 2
final_token_c_price = 5000


user_holding_as_percent_of_total_pool = (
    0.1  # user's initial holding is {i.e.,10%} of that of the total pool
)

k = k_calculator(token_quantity_weight_dict)
print("Constant K:", k)

# Prepare another input dictionary that includes price change (in relative term)
token_price_change_weight_dict = {
    "token_a": {
        "price change": final_token_a_price / initial_token_a_price,
        "weight": 0.2,
    },
    "token_b": {
        "price change": final_token_b_price / initial_token_b_price,
        "weight": 0.4,
    },
    "token_c": {
        "price change": final_token_c_price / initial_token_c_price,
        "weight": 0.4,
    },
}

impermanent_loss = flexible_impermanent_loss_calculator(token_price_change_weight_dict)
print("Impermanent loss:", impermanent_loss)
