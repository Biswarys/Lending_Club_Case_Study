#!/usr/bin/env python
# coding: utf-8

# # Lending Club Case Study

# In[10]:


#Import Necessary Libraries


# In[177]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 


# In[178]:


#Read the Excel file and store in a dataframe
##Got DTypeWarning error while reading CSV. Hence set the low memory as False.
##The reason we get this low_memory warning is because guessing dtypes for each column is very memory demanding. Pandas tries to determine what dtype to set by analyzing the data in each column.


# In[179]:


df = pd.read_csv(r'C:\Users\ASUS\Documents\AI ML\Lending Club\loan.csv', low_memory=False)


# In[180]:


#Output the top five columns of DataFrame


# In[181]:


df.head()


# In[182]:


#Check for Null Values in DataFrame


# In[183]:


df.isnull().sum()


# In[184]:


#Create a copy of the DataFrame so as not to affect the original


# In[187]:


df2 = df.copy()


# In[188]:


#Remove all the columns which have ALL Null Values


# In[189]:


df2 = df1.dropna(axis=1,how='all')


# In[190]:


#Check the null value sum now


# In[191]:


df2.isnull().sum()


# In[192]:


#Clean up columns with NULL values


# In[193]:


#Replace emp_title Null values with ABCDEF(dummy company)


# In[194]:


df2['emp_title'] = df2['emp_title'].fillna('ABCDEF')


# In[195]:


df2['emp_title']


# In[196]:


#Replace emp_length Null values with 0 Years


# In[197]:


df2['emp_length'] = df2.loc[:,'emp_length'].fillna(0)


# In[198]:


df2['emp_length'].isnull().sum()


# In[199]:


#Clean emp_length column to make it complete integer value i.e. Extract Integer values from Strings


# In[201]:


df2['emp_length'] = df2.emp_length.str.extract('(\d+)')


# In[202]:


df2['emp_length']


# In[203]:


#Fill mths_since_last_delinq NA values as 0 months


# In[204]:


df2['mths_since_last_delinq'] = df2['mths_since_last_delinq'].fillna(0)
df2['mths_since_last_delinq'] = df2['mths_since_last_delinq'].astype('int')


# In[205]:


df2['mths_since_last_delinq']


# In[206]:


#Fill mths_since_last_record NA values as 0 months 


# In[207]:


df2['mths_since_last_record'] = df2['mths_since_last_record'].fillna(0)
df2['mths_since_last_record'] = df2['mths_since_last_record']


# In[208]:


#Dropping all below mentioned columns which are unrequired in my opinion
#mths_since_last_record, pub_rec, initial_list_status, next_pymnt_d, collections_12_mths_ex_med, policy_code, application_type


# In[209]:


df2 = df2.drop(['mths_since_last_record', 'pub_rec', 'initial_list_status', 'next_pymnt_d', 'collections_12_mths_ex_med', 'policy_code', 'application_type'], axis=1)


# In[210]:


df2.isnull().sum()


# In[211]:


#Data has been Cleaned


# In[212]:


#To identify Risky borrowers, below factors can be applied
#1. If Source of borrower is not verified, then its risky
#2. If home of borrower is already in mortgage, then its a risk factor
#3. Ratio of salary vs loan disbursed should be less. So higher the percentage of loan amount compared to salary greater the risk
#4. Borrowers tagged as "Charged Off" are risks


# In[213]:


#1. If Source of borrower is not verified, then its risky


# In[214]:


df['unverified'] = df['verification_status'] == 'Not Verified'


# In[215]:


df_unverified = df[df['unverified']]


# In[216]:


#List of unverified IDs


# In[217]:


df_unverified


# In[218]:


#16921 borrowers are Unverified and so at risk
#Lets plot a pie chart of the Unverified borrowers


# In[238]:


df2.verification_status.value_counts().plot(kind='pie',autopct='%1.1f%%',shadow= True)
plt.axis('equal')
plt.title('Unverified Borrowers')


# In[232]:


#2. If home of borrower is already in mortgage, then its a risk factor


# In[251]:


df2['mortgage'] = df2['home_ownership'] == 'MORTGAGE'
df2[df2['mortgage']]


# In[ ]:


#17659 borrowers are under Mortgage


# In[252]:


#Piechart depicting percentage of borrowers in mortgage


# In[253]:


df2.home_ownership.value_counts().plot(kind='pie',autopct='%1.1f%%',shadow = True)
plt.axis('equal')
plt.title('Home Under Mortgage')


# In[254]:


#3. Ratio of salary vs loan disbursed should be less. So higher the percentage of loan amount compared to salary greater the risk


# In[344]:


df2['Salary Vs Loan'] = (df2['funded_amnt']/df2['annual_inc'])*100


# In[345]:


df2_Risk_Based_On_Salary = df2.sort_values(by=['Salary Vs Loan'], ascending = False)


# In[ ]:


#Top 10 risky borrowers based on loan payback capacity


# In[346]:


df2_Risk_Based_On_Salary.head(10)


# In[263]:


#Scatter Plot depicting how much risk based on funded amount


# In[347]:


sns.scatterplot(data=df2_Risk_Based_On_Salary, x= 'funded_amnt', y = 'Salary Vs Loan', hue = 'Salary Vs Loan')


# In[269]:


#4. Borrowers tagged as "Charged Off" are risks


# In[271]:


df2_ChargedOff = df2['loan_status'] == 'Charged Off'
df2[df2_ChargedOff]


# In[ ]:


#5627 are charged Off


# In[272]:


#PieChart depicting percentage of people Charged Off


# In[273]:


df2.loan_status.value_counts().plot(kind='pie',autopct='%1.1f%%',shadow = True)
plt.axis('equal')
plt.title('Charged Off Borrowers')


# In[ ]:


#Now we can find the most at risk borrowers by combining the above 4 points


# In[306]:


df3 = df2.copy()


# In[318]:


df4 = df3[(df3['verification_status'] == 'Not Verified')]


# In[322]:


df5 = df4['mortgage']


# In[330]:


df6 = df4[df5]
df6


# In[336]:


df7 = df6['loan_status'] == 'Charged Off'


# In[338]:


df_riskiest = df6[df7]
df_riskiest


# In[335]:


#836 are HIGH RISK borrowers and should be scrutinised


# In[339]:


df_riskiest.to_excel('Risky Borrowers.xlsx', index=False)


# In[340]:


#Check the top 10 highest funded amount of the riskiest borrowers


# In[343]:


df_riskiest.sort_values(by = 'funded_amnt', ascending = False).head(10)


# In[ ]:




