# -*- coding: utf-8 -*-
"""

@author: Samip
"""

"""It gives recommendation of your favorite Anime based on anime you selected. 
The recommendation is done based on total rating counts, average rating counts, genre and finally the genre of selected Anime.
More the value of corellation, more chances of getting them as recommendation."""

#Import lbraries
import pandas as pd

#Get data 
df=pd.read_csv('rating.csv')
anime=pd.read_csv('anime.csv')

#Merge two data to one
df=pd.merge(df,anime.drop('rating',axis=1),on='anime_id')

#Create rating data frame with average and total ratings 
ratings = pd.DataFrame(df.groupby('name')['rating'].mean())
ratings['num of ratings'] = pd.DataFrame(df.groupby('name')['rating'].count())

#Create a dictionary of name of movie and genre
genre_dict = pd.DataFrame(data=anime[['name','genre']])
genre_dict.set_index('name',inplace=True)

#Check for Genre
def check_genre(genre_list,string):
    if any(x in string for x in genre_list):
        return True
    else:
        return False

#Main function to get recommendation
def get_recommendation(name, min):
    anime_genre=genre_dict.loc[name].values[0].split(',') #Get genre
    cols=anime[anime['genre'].apply(lambda x:check_genre(anime_genre,str(x)))]['name'].tolist()     #Convert into cols list
    animemat=df[df['name'].isin(cols)].pivot_table(index='user_id',columns='name',values='rating')    #Check name and corresponding values from dataframe
    anime_user_rating=animemat[name]    #Get values of input name
    similar_anime=animemat.corrwith(anime_user_rating)    #Find correlation matrix
    corr_anime=pd.DataFrame(similar_anime,columns=['correlation'])   #Store the correlation values in a dataframe
    corr_anime=corr_anime.join(ratings['num of ratings'])    #Join by the number of ratings column
    corr_anime.dropna(inplace=True)
    corr_anime = corr_anime[corr_anime['num of ratings'] > min].sort_values(
        'correlation',ascending=False)   #Store the recommended anime 
    return corr_anime   #Return recommended animes
    
inp = input("Enter the name of Anime: ")
count = int(input("Enter number of recommendations: "))
min_ratings = int(input("Enter the number of ratings to be considered: "))
print('Top',  str(count),  'recommendation of', inp,  'are: ')
try:
    res = get_recommendation(inp, min_ratings)
    if res.isnull:
        print("No recommendation found")
    else:
        print(res.head(count))
except KeyError:
    print("Anime not found")