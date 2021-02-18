import datetime

import numpy as np
import pandas as pd
from scipy.optimize import minimize


# initial data processing

def select_data(df: pd.DataFrame, tickers: list, start: str, end: str):
    df_2 = df[tickers]
    df_2 = df_2[df_2.index >= start]
    df_2 = df_2[df_2.index <= end]
    return df_2


def process_data(df: pd.DataFrame):
    return np.log(df / df.shift(1))[1:]


def get_statistics(series: pd.Series):
    stats = series.describe()
    stats = stats.append(pd.Series([series.kurtosis()], index=['kurtosis']))
    stats = stats.append(pd.Series([series.skew()], index=['skewness']))

    df_stats = pd.DataFrame(columns=['Measure', 'Value'])
    df_stats['Measure'] = stats.index.to_list()
    df_stats['Value'] = stats.to_list()
    return df_stats


# MPT functions

def calculate_risk(covariance_matrix: pd.DataFrame, periods: int, weights: list):
    weights = np.asarray(weights)
    return np.sqrt(np.dot(np.dot(weights.T, covariance_matrix * periods), weights))


def optimize_risk(covariance_matrix: pd.DataFrame, periods: int):
    function = lambda weights: calculate_risk(covariance_matrix, periods, weights)
    constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
    bounds = tuple([(0, 1) for _ in range(covariance_matrix.shape[0])])
    vector = [1 / covariance_matrix.shape[0] for _ in range(covariance_matrix.shape[0])]
    return minimize(function, vector, method='SLSQP', bounds=bounds, constraints=constraints).x


def calculate_sharpe(returns: pd.Series, covariance_matrix: pd.DataFrame, periods: int, risk_free_rate: float, weights: list):
    return (np.dot(returns, weights) * periods - risk_free_rate) / calculate_risk(covariance_matrix, periods, weights)


def optimize_sharpe(returns: pd.Series, covariance_matrix: pd.DataFrame, periods: int, risk_free_rate: float):
    function = lambda weights: -calculate_sharpe(returns, covariance_matrix, periods, risk_free_rate, weights)
    constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
    bounds = tuple([(0, 1) for _ in range(covariance_matrix.shape[0])])
    vector = [1 / covariance_matrix.shape[0] for _ in range(covariance_matrix.shape[0])]
    return minimize(function, vector, method='SLSQP', bounds=bounds, constraints=constraints).x


def get_results(returns: pd.Series, covariance_matrix: pd.DataFrame, periods: int, risk_free_rate: float, weights: list):

    expected_return = np.dot(returns, weights) * periods
    risk = calculate_risk(covariance_matrix, periods, weights)
    sharpe = calculate_sharpe(returns, covariance_matrix, periods, risk_free_rate, weights)

    tmp_res_dict = {
        'ExpReturn': expected_return,
        'Risk': risk,
        'Sharpe': sharpe
    }

    return tmp_res_dict


def run_mpt_calculations(df_est, df_eval, risk_free_rate):

    eval_periods = len(df_eval.index) + 1
    eval_returns = df_eval.mean()
    eval_covariance = df_eval.cov()

    w_naive = [1 / len(df_est.columns) for x in range(len(df_est.columns))]

    list_min_risk = []
    list_max_eff = []
    list_naive = []

    for days in range(3, len(df_est.index)):

        est_returns = df_est.iloc[-days:].mean()
        est_covariance = df_est.iloc[-days:].cov()

        w_min_risk = optimize_risk(est_covariance, days)
        w_max_eff = optimize_sharpe(est_returns, est_covariance, days, risk_free_rate)

        list_min_risk.append(get_results(eval_returns, eval_covariance, eval_periods, risk_free_rate, w_min_risk))
        list_max_eff.append(get_results(eval_returns, eval_covariance, eval_periods, risk_free_rate, w_max_eff))
        list_naive.append(get_results(eval_returns, eval_covariance, eval_periods, risk_free_rate, w_naive))

    df_min_risk = pd.DataFrame(data=list_min_risk, columns=['ExpReturn', 'Risk', 'Sharpe'])
    df_max_eff = pd.DataFrame(data=list_max_eff, columns=['ExpReturn', 'Risk', 'Sharpe'])
    df_naive = pd.DataFrame(data=list_naive, columns=['ExpReturn', 'Risk', 'Sharpe'])

    df_min_risk['strategy'] = 'min_risk'
    df_max_eff['strategy'] = 'max_eff'
    df_naive['strategy'] = 'naive'

    days = [x for x in range(3, len(df_est.index))]

    df_min_risk['days'] = days
    df_max_eff['days'] = days
    df_naive['days'] = days

    return pd.concat([df_min_risk, df_max_eff, df_naive])


# additional

def validate_input_data(df: pd.DataFrame):

    issues = []
    dates = df.index.to_list()

    if dates != sorted(dates):
        issues.append('Dates are not in ascending order.')

    def validate_date(date: str):
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    if False in [validate_date(date) for date in dates]:
        issues.append('Date format is not valid.')

    columns = df.columns.to_list()

    for column in columns:
        value_list = df[column].to_list()
        if False in [type(value) in [int, float] for value in value_list]:
            issues.append('Some of values are not of int / float type.')
            break

    return issues


