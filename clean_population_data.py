import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Define whether we're running in Jupyter or not
JUPYTER = False

def remove_typos(df):
    # Remove ' (_typo)' from category names
    df['income_groups'] = df['income_groups'].str.replace('_typo', '', regex=False)
    return df


def remove_duplicates(df):
    df = df.drop_duplicates()
    return df


def convert_types(df):
    # Convert 'income_groups' column to category type
    df['income_groups'] = df['income_groups'].astype('category')
    # Convert 'age' column to integer type
    df['age'] = df['age'].fillna(-1).astype(int)
    # Convert 'gender' column to category type
    df['gender'] = df['gender'].fillna(-1).astype(int)
    # Convert 'year' column to integer type
    df['year'] = df['year'].fillna(-1).astype(int)
    # Convert 'population' column to integer type
    df['population'] = df['population'].fillna(-1).astype(int)
    return df

#This function will find all the missing value datas' indexes
def find_missing_data_index(df):
    #Find all missing values by each category
    missing_income = df[df['income_groups'].isnull()]
    missing_age=df[df['age']==-1]
    missing_gender=df[(df['gender']== -1) | (df['gender'] == 3)]
    missing_year=df[df['year']==-1]
    missing_population=df[df['population']==-1]

    #Store the index of the missing values
    missing_income_row = missing_income.index
    missing_age_row = missing_age.index
    missing_gender_row = missing_gender.index
    missing_year_row = missing_year.index
    missing_population_row = missing_population.index

    #Store the indexes in a 2D list that contains 5 lists of indexes
    list = [missing_income_row, missing_age_row, missing_gender_row, missing_year_row, missing_population_row]
    return list

#This function will try to correct the missing income_groups data
def fill_missing_incomegroups(df, missing_incomegroup_indexs):
    #4 data is expected with the same gender, age and year. 
    expected_groups = {'low_income', 'high_income', 'lower_middle_income', 'upper_middle_income'}

    #Loop through all the indexes, and extract the gender, age, year
    for missing_incomegroup_index in missing_incomegroup_indexs:
        this_gender = df.at[missing_incomegroup_index,'gender']
        this_age = df.at[missing_incomegroup_index,'age']
        this_year = df.at[missing_incomegroup_index,'year']
        
        #Save all the groups and ignore all the missing, incorrect data
        this_group = df[(df['gender'] == this_gender) &
                    (df['age'] == this_age) &
                    (df['year'] == this_year)&
                    (df['age'] != -1)&
                    (df['year'] != -1)&
                    (df['gender'] != -1)&
                    (df['gender'] != 3)]
        
        #If 4 data present, then proceed, if not, skip the code below and 
        # continue to the next iteration
        if len(this_group) != 4:
            continue
        #By having the expected_group minus present group's income_group, 
        # we can know what income_group the missing data is
        present_groups = set(this_group['income_groups'].dropna())
        missing_income_group = list(expected_groups - present_groups)

        #Replace the missing data with its correct value
        if len(missing_income_group) == 1:
            df.at[missing_incomegroup_index,'income_groups'] = missing_income_group[0]        
    return df


#This function will try to correct the missing gender data
def fill_missing_gender(df, missing_gender_indexs):
    #Iterate through the indexes of missing gender index
    for missing_gender_index in missing_gender_indexs:    
        #Extract the income, age, and year from this index
        # Two data, one gender 1 and one gender 2 is expected    
        this_income = df.at[missing_gender_index,'income_groups']
        this_age = df.at[missing_gender_index,'age']
        this_year = df.at[missing_gender_index,'year']

        #Group all data with the same income_groups, age, and year.
        this_group = df[
            (df['income_groups'] == this_income) &
            (df['age'] != -1) &  
            (df['age'] == this_age) &
            (df['year'] == this_year)]
        
        # Get unique genders in the group
        genders = this_group['gender'].unique()  
        
        #If if gender 2 is present while 1 is not, then missing data is 1
        if 2 in genders and 1 not in genders:
            df.at[missing_gender_index,'gender'] = 1

        #If if gender 1 is present while 2 is not, then missing data is 1
        elif 1 in genders and 2 not in genders:
            df.at[missing_gender_index,'gender'] = 2

        #Else, do nothing with the data
    return df 
    
#This function will try to input the missing population data
def fill_missing_population(df):
    #Since I replaced all missing values with -1 earlier,
    # so replace all -1 to NA
    df['population'] = df['population'].replace(-1, pd.NA)
    pd.set_option('future.no_silent_downcasting', True)

    #Use forward fill to fill the missing datas
    df['population'] = df['population'].ffill()
    return df

def plot_boxplot(df, column, filename=None):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df[column])
    plt.title(f'Boxplot of {column}')
    if JUPYTER:
        plt.show()
    else:
        plt.savefig(filename)
        plt.close()

if __name__ == '__main__':

    # Load the data
    df = pd.read_csv('messy_population_data.csv')
    print("Initial data shape:", df.shape)
    print("\nInitial data info:")
    df.info()


    # 1. Handling Inconsistent Categories
    print("\n1. Handling Inconsistent Categories")
    print("Unique categories before cleaning:")
    print(df['income_groups'].value_counts())
    df = remove_typos(df)
    print("\nUnique categories after cleaning:")
    print(df['income_groups'].value_counts())
    print("Shape after removing typos:", df.shape)


    # 2. Handling Duplicates
    print("\n2. Handling Duplicates")
    print("Duplicate rows:", df.duplicated().sum())
    df = remove_duplicates(df)
    print("Shape after removing duplicates:", df.shape)


    # 3. Data Type Conversions
    print("\n3. Data Type Conversions")
    print("Data types before:")
    print(df.dtypes)
    df= convert_types(df)
    print("\nData types after:")
    print(df.dtypes)
    

    # 4. Handling Missing Values
    print("\n4. Handling Missing Values")
    print("Missing values before:")
    incomegroups_null_count = df['income_groups'].isnull().sum()
    print(f"'income_groups': {incomegroups_null_count}")
    col_minus_one = ['age', 'gender', 'year', 'population']
    for column in col_minus_one:
        minus_one_count = (df[column] == -1).sum()
        print(f"'{column}': {minus_one_count}")
    print(df.shape)

    #Index 0 is missing_income_row
    #Index 2 is missing_gender_row
    missing_data_index_list = find_missing_data_index(df)
    df = fill_missing_gender(df, missing_data_index_list[2])
    df = fill_missing_incomegroups(df, missing_data_index_list[0])
    df = fill_missing_population(df)

    df = df[(df != -1).all(axis=1)]
    df = df[df['gender'] != 3]
    df = df.dropna()
    print("\nMissing values after:")
    print(df.isnull().sum())
    print(df.shape)


    # 5. Handling Outliers
    print("\n5. Handling Outliers")
    print("Shape after removing outliers:", df.shape)
    column = 'population'
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR))]
    df = df[~((df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR)))]
    plot_boxplot(df, 'population', 'population_boxplot_before.png')
    print("Shape after removing outliers:", df.shape)
    plot_boxplot(df, 'population', 'population_boxplot_after.png')


    # 6. Handling Incorrect Values
    print("\n6. Handling Incorrect Values")
    print("Year before cleaning:")
    print(df['year'].value_counts())
    # Filter the data to include only reasonable years (e.g., 1950-2100)
    df = df[(df['year'] >= 1950) & (df['year'] <= 2100)]
    print("\nYear after cleaning:")
    print(df['year'].value_counts())


    # 7. Feature Engineering
    print("\n7. Feature Engineering")
    df['age_group'] = pd.cut(df['age'], bins=[-1, 18, 35, 60, 100], 
                         labels=['Child', 'Young Adult', 'Adult', 'Elderly'])
    
    df['era'] = pd.cut(df['year'], bins=[1949, 1980, 2000, 2025, 2100], 
                   labels=['Middle 50th', 'Late 20th', 'Early 21st', 'Future'])
    
    print(df[['age', 'age_group', 'year', 'era', 'income_groups', 'population']].head())


    # 8. Encoding Categorical Variables
    print("\n8. Encoding Categorical Variables")
    # one-hot encoding
    df_encoded = pd.get_dummies(df, columns=['income_groups'], prefix='inc')  # Drop first to avoid redundancy
    print("\nShape after one-hot encoding:", df.shape)


    # 9. Final Data Quality Check
    print("\n9. Final Data Quality Check")
    print(df.describe())
    print(df_encoded.describe())
    print()
    print(df.info())
    # Display the number of unique values for each column
    for column in df.columns:
        unique_count = df[column].nunique()
        print(f"Number of unique values for '{column}': {unique_count}")

    #Correlation heatmap
    correlation_matrix = df_encoded.corr(numeric_only=True)  
    plt.figure(figsize=(10, 8))  
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Heatmap', fontsize=16)
    plt.savefig('correlation_heatmap.png')
    plt.close()


    # 10. Comparing with Original Clean Data
    print("\n10. Comparing with Original Clean Data")
    df_o = pd.read_csv('messy_population_data.csv')

    print("Original dirty data shape:", df_o.shape)
    print("Cleaned messy data shape:", df.shape)

    common_columns = set(df_o.columns) & set(df.columns)
    for column in common_columns:
        if df_o[column].dtype != df[column].dtype:
            print(f"Data type mismatch in column '{column}':")
            print(f"  Original: {df_o[column].dtype}")
            print(f"  Cleaned: {df[column].dtype}")


    df.to_csv("cleaned_population_data.csv", index=False)
    print("\nCleaned data saved to 'cleaned_population_data.csv'")

    df_encoded.to_csv("clean_encoded_data.csv", index=False)
    print("\nCleaned data saved to 'clean_encoded_data.csv'")

