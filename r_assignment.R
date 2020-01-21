library(readxl)
library(dplyr)
excel_sheets("SaleData.xlsx")
df <- read_excel("SaleData.xlsx", sheet = "Sales Data")
diamond<-read.csv("diamonds.csv")
movie<-read.csv('movie_metadata.csv')
imdb<-read.csv('imdb.csv',header = T)
#Question-1
library(readxl)
library(dplyr)
#library(plyr)

ans1 <- df %>% group_by(Item) %>% summarise(min_sales = min(Sale_amt))
print(ans1)

# Question-2
ans2 <- df %>% group_by(format(as.Date(OrderDate,format="%Y-%m-%d"),"%Y"),Region) %>% summarise(total_sales = sum(Sale_amt))
print(ans2)

#Question-3
df$days_diff <- Sys.Date()- as.Date(df$OrderDate,format="%Y-%m-%d")
print(head(df))

#Question-4
data_1 <- data.frame(manager=df$Manager,list_of_salesmen=df$SalesMan)
ans4 <- data_1 %>% group_by(manager) %>% summarise(list_of_salesmen = paste(unique(list_of_salesmen),collapse = ","))
print(ans4)

#Question-5
data_2 <- data.frame(Region=df$Region,Salesmen_count=df$SalesMan, total_sales=df$Sale_amt)
data_3 <- data_2 %>% group_by(Region) %>%  summarise(total_sales= sum(total_sales))
data_4 <- data_2 %>% group_by(Region) %>% count(Salesmen_count) %>% count(Region)
ans5 <- data.frame(data_3,Salesmen_count=data_4$n)
print(ans5)

#Question-6
data_6 <- data.frame(Manager=df$Manager, Total_sale=df$Sale_amt)
total_sale_amount= sum(df$Sale_amt)
ans6 <- data_6 %>% group_by(Manager) %>% summarise(percent_sales= sum(Total_sale)*100/total_sale_amount)
print(ans6)

#Question-7

ans7<-imdb[5,6]
print(ans7)


#Question-8

ans8<-function(df){
  i<-2
  while(i<=14762){
    #print(i)
    if(!is.na(df[i,45])){
      #print(i)
      df<-df[-c(i),]
    }
    i=i+1
  }
  max_<-which.max(df$duration)
  min_<-which.min(df$duration)
  r_1<-as.numeric(max_)
  r_2<-as.numeric(min_)
  df$duration<-as.numeric(as.character(df$duration))
  print("title:")
  print(df[r_1,3])
  print("duration:")
  print(df[r_1,8])
  print("title:")
  print(df[r_2,3])
  print("duration:")
  print(df[r_2,8])
}
ans8(imdb)

#Question-9
ans9<-function(df){
  j<-2
  while(j<=14762){
    #print(i)
    if(!is.na(df[j,45])){
      #print(i)
      df<-df[-c(j),]
    }
    j=j+1
  }
  df$imdbRating<-as.numeric(as.character(df$imdbRating))
  df2 <-df[order(df$year,-df$imdbRating),]
  return(df2)
}
ans9(imdb)

#Question-10
ans10<-function(df){
  new_data <- subset(df, gross>2000000)
  new_data1 <- subset(new_data, budget<1000000)
  new_data2 <- subset(new_data1, duration >= 30 & duration < 180)
  return(new_data2)
}
ans10(movie)



#Question-11
ans11<-function(df){
  row_<-(nrow(df)-nrow(distinct(df)))
  return(row_)
}
ans11(diamond)

#Question-12
ans12<-function(df){
  df <- df[-which(df$carat == ""), ]
  df <- df[-which(df$cut == ""), ]
  return(df)
}
ans12(diamond)

#Question-13
ans13<-function(df){
  r<-select_if(df,is.numeric)
  return(r)
}
ans13(diamond)

diamond$z<-as.numeric(as.character(diamond$z))
cbind(diamond,volume=0)

#Question-14

ans14<-function(df){
  i<-1
  while(i<=53943)
  {
    if(df[i,5]>60){
      df[i,"volume"]<-df[i,8]*df[i,9]*df[i,10]
    } else{
      df[i,"volume"]<-8
    }
    i=i+1
  }
  return(df)
}
ans14(diamond)

#Question-15
ans15<-function(df){
  i<-1
  df[is.na(df)]<-0
  mean_<-mean(df$price)
  while(i<=53943){
    if((df[i,7])==0){
      df[i,7]<-mean_
    }
    i=i+1
  }
  return(df)
}
ans15(diamond)

