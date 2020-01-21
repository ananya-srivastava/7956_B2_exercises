# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# import pandas, numpy
import numpy as np
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import itertools
from collections import Counter


#For question 1 to 6
df=pd.read_excel('SaleData.xlsx')

# Q1 Find least sales amount for each item
# has been solved as an example
def least_sales(df):
    # write code to return pandas dataframe
    ls = df.groupby(["Item"])["Sale_amt"].min().reset_index()
    return ls

# Q2 compute total sales at each year X region   
def sales_year_region(df):   
    # write code to return pandas dataframe
    df['Year'] = df['OrderDate'].apply(lambda time:time.year)
    ls1 = df.groupby(by=['Year','Region'])['Sale_amt'].sum().reset_index()
    return ls1

# Q3 append column with no of days difference from present date to each order date
def days_diff(df):
    # write code to return pandas dataframe
    today = date.today()
    today = pd.to_datetime(today)
    df['days_diff'] = today- df['OrderDate']
    return(df)

# Q4 get dataframe with manager as first column and  salesman under them as lists in rows in second column.
def mgr_slsmn(df):
    # write code to return pandas dataframe
    ls3=df.groupby(['Manager'])['SalesMan'].unique().reset_index()
    ls3=ls3.rename(columns={'SalesMan':'list_of_salesmen'})
    return ls3


# Q5 For all regions find number of salesman and number of units
def slsmn_units(df):
    # write code to return pandas dataframe
    unit=df.groupby('Region')['Units'].sum().reset_index()
    salesman=df.groupby('Region')['SalesMan'].nunique().reset_index()
    updated_df=pd.merge(unit,salesman,how='inner',on='Region')
    updated_df.rename(columns={'Units' : 'total_sales','SalesMan':'salesmen_count'}, inplace=True)
    return updated_df
 

# Q6 Find total sales as percentage for each manager
   
def sales_pct(df):
    data_frame=pd.DataFrame( {'manager':df['Manager'], 'percent_sales':df['Units']})
    data_frame=data_frame.groupby('manager')['percent_sales'].apply(sum).reset_index()
    data_frame['percent_sales']= data_frame['percent_sales'] * 100/ (data_frame['percent_sales'].sum())
    return data_frame

#For question-7 to 10
df2=pd.read_csv("imdb.csv",escapechar='\\')
# Q7 get imdb rating for fifth movie of dataframe
def fifth_movie(df):
    return(df['imdbRating'][4])

# Q8 return titles of movies with shortest and longest run time

def movies(df):
    print('max_length',end=" ")
    print(df[df['duration']==df['duration'].max()]['title'])
    print('min_length',end=" ")
    print(df[df['duration']==df['duration'].min()]['title'])

# Q9 sort by two columns - release_date (earliest) and Imdb rating(highest to lowest)
def sort_df(df):
	# write code here
    
    ls=df.sort_values(['year','imdbRating'],ascending=[True,False])
    return ls
 
# Q10 subset revenue more than 2 million and spent less than 1 million & duration between 30 mintues to 180 minutes
df3=pd.read_csv('movie_metadata.csv')
def subset_df(df):
    
	# write code here
    result = df[(df['gross'] > 20000000) & (df['budget'] < 10000000) & (df['duration'] >= 30) & (df['duration'] <= 180)]
    return result

#For question 11 to 15
df4= pd.read_csv('diamonds.csv')
# Q11 count the duplicate rows of diamonds DataFrame.
def dupl_rows(df):
	# write code here
    result=len(df)-len(df.drop_duplicates())
    return result

# Q12 droping those rows where any value in a row is missing in carat and cut columns
def drop_row(df):
	# write code here
    df = df[pd.notnull(df['carat']) & pd.notnull(df['cut'])]
    return df


# Q13 subset only numeric columns
def sub_numeric(df):
	# write code here 
    t=df._get_numeric_data()
    return t

# Q14 compute volume as (x*y*z) when depth > 60 else 8
def volume(df):
	# write code here
    df['z'] = pd.to_numeric(df.z, errors='coerce')
    df['volume']= (df['x']*df['y']*df['z']).where(df['depth'] > 60, 8)
    return df
   

# Q15 impute missing price values with mean
def impute(df):
	# write code here
    df['price'].fillna((df['price'].mean()), inplace=True)
    return df

#Bonus Questions
    
#Q1 Generate a report that tracks the various Genere combinations for each type year on year. The result data frame should contain type, Genere_combo, year, avg_rating, min_rating, max_rating, total_run_time_mins

def get_key(my_dict):
    genre_dict={}
    for key,value in my_dict.items():
        s=[]
        for i,j in value.items():
            if(j>0):
                #print(i[0],end=" ")
                s.append(i[0])
        genre_dict[key]=s
    return genre_dict

def bonus_question1(df):
    grouped=df.groupby(['type','year']).agg([np.sum])
    grouped1=grouped.loc[:,"Action":]
    grouped1_transpose=grouped1.transpose()
    grouped_dict=grouped1_transpose.to_dict()
    genre_dict=get_key(grouped_dict)
    s = pd.Series(genre_dict)
    movie_stats = df.groupby(['type','year']).agg({'imdbRating': [min,max, np.mean],'duration':(sum)})
    movie_stats['Genre_combo']= s
    movie_stats['duration']=movie_stats['duration']/60
    movie_stats=movie_stats.rename(columns={"min": "min_rating", "max": "max_rating","mean":"avg_rating","duration": "total_run_time_mins","sum":"","imdbRating":"Rating"})
    print(movie_stats)
    

#Q2 
def cal_percentie(x):
    lis=[]
    a=np.percentile(x,25)
    b=np.percentile(x,50)
    c=np.percentile(x,75)
    lis.append(a)
    lis.append(b)
    lis.append(c)
    return lis


def count_numVideos_dict(x,y):
    d={}
    for key,value in y.items():
        l2=[]
        count1=count2=count3=count4=0
        for i in range(0,len(value)):
            if(value[i]<x[key][0]):
                count1+=1
            elif(x[key][0]<=value[i]<x[key][1]):
                count2+=1
            elif(x[key][1]<=value[i]<=x[key][2]):
                count3+=1
            else:
                count4+=1
        l2.append(count1)
        l2.append(count2)
        l2.append(count3)
        l2.append(count4)
        d[key]=l2
    return d

def bonus_question2(df):
    df['title_length']=df['wordsInTitle'].str.len()
    print('correlation',end=" ")
    print((df['title_length']).corr(df['imdbRating']))
    print()
    plt.scatter(df['title_length'],df['imdbRating'], color= "green", marker= ".")
    quantile_df=pd.DataFrame()
    quantile_df=df[['year', 'title_length']].groupby('year').quantile().reset_index().rename(columns={"title_length": "quantile"})

    len_df=df.groupby("year").agg({'title_length': [min,max]}).rename(columns={"min": "min_length","max":"max_length"})
    len_df['quantile']=quantile_df['quantile']
    len_df.columns=['min_length','max_length','quantile']
    print("crosstab")
    print(pd.crosstab(quantile_df['year'],quantile_df['quantile']))
    percentile_df=(df.groupby(['year'])['title_length'].apply(lambda x: cal_percentie(x)))
    percentile_df_dict=dict(percentile_df)

    var_1=df.groupby(['year'])['title_length'].apply(lambda x:list(x))
    var_1_dict=dict(var_1)
    d2=count_numVideos_dict(percentile_df_dict,var_1_dict)
    s1=pd.DataFrame(d2)
    s1_transpose=s1.transpose()
    s1_transpose.columns =['num_videos_less_than25Percentile','num_videos_25_50Percentile','num_videos_50_75Percentile','num_videos_greaterthan75Precentile']
    df_all_cols_2 = pd.concat([len_df,s1_transpose], axis = 1)
    print(df_all_cols_2)
   
#Q3
def bonus_question3(df):
    df['bin'] = pd.qcut(df['volume'], q=6)
    df_updated=np.array(df['bin'].value_counts())
    cross_tab=pd.crosstab(df.bin,df.cut)
    i=0
    result=pd.DataFrame()
    for i in range(len(df_updated)):
        result[i]=(cross_tab.loc[i]/df_updated[i])*100
    result=result.transpose()
    print(result)
      
#Q4
def bonus_question4(df):
    sorted_meta_movie=df.sort_values(by=['title_year','gross'],ascending=False)
    count_data=sorted_meta_movie.groupby("title_year").agg({'title_year':'count'})
    count_data.columns=['count']
    count_data=count_data.sort_values(by=['title_year'],ascending=False)
    num = 10
    i=0
    j=0
    result=pd.DataFrame()
    for i in range(0,num):
        data_frame=pd.DataFrame()
        sliced_data=sorted_meta_movie.iloc[j:j+int(count_data.iloc[i])]
        data_frame['year']=sliced_data.head(int(count_data.iloc[i]*(num/100)))['title_year']
        data_frame['movie_name']=sliced_data.head(int(count_data.iloc[i]*(num/100)))['movie_title']
        data_frame['genres']=sliced_data.head(int(count_data.iloc[i]*(num/100)))['genres']
        data_frame['gross']=sliced_data.head(int(count_data.iloc[i]*(num/100)))['gross']
        j=j+int(count_data.iloc[i])
        result=pd.concat([result,data_frame])   
    print(result)
        

#Q5
def bonus_question5(df):
    df['decile']=pd.qcut(df["duration"], 10, labels=False)
    genre_data=df.groupby('decile').agg([np.sum])
    genre_data=genre_data.loc[:,"Action":]
    genre_data.columns = genre_data.columns.droplevel(1)
    i=0.0
    list_1=[]
    for j in range(0,10):
        genre_sorted_data=genre_data.sort_values(by=i,axis=1, ascending=False)
        genre_combo=list(genre_sorted_data.columns[1:4])
        list_1.append(genre_combo)
        i+=1
    
    genre_list=pd.Series(list_1)
    result=df.groupby('decile').agg({'nrOfNominations':'sum','nrOfWins':'sum','imdbRating':'count'}).rename(columns={'nrOfNominations':'nomination','nrOfWins':'wins','imdbRating':'count'})
    result['top_3_geners']=genre_list
    print(result)



