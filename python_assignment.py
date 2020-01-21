# import pandas, numpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from datetime import date
from collections import Counter
from scipy.stats import norm 
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler

#from tigerml.eda import Analyser

# Create the required data frames by reading in the files
df=pd.read_excel('SaleData.xlsx')
df1=pd.read_csv("imdb.csv",escapechar='\\')
df2=pd.read_csv('diamonds.csv')
df3=pd.read_csv('movie_metadata.csv')


# Q1 Find least sales amount for each item
# has been solved as an example
def least_sales(df):
    # write code to return pandas dataframe
    ls = df.groupby(["Item"])["Sale_amt"].min().reset_index()
    return ls

# Q2 compute total sales at each year X region   
def sales_year_region(df):   
    # write code to return pandas dataframe
    df['year'] = df.OrderDate.apply(lambda x: x.strftime('%Y'))
    total_sales = df.groupby(['year','Region'])["Sale_amt"].sum().reset_index()
    return total_sales

# Q3 append column with no of days difference from present date to each order date
def days_diff(df):
    # write code to return pandas dataframe
    today = date.today()
    today = pd.to_datetime(today)
    df['days_diff'] = today- df['OrderDate']
    return df 

# Q4 get dataframe with manager as first column and  salesman under them as lists in rows in second column.
def mgr_slsmn(df):
    # write code to return pandas dataframe
    list_of_salesmen=df.groupby(['Manager'])['SalesMan'].unique().reset_index()
    list_of_salesmen.rename(columns={'SalesMan':'list_of_salesmen'}, inplace=True)
    return list_of_salesmen

# Q5 For all regions find number of salesman and number of units
def slsmn_units(df):
    # write code to return pandas dataframe
    no_units=df.groupby('Region')['Units'].sum().reset_index()
    no_salesmen=df.groupby('Region')['SalesMan'].nunique().reset_index()
    new_df=pd.merge(no_salesmen,no_units,how='inner',on='Region')
    new_df.rename(columns={'SalesMan':'salesmen_count','Units' : 'total_sales'}, inplace=True)
    return new_df


# Q6 Find total sales as percentage for each manager
def sales_pct(df):
    # write code to return pandas dataframe
    mgr_sale=df.groupby('Manager')['Sale_amt'].sum().reset_index()
    total_sale_amt=mgr_sale['Sale_amt'].sum()
    mgr_sale['percent_sales ']=(mgr_sale['Sale_amt']/total_sale_amt)*100
    mgr_sale=mgr_sale.drop(['Sale_amt'],axis=1)
    return mgr_sale
    

# Q7 get imdb rating for fifth movie of dataframe
def fifth_movie(df):
	# write code here
    pos=df.iloc[4]['imdbRating']
    return pos

# Q8 return titles of movies with shortest and longest run time
def movies(df):
	# write code here
    print ('longest run time movie: ')
    print(df[df['duration']==df['duration'].max()]['title'])
    
    print ('shortest run time movie: ')
    print(df[df['duration']==df['duration'].min()]['title'])
    
    
# Q9 sort by two columns - release_date (earliest) and Imdb rating(highest to lowest)
def sort_df(df):
	# write code here
    sorted_dataframe=df.sort_values(['year','imdbRating'],ascending=[True,False])
    return sorted_dataframe
    
# Q10 subset revenue more than 2 million and spent less than 1 million & duration between 30 mintues to 180 minutes
def subset_df(df):
    
	# write code here
    result = df[(df['gross'] > 20000000) & (df['budget'] < 10000000) & (df['duration'] >= 30) & (df['duration'] <= 180)]
    return result

# Q11 count the duplicate rows of diamonds DataFrame.
def dupl_rows(df):
	# write code here
    result1=len(df)-len(df.drop_duplicates())
    return result1

# Q12 droping those rows where any value in a row is missing in carat and cut columns
def drop_row(df):
	# write code here
    result2 = df[pd.notnull(df['carat']) & pd.notnull(df['cut'])]
    return result2
    
# Q13 subset only numeric columns
def sub_numeric(df):
	# write code here 
    result3 =df._get_numeric_data()
    return result3

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

#bonus questions

#bonus Q1
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

def bonus1(df):
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
        
#bonus Q2
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

def bonus2(df):
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
    
# bonus Q3
def bonus3(df):
    df['bin'] = pd.qcut(df['volume'], q=6)
    updated_df=np.array(df['bin'].value_counts())
    cross_tab=pd.crosstab(df.bin,df.cut)
    i=0
    res=pd.DataFrame()
    for i in range(len(updated_df)):
        res[i]=(cross_tab.loc[i]/updated_df[i])*100
    res=res.transpose()
    print(res)
      
# bonus Q4
def bonus4(df):
    meta_movie=df.sort_values(by=['title_year','gross'],ascending=False)
    new_df=meta_movie.groupby("title_year").agg({'title_year':'count'})
    new_df.columns=['count']
    new_df=new_df.sort_values(by=['title_year'],ascending=False)
    num = 10
    i=0
    j=0
    result=pd.DataFrame()
    for i in range(0,num):
        data_fr=pd.DataFrame()
        meta_movie_1=meta_movie.iloc[j:j+int(new_df.iloc[i])]
        data_fr['year']=meta_movie_1.head(int(new_df.iloc[i]*(num/100)))['title_year']
        data_fr['movie_name']=meta_movie_1.head(int(new_df.iloc[i]*(num/100)))['movie_title']
        data_fr['genres']=meta_movie_1.head(int(new_df.iloc[i]*(num/100)))['genres']
        data_fr['gross']=meta_movie_1.head(int(new_df.iloc[i]*(num/100)))['gross']
        j=j+int(new_df.iloc[i])
        result=pd.concat([result,data_fr])   
    print(result)
        

#bonus Q5
def bonus5(df):
    df['decile']=pd.qcut(df["duration"], 10, labels=False)
    genre_sum=df.groupby('decile').agg([np.sum])
    genre_sum=genre_sum.loc[:,"Action":]
    i=0.0
    lt=[]
    for j in range(0,10):
        genre_sum1=genre_sum.sort_values(by=i,axis=1, ascending=False)
        genre_sum1.columns = genre_sum1.columns.map('_'.join)
        st=list(genre_sum1.columns[:3])
        lt.append(st)
        i+=1

    df1=pd.Series(lt)
    df2=df.groupby('decile').agg({'nrOfNominations':'sum','nrOfWins':'sum','imdbRating':'count'}).rename(columns={'nrOfNominations':'nomination','nrOfWins':'wins','imdbRating':'count'})
    df2['top_3_geners']=df1
    print(df2)



