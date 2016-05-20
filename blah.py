import pandas as pd


group = [
    [0, 1],
    [0, 1],
    [1, 1],
    [1, 0]
]


df = pd.DataFrame(group)
df.columns = ['a', 'b']

print(df)
print()

for col in df.columns:
    print(df.groupby(col).count().max())