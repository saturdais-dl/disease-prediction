import pandas as pd
import numpy as np
import wfdb
import ast

def load_raw_data(df, sampling_rate, path):
    """
    Loads raw ECG data from the specified files and returns it as a numpy array.

    Parameters:
    df (pandas.DataFrame): DataFrame containing the filenames of the ECG records.
    sampling_rate (int): The sampling rate of the ECG data. If 100, low-resolution data is loaded; otherwise, high-resolution data is loaded.
    path (str): The path to the directory containing the ECG data files.

    Returns:
    numpy.ndarray: A numpy array containing the loaded ECG signals.

    Example:
    df = pd.read_csv('ptbxl_database.csv')
    data = load_raw_data(df, 100, '/path/to/data/')
    """
    if sampling_rate == 100:
        data = [wfdb.rdsamp(path + f) for f in df.filename_lr]
    else:
        data = [wfdb.rdsamp(path + f) for f in df.filename_hr]
    data = np.array([signal for signal, meta in data])
    return data

def aggregate_diagnostic(y_dic, agg_df):
    """
    Aggregates diagnostic information from the provided diagnostic codes using the aggregation DataFrame.

    Parameters:
    y_dic (dict): A dictionary of diagnostic codes for a single ECG record.
    agg_df (pandas.DataFrame): DataFrame containing diagnostic aggregation information.

    Returns:
    list: A list of aggregated diagnostic classes for the provided diagnostic codes.

    Example:
    agg_df = pd.read_csv('scp_statements.csv', index_col=0)
    y_dic = {'NORM': 1, 'MI': 2}
    aggregated = aggregate_diagnostic(y_dic, agg_df)
    """
    tmp = []
    for key in y_dic.keys():
        if key in agg_df.index:
            tmp.append(agg_df.loc[key].diagnostic_class)
    return list(set(tmp))


def load_data_from_directory(path_to_directory, sampling_rate):
    """
    Loads patient data, ECG data, and performs diagnostic aggregation.

    Parameters:
    path_to_directory (str): The path to the directory containing the data files.
    sampling_rate (int): The sampling rate of the ECG data.

    Returns:
    tuple: A tuple containing:
        - numpy.ndarray: A numpy array containing the loaded ECG signals.
        - pandas.DataFrame: DataFrame containing patient and diagnostic data.
        - pandas.DataFrame: DataFrame containing diagnostic aggregation information.

    Example:
    path = '/path/to/data/'
    sampling_rate = 100
    X, Y, agg_df = load_data_from_directory(path, sampling_rate)
    """
    # Load and convert annotation data
    Y = pd.read_csv(path_to_directory + 'ptbxl_database.csv', index_col='ecg_id')
    Y.scp_codes = Y.scp_codes.apply(lambda x: ast.literal_eval(x))

    # Load raw signal data
    X = load_raw_data(Y, sampling_rate, path_to_directory)

    # Load scp_statements.csv for diagnostic aggregation
    agg_df = pd.read_csv(path_to_directory + 'scp_statements.csv', index_col=0)
    agg_df = agg_df[agg_df.diagnostic == 1]

    Y['diagnostic_superclass'] = Y.scp_codes.apply(lambda x: aggregate_diagnostic(x, agg_df))

    return X, Y, agg_df

def get_train_test_split(X, Y, test_fold=10, validation=False):
    """
    Splits the data into training, test, and optionally validation sets based on the stratification fold.

    Parameters:
    X (numpy.ndarray): The ECG signal data.
    Y (pandas.DataFrame): DataFrame containing patient and diagnostic data.
    test_fold (int, optional): The fold number to use for the test set. Defaults to 10.
    validation (bool, optional): Whether to include a validation set. Defaults to False.

    Returns:
    tuple: A tuple containing:
        - numpy.ndarray: Training set ECG signals.
        - numpy.ndarray: Test set ECG signals.
        - pandas.Series: Training set diagnostic classes.
        - pandas.Series: Test set diagnostic classes.
        - numpy.ndarray (optional): Validation set ECG signals.
        - pandas.Series (optional): Validation set diagnostic classes.

    Example:
    X_train, X_test, y_train, y_test = get_train_test_split(X, Y, test_fold=10)
    """
    validation_folds = [8, 9]
    # From the documentation of the dataset, they recommend for the test fold to be 10 and 8 and 9 as validation.

    X_train = X[np.where((Y.strat_fold != test_fold) & (~Y.strat_fold.isin(validation_folds)))]
    y_train = Y[(Y.strat_fold != test_fold) & (~Y.strat_fold.isin(validation_folds))].diagnostic_superclass

    X_test = X[np.where(Y.strat_fold == test_fold)]
    y_test = Y[Y.strat_fold == test_fold].diagnostic_superclass

    if validation:
        X_val = X[np.where(Y.strat_fold.isin(validation_folds))]
        y_val = Y[Y.strat_fold.isin(validation_folds)].diagnostic_superclass

        return X_train, X_test, y_train, y_test, X_val, y_val
    else:
        return X_train, X_test, y_train, y_test
