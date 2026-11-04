import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv(
    "data/Perovskite_database_content_all_data.csv", low_memory=False 
)
#converting band gaps to numeric numbers before I drop, Use 'coerce' so that bad data becomes NaN

df['Perovskite_band_gap'] = pd.to_numeric(df['Perovskite_band_gap'], errors = 'coerce')


#getting rid of the values that the data set will not permit
columns = [
    'Perovskite_composition_a_ions',
    'Perovskite_composition_a_ions_coefficients',
    'Perovskite_composition_b_ions',
    'Perovskite_composition_b_ions_coefficients',
    'Perovskite_composition_c_ions',
    'Perovskite_composition_c_ions_coefficients',
    'Perovskite_band_gap',
]




df = df.dropna(subset = columns)
print(df.size)


#grabbing the composition monovalent cation
a_ions = (df['Perovskite_composition_a_ions']).tolist()
a_ions_compositions = (df['Perovskite_composition_a_ions_coefficients']).tolist()


#divalent metals are the b-sites here
b_ions = (df['Perovskite_composition_b_ions']).to_numpy()
b_ions_compositions = (df['Perovskite_composition_b_ions_coefficients']).to_numpy()

#halides are here
x_ions = (df['Perovskite_composition_c_ions']).to_numpy()
x_ions_compositions = (df['Perovskite_composition_c_ions_coefficients']).to_numpy()



#to replicate the husssain paper I want to only replicate a few of the compounds (potential to build on later)
allowed_a = ['Cs', 'FA', 'MA']
allowed_b = ['Pb','Sn']
allowed_x =   ['I','Br','Cl']

#make a note of which indices are bad
index_to_drop = []
for i in range(len(a_ions)):
    a_good = all(ion in allowed_a for ion in a_ions[i].split('; '))
    b_good = all(ion in allowed_b for ion in b_ions[i].split('; '))
    x_good = all(ion in allowed_x for ion in x_ions[i].split('; '))
    #if any of these are not good then drop the row
    if a_good and b_good and x_good:
        pass
    else:
        index_to_drop.append(df.index[i])

df = df.drop(index = index_to_drop)



#dropping duplicated rows using pandas duplicated function
df.duplicated(subset=columns).sum()
df = df.drop_duplicates(subset = columns)
###


#adding in a loop that sorts out the issue with
# Cl;Br = 0.25;0.75 and Br;CL = 0.75,0.25 not being the same

ions = ['Cs','FA','MA','Pb','Sn','I','Br','Cl']
clean_df = pd.DataFrame(columns = ions + ['band_gap'])
skipped_val = 0

for i in range(len(df)):
    #making lots of rows of zeros
    row = df.iloc[i]
    new_row  = pd.Series(0.0, index = ions + ['band_gap'])
    good = True




    #scrapping where the lengths are different
    for names, coeffs in [(row['Perovskite_composition_a_ions'],row['Perovskite_composition_a_ions_coefficients']),
                          (row['Perovskite_composition_b_ions'], row['Perovskite_composition_b_ions_coefficients']),
                          (row['Perovskite_composition_c_ions'], row['Perovskite_composition_c_ions_coefficients'])]:
        names =   names.split('; ')
        coeffs = coeffs.split('; ')
        if len(names)!= len(coeffs):
            good =  False
            break
        for j in range(len(names)):
            try:
                new_row[names[j]] = round(float(coeffs[j]),2)
            except ValueError:
                good = False
    if not good:
        skipped_val +=1 
        continue

    new_row['band_gap'] = row['Perovskite_band_gap']


    #we'll append only if an identicla row isn't already in the clean df
    if not (clean_df == new_row).all(axis =1).any():
            clean_df.loc[len(clean_df)] = new_row


print(len(clean_df),skipped_val)

clean_df.to_csv('data/clean_data.csv', index = False)
