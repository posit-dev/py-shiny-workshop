We have a second sidebad input which allows the user to filter the dataset by the number of characters in the `text` field.
Add a second reactive calculation to the app which filters the `account_data()` reactive.

For `input.chars()` returns a tuple with the lower and upper range of a value, and you can filter the data frame with:
`df[df["text"].str.len().between(*input.chars()]`.
