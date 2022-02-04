import csv
import pandas as pd

# step 1: read the csv file
## open the csv file, which is in the same directory as this script, for reading
csvFileDisneyplus = open('disney_plus_titles.csv')
## create a csv reader object
dfDisneyplus = pd.read_csv(csvFileDisneyplus)
## close the csv file
csvFileDisneyplus.close()

# step 2: create a list of all genre names
## of each title get the entries of the genre column as a list
genrenamesListed = dfDisneyplus.get('listed_in').str.split(pat=', ')
## create an empty list
genrenames = []
## first, iterate over the DataFrame of each title
for genrenamesListedItems in genrenamesListed:
    ## then, iterate over the list of genre names of the current title
    for genrename in genrenamesListedItems:
        ## finally, add the genre name to the list
        genrenames.append(genrename)

# step 3: count distinct genre names
## create a DataFrame from the list
dfGenrenames = pd.DataFrame(genrenames, columns=['Genre Name'])
## to count the distinct genre names, we need to create a list of unique genre names
genrenamesAggregated = dfGenrenames.get('Genre Name').unique()
## print the number of distinct genre names
print('Number of distinct genre names: ' + str(len(genrenamesAggregated)))

# step 4: count the number of titles in each genre
## create a dictionary to store the genre names and their counts
moviesInGenre = {}
## iterate over the DataFrame of aggregated genre names
for genrename in genrenamesAggregated:
    ## count the number of titles in the current genre
    moviesInGenre[genrename] = dfDisneyplus.loc[dfDisneyplus['listed_in'].str.contains(genrename), 'title'].count()

# step 5: write result to csv file
## open the csv file for writing and truncate it or create it if it doesn't exist
csvFileResultStep5 = open('exercise1_result_step5.csv', 'w+')
## create a csv writer object
csvWriter = csv.writer(csvFileResultStep5)
## write the header
csvWriter.writerow(['Genre Name', 'Number of Movies'])
## dump the dictionary to the csv file
csvWriter.writerows(moviesInGenre.items())
## close the csv file
csvFileResultStep5.close()

# step 6: count movies with "Disney" or "Marvel" in the description
## create a list of all movies with "Disney" or "Marvel" in the description
occurences = {
    'Disney': dfDisneyplus.loc[dfDisneyplus['description'].str.contains('Disney', case=False), 'show_id'].count(),
    'Marvel': dfDisneyplus.loc[dfDisneyplus['description'].str.contains('Marvel', case=False), 'show_id'].count(),
}
## open the csv file for writing and truncate it or create it if it doesn't exist
csvFileResultStep6 = open('exercise1_result_step6.csv', 'w+')
## create a csv writer object
csvWriter = csv.writer(csvFileResultStep6)
## write the header
csvWriter.writerow(['Keyword', 'Number of Movies'])
## dump the dictionary to the csv file
csvWriter.writerows(occurences.items())
## close the csv file
csvFileResultStep6.close()
