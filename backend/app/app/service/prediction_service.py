from collections import ChainMap
from datetime import date
from random import choices as rl_agent_decisioning

from app.schemas.state import Gender, Region, State


def filter_b_company(data):
    new_data = []
    for row in data[1:]:
        if row[5] == 'Europa':
            row[10] = 'False'
            row[11] = 'False'
            row[12] = 'False'
        if int(row[1]) > 65:
            row[7] = 'False'
            row[9] = 'False'
            row[10] = 'False'
        state = State()
        state.age = int(row[1])
        state.region = (Region[row[5]] if row[5] != '' else Region.Asia)
        state.gender = get_gender(row[3])
        state.client_since = row[4]
        state.last_offer = row[6]
        offers = []
        index_value = 1
        for offer in row[7:16]:
            offers.append({f'Offer_{index_value}': offer})
            index_value += 1
        new_data.append({'best_offers': dict(ChainMap(*rl_agent(state, ChainMap(*offers)))),
                         'customer_id': row[0],
                         'response_date': str(date.today())})
    return new_data


def get_gender(gender: str):
    if gender.lower() == 'male':
        return Gender.M
    elif gender.lower() == 'female':
        return Gender.F
    elif gender.lower() == '':
        return Gender.M
    else:
        return Gender[gender.upper()]


def rl_agent(customer_state, offers):
    weights = []
    print(f"logging customer_state age: {customer_state.age}")
    if customer_state.age < 30:
        weights = [10, 8, 6, 6, 6, 4]
    else:
        weights = [8, 6, 10, 6, 4]
    only_true_offers = []
    for offer, value in offers.items():
        if value == 'True':
            only_true_offers.append({offer: value})
    print(f"logging customer_state region: {customer_state.region}")
    if customer_state.region == Region.Europa:
        weights = [10, 8, 6, 6, 10, 10]
    elif customer_state.region == Region.Americas:
        weights = [4, 8, 6, 6, 10, 10]
    elif customer_state.region == Region.Asia:
        weights = [4, 10, 10, 6, 4, 4]
    else:
        raise Exception(f"weight by region not applied, is categorical data ?")
    print(f"logging customer_state gender: {customer_state.gender}")
    if customer_state.gender == Gender.M:
        weights = [10, 10, 10, 6, 4, 4]
    elif customer_state.gender == Gender.F:
        weights = [4, 4, 6, 10, 10, 10]
    else:
        raise Exception(f"weight by gender was not applied, is categorical data?")
    if len(weights) > len(only_true_offers):
        weights = weights[0:len(only_true_offers)]
    elif len(only_true_offers) > len(weights):
        only_true_offers = only_true_offers[0:len(weights)]
    return rl_agent_decisioning(only_true_offers, weights=weights, k=3)
