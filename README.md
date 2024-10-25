# Data Cleaning Project: Population Dataset

## 1. Initial State Analysis

### Dataset Overview
- **Name**: messy_population_data.csv
- **Rows**: [125718]
- **Columns**: [5]

### Column Details
| Column Name | Data Type | Non-Null Count | Unique Values |  Mean  |
|-------------|-----------|----------------|---------------|--------|
| [Income_groups]| [Object] | [119412]   | [8]   | [-] |
| [age]| [float64] | [119495]   | [101]   | [50.007038] |
| [gender]| [float64] | [119811]   | [3]   | [1.578578] |
| [year]| [float64] | [119516]   | [169]   | [2025.068049] |
| [population]| [float64] | [119378]  | [114925] | [1.112983e+08] |


### Identified Issues

1. **[Handling Inconsistent Categories]**
   - Description: [Typos are inconsistent or incorrect entries in the dataset.]
   - Affected Column(s): [Income_groups]
   - Example: [low_income_typo,97.0,1.0,1991.0,583.0]
   - Potential Impact: [Typos can lead to misclassification, inaccurate grouping, and unreliable analysis results.]

2. **[Duplicates ]**
   - Description: [Some identical rows appear multiple times in the dataset.]
   - Affected Column(s): [income_graoups, age, gender, year, population]
   - Example: [upper_middle_income,85.0,1.0,1962.0,120531.0]
   - Potential Impact: [Duplicates may result in overestimation and inaccurate analysis outcomes.]

3. **[Incorrect Data Types]**
   - Description: [Some columns have incorrect data types, meaning the data stored in these columns does not match the expected format.]
   - Affected Column(s): [income_graoups, age, gender, year, population]
   - Example: [Columns like income_groups are stored as object data types, but they should be converted to the category type.]
   - Potential Impact: [Incorrect data types can lead to errors, unreliable analysis results.]

4.  **[Missing Values]**
   - Description: [There are missing values (null/nan) across all the columns, indicating that some data points are incomplete or not recorded.]
   - Affected Column(s): [income_graoups, age, gender, year, population]
   - Example: [,12.0,3.0,2032.0,nan]
   - Potential Impact: [Missing values may reduced the accuracy of summaries and cause bias in analysis.]

5. **[Outliers ]**
   - Description: [Some columns contain outliers—values that fall below Q1 - 1.5 * IQR or above Q3 + 1.5 * IQR. ]
   - Affected Column(s): [population]
   - Example: [high_income,,1.0,1995.0,6780019000.0]
   - Potential Impact: [Outliers could skew the results of analysis.]

6. **[Incorrect Values]**
   - Description: [Some columns contain incorrect or unexpected values.]
   - Affected Column(s): [Gender, population, year]
   - Example: [Gender values should be limited to 1 and 2, but a value 3 is present in the data.]
   - Potential Impact: [The presence of an unexpected gender value could skew analysis, misrepresent trends, introduce bias, and lead to inaccurate interpretations of population distributions and group comparisons.]

## 2. Data Cleaning Process

### Issue 1: [Handling Inconsistent Categories]
- **Cleaning Method**: [remove the typo part from values]
- **Implementation**:
  ```python
  def remove_typos(df):
    # Remove ' (_typo)' from category names
    df['income_groups'] = df['income_groups'].str.replace('_typo', '', regex=False)
    return df
  # 1. Handling Inconsistent Categories
  print("\n1. Handling Inconsistent Categories")
  print("Unique categories before cleaning:")
  print(df['income_groups'].value_counts())
  df = remove_typos(df)
  print("\nUnique categories after cleaning:")
  print(df['income_groups'].value_counts())
  print("Shape after removing typos:", df.shape)
  ```
- **Justification**: [Correcting typos ensures that data is accurate and consistent across the dataset. It prevents incorrect groupings, like high_income and high_income_typo being treated as different categories and allows for more reliable aggregations and comparisons. By removing the extra '_typo' part from the categories, we merge them into their correct groups.]
- **Impact**: 
  - Rows affected: [5836]
  - Data distribution change: [Before the typo removal, the income_groups column contained 8 categories due to duplicated entries with typos. After the correction, the number of categories was reduced to 4, merging the values under their correct categories.]


### Issue 2: [Duplicates]
- **Cleaning Method**: [Remove duplicates]
- **Implementation**:
  ```python
  def remove_duplicates(df):
    df = df.drop_duplicates()
    return df
  # 2. Handling Duplicates
  print("\n2. Handling Duplicates")
  print("Duplicate rows:", df.duplicated().sum())
  df = remove_duplicates(df)
  print("Shape after removing duplicates:", df.shape)
  ```
- **Justification**: [We need to remove duplicates to ensure that each row contributes uniquely to the analysis, preventing overestimation. Since there is no other reliable way to handle duplicate data, removal is necessary to maintain the integrity and accuracy of the results.]
- **Impact**: 
  - Rows affected: [2950]
  - Data distribution change: [After removing 2950 duplicate rows, the overall dataset size was reduced, ensuring that each record contributes only once to the analysis.]


### Issue 3: [Incorrect Data Types]
- **Cleaning Method**: [Convert the data types to the correct data types.]
- **Implementation**:
  ```python
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

  # 3. Data Type Conversions
  print("\n3. Data Type Conversions")
  print("Data types before:")
  print(df.dtypes)
  df= convert_types(df)
  print("\nData types after:")
  print(df.dtypes)
  ```
- **Justification**: [We converted the income_groups column to category and the remaining columns to integer. We converted the income_groups column to category since it clearly represents discrete, non-numeric categories. However, we did not convert the gender column to category because we are uncertain about the precise meaning of the numeric values 1 and 2. Without a clear definition of these values, treating them as integers ensures we retain the original information without making incorrect assumptions about their categorical nature. We converted the remaining variables to integer because keeping them as float was not appropriate, as they are meant to represent whole numbers (e.g., age, year, population).Ensuring columns have the correct data types enables more accurate operations and improves performance. It also helps avoid potential errors during analysis or modeling by maintaining consistency in numerical calculations and proper handling of categorical data.]
- **Impact**: 
  - Rows affected: [every rows]
  - Data distribution change: [The data values in each column remained unchanged after the type conversion. However, numeric values were converted to integers, removing any decimal points to ensure consistency in calculations and representation.]




### Issue 4: [Missing Values]
- **Cleaning Method**: [We handled missing values differently across variables]
- **Implementation**:
  ```python
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
  # 4. Handling Missing Values
  def plot_boxplot(df, column, filename=None):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df[column])
    plt.title(f'Boxplot of {column}')
    if JUPYTER:
      plt.show()
    else:
      plt.savefig(filename)
      plt.close()
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
  ```
- **Justification**: [We first identified missing values by using a custom function, find_missing_data_index(df), which allowed us to locate and index missing entries. Handling Missing Values in income_groups:
From the original dataset, we observed that for identical combinations of gender, age, and year, there should be exactly four rows, each corresponding to a distinct income group. When a missing income group was detected, we filled it only if three other rows with the same gender, age, and year were present, ensuring that we knew the correct missing group. Handling Missing Values in gender: A similar logic was applied for gender. For each unique combination of income group, age, and year, there should be two genders (1 and 2). If only one gender was present, and the missing value was marked as nan or 3 (an invalid entry), we filled it with the expected missing gender. However, this approach carries a small risk of misclassification. In some cases, a row with gender 3 or nan could be a duplicate of an existing row with gender 1 or 2, rather than the truly missing counterpart. Rather than overcomplicating the solution with a complex algorithm to handle all edge cases, we opted for a simple, practical approach to recover most missing values efficiently. A few incorrect gender classifications will have minimal impact on the overall trends.Outlier detection will be applied later to remove obviously incorrect values, further ensuring the dataset's accuracy. Handling Missing Values in population: For the population variable, we applied a forward fill method. At the end, for all thwe dropped all rows with null values and removed rows with gender 3 to ensure data consistency.]
- **Impact**: 
  - Rows affected: [16811]
  - Data distribution change: [In total, 16,811 rows were removed.]



### Issue 5: [Outliers]
- **Cleaning Method**: [Remove outliers]
- **Implementation**:
  ```python
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
  ```
- **Justification**: [Outliers can skew summary statistics and mislead results, making trends appear unreliable. Removing them ensures the analysis is more accurate and meaningful, free from distractions caused by extreme values.]
- **Impact**: 
  - Rows affected: [2006]
  - Data distribution change: [From the box plot, we can observe the changes.]


### Issue 6: [Incorrect Values]
- **Cleaning Method**: [drop the incorrect year]
- **Implementation**:
  ```python
    # 6. Handling Incorrect Values
    print("\n6. Handling Incorrect Values")
    print("Year before cleaning:")
    print(df['year'].value_counts())
    # Filter the data to include only reasonable years (e.g., 1950-2100)
    df = df[(df['year'] >= 1950) & (df['year'] <= 2100)]
    print("\nYear after cleaning:")
    print(df['year'].value_counts())
  ```
- **Justification**: [We know from the original clean dataset that the year values range from 1950 to 2100, so any values outside this range should be dropped to maintain data consistency.]
- **Impact**: 
  - Rows affected: [18]
  - Data distribution change: [Removed the year values that fall outside the range of 1950 to 2100.]


## 3. Final State Analysis

### Dataset Overview
- **Name**: clean_data.csv
- **Rows**: [103641]
- **Columns**: [7]

### Column Details
| Column Name | Data Type | Non-Null Count | #Unique Values |  Mean  |
|-------------|-----------|----------------|----------------|--------|
| [Income_groups]| [category] | 103641   | [4]   | [-] |
| [age]| [int64] | [103641]   | [101]   | [50.102421] |
| [gender]| [int64] | [103641]   | [2]   | [-] |
| [year]| [int64] | [103641]   | [151]   | [2024.949537] |
| [population]| [int64] | [103641]  | [98179] | [111298303.15437518] |



### Summary of Changes
- [major changes made to the dataset]

- [Handling Inconsistent Categories:
Removed typos from the income_groups column, reducing the categories from 8 to 4.
Handling Duplicates:
Removed 2,950 duplicate rows to ensure each record is unique and prevent overestimation.
Incorrect Data Types:
Converted income_groups to category and other numeric columns (age, year, population) to integers, improving consistency and performance.
Handling Missing Values:
Filled missing income_groups and gender values using logical inference, forward-filled population, and removed rows with invalid data, affecting 16,811 rows.
Handling Outliers:
Removed 2,006 outliers from the population column to ensure meaningful trends in analysis.
Incorrect Values:
Removed 18 rows with year values outside the valid range (1950-2100) to maintain data consistency.]

- [Describe your cleaned dataset and how it compares to the original dirty one.]

[The original dirty dataset had 125,718 rows, while the cleaned dataset contains 103,641 rows. Several data type changes were made: income_groups was converted from object to category, and year, age, gender, and population were converted from float64 to int64 to ensure consistency and better representation of whole numbers.]

- [Discuss any challenges faced and how you overcame them.]

[The biggest challenge for me was finding the correct way to handle missing data. I was concerned that my algorithm might not be accurate enough, potentially introducing more bias. To overcome this, I applied different strategies for different variables. While I dropped most of the missing data to ensure consistency, I also made a focused effort to restore as much of the missing information as possible.]

- [Reflect on what you learned from this process.]

[I learned a lot about using pandas and numpy. I realized how time-consuming data cleaning can be and how important it is to preserve as much of the dataset as possible without introducing bias. While there are many algorithms for data cleaning, finding the one that fits a specific dataset is also crucial. Coming up with an effective and unbiased approach is definitely challenging.]

- [Suggest potential next steps or further improvements.]

[we could look at bias detection. Handling missing values during data cleaning can introduce bias, potentially skewing results and misrepresenting trends. It's important to assess how cleaning methods affect the dataset by comparing distributions and checking if specific groups are disproportionately impacted. To mitigate bias, multiple imputation techniques can be tested, assumptions carefully reviewed, and methods aligned with the dataset’s context and analysis goals.]