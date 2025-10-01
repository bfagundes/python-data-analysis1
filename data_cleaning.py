# This file helps us clean up messy answers so we can count and understand them better.

import pandas as pd 
from config import MULTIPLE_SEPARATOR, TOP_N, OTHERS_LABEL

# This function cleans up answers where people picked only one thing
def clean_single(series: pd.Series) -> pd.Series:
    # Go through each answer:
    # - If it's empty or just spaces, throw it away
    # - If it's a string, remove extra spaces
    s = series.apply(
        lambda x: None if (pd.isna(x) or (isinstance(x, str) and x.strip() == "")) else (x.strip() if isinstance(x, str) else x)
    )
    
    # Remove all the empty ones
    return s.dropna()

# This function handles answers where people picked multiple things
def expand_multiple(series: pd.Series, sep=MULTIPLE_SEPARATOR) -> pd.Series:
    
    # Split each answer into smaller pieces
    def split_cell(x):
        if pd.isna(x):  # If it's empty, return nothing
            return []
        
        if isinstance(x, str):  # If it's a string, split by the separator (like ";")
            parts = [p.strip() for p in x.split(sep)]
            return [p for p in parts if p != ""]
        
        return [x]  # If it's not a string, just return it as-is

    # Break all the answers into pieces and flatten them into one big list
    exploded = series.apply(split_cell).explode()

    # Remove any leftover empty pieces
    return exploded[exploded.notna()]

# This function keeps only the top answers and puts the rest into a group called "Outros"
def cap_top_n_with_outros(counts: pd.Series, n: int = TOP_N, outros_label: str = OTHERS_LABEL) -> pd.Series:
    # Sort answers from most to least popular
    counts = counts.sort_values(ascending=False)

    # If there aren’t more than n answers, just return them all
    if len(counts) <= n:
        return counts

    # Keep the top n answers
    top = counts.iloc[:n]

    # Add up the rest and call them "Outros"
    outros_sum = counts.iloc[n:].sum()
    if outros_sum > 0:
        top.loc[outros_label] = top.get(outros_label, 0) + outros_sum

    return top

# This function turns counts into percentages
def to_percentages(counts: pd.Series) -> pd.Series:
    # Add up all the counts
    total = counts.sum()

    # If there's nothing to count, return an empty list
    if total == 0:
        return pd.Series(dtype=float)

    # Turn each count into a percentage and round to 2 decimal places
    return (counts / total * 100).round(2).sort_values(ascending=False)
