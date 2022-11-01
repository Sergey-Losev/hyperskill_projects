import pandas as pd
import os
import requests
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Check for ../Data directory presence
if not os.path.exists('../Data'):
    os.mkdir('../Data')

# Download data if it is unavailable.
if 'nba2k-full.csv' not in os.listdir('../Data'):
    print('Train dataset loading.')
    url = "https://www.dropbox.com/s/wmgqf23ugn9sr3b/nba2k-full.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('../Data/nba2k-full.csv', 'wb').write(r.content)
    print('Loaded.')

data_path = "../Data/nba2k-full.csv"


def clean_data(path):
    # 1. Load a DataFrame from the location specified in the path
    df = pd.read_csv(path)
    # 2. Parse the b_day and draft_year features as datetime objects;
    df['b_day'] = pd.to_datetime(df['b_day'])
    df['draft_year'] = pd.to_datetime(df['draft_year'], format='%Y')
    # 3. Replace the missing values in team feature with "No Team";
    df['team'].fillna('No Team', inplace=True)
    # 4. Take the height feature in meters and the weight feature in kg;
    df['weight'] = df['weight'].str.split(' / ', expand=True).iloc[:, 1].str.replace(' kg.', '').astype(float)
    df['height'] = df['height'].str.split(' / ', expand=True).iloc[:, 1].astype(float)
    # 5. Remove the extraneous $ character from the salary feature;
    df['salary'] = df['salary'].str.replace('$', '').astype(float)
    # 6. Parse the height, weight, and salary features as floats - done earlier at once;
    # 7. Categorize the country feature as "USA" and "Not-USA";
    df.loc[df['country'] != 'USA', 'country'] = 'Not-USA'
    # 8. Replace the cells containing "Undrafted" in the draft_round feature with the string "0";
    df.loc[df['draft_round'] == 'Undrafted', 'draft_round'] = '0'
    # 9. Return the modified DataFrame.
    return df


def feature_data(df):
    # 1. The input parameter is the returned DataFrame from the
    # clean_data function from the previous stage;
    # Replace game-name to year
    df.version = df.version.str.replace('NBA2k20', '2020').replace('NBA2k21', '2021')
    # 2. Get the unique values in the version column of the DataFrame you got from
    # clean_data as a year (2020, for example) and parse as a datetime object;
    # Make a date from string
    df.version = pd.to_datetime(df.version, format='%Y')
    # 3. Engineer the age feature by subtracting b_day column from version;
    df['age'] = df['version'].dt.to_period('Y').astype(int) - df['b_day'].dt.to_period('Y').astype(int)
    # 4. Engineer the experience feature by subtracting draft_year column from version;
    df['experience'] = df['version'].dt.to_period('Y').astype(int) - df['draft_year'].dt.to_period('Y').astype(int)
    # 5.Engineer the body mass index feature from weight (ww)
    # and height (hh) columns. The formula is bmi = w / h^2 bmi=w/h2;
    df['bmi'] = df.weight / df.height ** 2
    # 6. Drop the version, b_day, draft_year, weight, and height columns;
    df.drop(columns=['version', 'b_day', 'draft_year', 'weight', 'height'], inplace=True)
    # 7. Remove the high cardinality features;
    columns = []
    for item in df.columns[:-3]:
        if df[item].nunique() > 50 and df[item].dtype != 'float64':
            columns.append(item)
    df.drop(columns=columns, inplace=True)
    # 8. Return the modified DataFrame.
    return df


def multicol_data(df):
    """
    Drop multicollinear features from the DataFrame that you got from the feature_data;
    :param df:
    The input parameter is the returned DataFrame from the feature_data function;
    :return:
    Return the modified DataFrame.
    """
    corr = df.select_dtypes('number').drop(columns='salary').corr()
    correlated_features = []
    for i in range(corr.shape[0]):
        for j in range(0, i):
            if corr.iloc[i, j] > 0.5 or corr.iloc[i, j] < -0.5:
                correlated_features.append([corr.columns[i], corr.index[j]])

    for feature1, feature2 in correlated_features:
        if df[[feature1, 'salary']].corr().iloc[1, 0] > df[[feature2, 'salary']].corr().iloc[1, 0]:
            df.drop(columns=feature2, inplace=True)
        else:
            df.drop(columns=feature1, inplace=True)

    return df


def transform_data(df):
    """
    Transform numerical features in the DataFrame it got from multicol_data using StandardScaler;
    Transform nominal categorical variables in the DataFrame using OneHotEncoder;
    Concatenate the transformed numerical and categorical features in the following order: numerical features,
    then nominal categorical features;
    :param df:
    As the input parameter, take the DataFrame returned from multicol_data function, which you implemented in the
    previous stage;
    :return:
    Return two objects: X, where all the features are stored, and y with the target variable.
    """
    num_feat_df = df.select_dtypes('number')  # numerical features
    cat_feat_df = df.select_dtypes('object')  # categorical features
    object_ = StandardScaler()
    num_feat_df_scaled = object_.fit_transform(num_feat_df[['rating', 'experience', 'bmi']])
    num_feat_df_scaled = pd.DataFrame(num_feat_df_scaled, columns=num_feat_df[['rating', 'experience', 'bmi']].columns)
    enc = OneHotEncoder(sparse=False)

    def one_hot(dataframe):
        """
        This is the function to apply features' to the corresponding columns of the given dataframe
        """
        new_df = pd.DataFrame()
        for column in dataframe:
            result = enc.fit_transform(pd.DataFrame(dataframe[column]))
            df_enc = pd.DataFrame(result, columns=enc.categories_[0])
            new_df = pd.concat([new_df, df_enc], axis=1)
        return new_df

    cat_feat_df_enc = one_hot(cat_feat_df)

    x = pd.concat([num_feat_df_scaled, cat_feat_df_enc], axis=1)
    y = df.salary
    return x, y
