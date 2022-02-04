import json
import pandas as pd

# step 1: read the json file
## open the json file, which is in the same directory as this script, for reading
jsonFile = open('pokemon.json')
## read the json file
jsonData = json.load(jsonFile)
## close the json file
jsonFile.close()
## create a DataFrame from the json file
dfPokemon = pd.DataFrame(jsonData['pokemon'])

# step 2: create a list of all pokemon types and its counts
## first, create a dictionary to store the pokemon types and their counts
pokemonTypes = {}
## iterate over the column containing the types of each pokemon
for pokemon in dfPokemon.get('type'):
    ## iterate over the list of types of the current pokemon
    for pokemonType in pokemon:
        ## finally, add the type to the dictionary if it is not already in the dictionary and increase the count by 1
        pokemonTypes[pokemonType] = pokemonTypes.get(pokemonType, 0) + 1

# step 3: write result to csv file
## get the keys of the dictionary, which are the pokemon types
matrixElements = pokemonTypes.keys()
## create a DataFrame from the list of pokemon types, both with the pokemon types as the rows and the columns
dfPokemonTypesMatrix = pd.DataFrame(0, index=matrixElements, columns=matrixElements).rename_axis('type')
## iterate over the column containing the types of each pokemon
for pokemon in dfPokemon.get('type'):
    ## next, iterate over the list of types of the current pokemon
    for pokemonTypeX in pokemon:
        ## and iterate again over the list of types of the current pokemon
        for pokemonTypeY in pokemon:
            ## count only if both iterations are not the same pokemon type or the pokemon has only one type
            if pokemonTypeX != pokemonTypeY or len(pokemon) == 1:
                ## finally, increase the count of the matrix element by 1
                dfPokemonTypesMatrix.loc[pokemonTypeX, pokemonTypeY] = dfPokemonTypesMatrix.loc[pokemonTypeX, pokemonTypeY] + 1

## export the matrix to a csv file
dfPokemonTypesMatrix.to_csv('exercise2_result.csv', columns=matrixElements)
