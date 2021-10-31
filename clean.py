import pandas as pd

df = pd.read_csv('./2022_spring.csv')

# We want only undergraduate courses in the CS and Econ departments
df = df[(df['Mnemonic'] == 'CS') | (df['Mnemonic'] == 'ECON')]
df = df[df['Number'] < 4900]
df.to_csv('dataset.csv')
