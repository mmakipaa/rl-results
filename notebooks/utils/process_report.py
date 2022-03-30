import pandas as pd
import numpy as np


def process_report(df_report, df_ref):

 
    df_reference, ref_change_points = process_reference(df_ref)
    df_sa = df_report.copy()
    df_sa = df_sa.fillna(value=np.nan)

    df_sa = calc_max_action_values_for_state(df_sa)
    df_sa = add_ref_values_and_mse(df_sa, df_reference)
    df_states = create_and_label_states(df_sa)
    df_states = add_ref_values_to_states(df_states, df_reference)

    return df_reference, ref_change_points, df_sa, df_states

# REFERENCE BELOW

def find_change_point(x):
    
    fill_v = x['ref_a_is_max'].iloc[-1]
    return x.loc[x['ref_a_is_max'] != x['ref_a_is_max'].shift(-1,fill_value=fill_v) ,'player']

def process_reference(df_ref):
    df_reference = df_ref.loc[df_ref['iterations'] == df_ref['iterations'].max(),['dealer', 'player', 'soft', 'action', 'value']] \
                        .rename(columns={"value": "ref_value"})

    df_refg = df_reference.groupby(['dealer', 'player', 'soft'])

    df_reference['ref_s_max_value'] = df_refg['ref_value'].transform('max') 
    df_reference['ref_a_is_max'] = df_reference['ref_value'] == df_reference['ref_s_max_value']

    df_reference = df_reference.drop('ref_s_max_value', axis='columns').reset_index(drop=True)


    df_refg = df_reference.sort_values(['soft', 'action', 'dealer','player']).groupby(['soft', 'action', 'dealer'])

    df_ref_change_points = df_refg.apply(find_change_point).reset_index(name='change_point').drop(columns=['level_3'])

    return df_reference, df_ref_change_points

# NEW FUNCTIONS BELOW

def calc_max_action_values_for_state(df_sa):

    dg = df_sa.groupby(['agent', 'iterations', 'dealer', 'player', 'soft'])
    df_sa['s_max_value'] = dg['value'].transform('max')
    df_sa['a_is_max'] = df_sa['value'] == df_sa['s_max_value']

    df_sa = df_sa.drop('s_max_value', axis='columns')

    return df_sa

def add_ref_values_and_mse(df_sa, df_reference):

    df_sa = pd.merge(df_sa, df_reference, on=['dealer','player','soft','action'], how='left')

    df_sa['sq_error'] = (df_sa['value'] - df_sa['ref_value']) ** 2

    return df_sa

# TODO: WHAT IS X, RENAME?

def create_state_labels(state):

    INITIAL_Q = 0

    HIT = 5
    HIT_ONE = 4
    STAND_ONE = 3
    STAND = 2
    SAME = 1
    BLANK = 0

    if state['visit_count'].isna().sum() == 2:
        # no visit counts, skip analysis
        not_visited = 0
    else:
        not_visited = sum(state['visit_count'] == 0)

    if not_visited == 2:
        return_label = BLANK
        return_action = np.nan

    elif not_visited == 1:
        seen_value = state.loc[state['visit_count'] > 0,'value'].iloc[0]
        seen_action = state.loc[state['visit_count'] > 0,'action'].iloc[0]

        if seen_value < INITIAL_Q:
            if seen_action == True:
                return_label = STAND_ONE
                return_action = False
            else:
                return_label = HIT_ONE
                return_action = True

        elif seen_value > INITIAL_Q:
            if seen_action == True:
                return_label = HIT_ONE
                return_action = True
            else:
                return_label = STAND_ONE
                return_action = False

        elif seen_value == INITIAL_Q:
            return_label = SAME
            return_action = np.nan
        else:
            raise SystemExit("NOW WE HAVE A PROBLEM - ties")

    elif not_visited == 0:
        if state['value'].max() > state['value'].min():
            return_action = state.loc[state['value'] == state['value'].max(),'action'].iloc[0]
            if return_action == True:
                return_label = HIT
            elif return_action == False:
                return_label = STAND
        elif state['value'].max() == state['value'].min():
            return_action = np.nan
            return_label = SAME
        else:
            raise SystemExit("NOW WE HAVE A PROBLEM - values")
    else:
        raise SystemExit("NOW WE HAVE A PROBLEM - not_visited")

    return pd.Series([ return_action, return_label ],index=['s_best_action', 's_label'])


def create_and_label_states(df_sa):

    dg = df_sa.groupby(['agent', 'iterations', 'dealer', 'player', 'soft'])

    dg_first = dg.agg(
        s_visited_actions=('visit_count', lambda x: np.NaN if x.isna().any() else sum(x>0) ), 
        s_visits=('visit_count',lambda x: x.sum(skipna=False)), 
        s_min_value=('value', 'min'),
        s_max_value=('value', 'max'),
        s_diff=('value',lambda x: x.max() - x.min())
    )
    dg_second = dg.apply(create_state_labels)

    df_states = pd.merge(dg_first, dg_second, on=['agent', 'iterations', 'dealer', 'player', 'soft'], how='inner').reset_index()

    return df_states


def add_ref_values_to_states(df_states, df_reference):
    df_ref_max= df_reference.loc[df_reference['ref_a_is_max']].drop(['ref_a_is_max'], axis='columns')
    df_ref_max = df_ref_max.rename(columns={"action": "ref_best_action", "ref_value": "ref_s_max_value"})

    df_states = pd.merge(df_states, df_ref_max, on=['dealer', 'player', 'soft'], how='inner').reset_index()

    return df_states