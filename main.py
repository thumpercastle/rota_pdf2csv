import tabula
import pandas as pd
import re
import datetime as dt
import numpy as np

## read pdf
df = tabula.read_pdf(input_path="C:/Users/tonyr/Downloads/lidia_rota_file.pdf", pages="all")
print(df[15:45])

## add a date column
df["date"] = pd.date_range("2020-09-06", "2021-09-30", freq="D")

## drop defunct index column and filter to required column
df = df.drop(df.index[0])
df = df.filter(items=["date", "adia/Lidi"], axis=1)

## make data into usable format
df.columns = ["date", "shift"]
df["Start Date"] = pd.to_datetime(df["date"])

## create day of week and sort for Lidia's days
df["day_of_week"] = df["date"].dt.day_name()
df = df[df["day_of_week"].str.contains("Monday|Tuesday|Wednesday|Sunday", regex=True)]

## tidy up data and make it readable
df = df.replace(to_replace="O", value="Ordinary")
df = df.replace(to_replace="L", value="Long day")
df = df.replace(to_replace="N", value="Nights")
df["shift"] = df["shift"].fillna("*")
df = df.replace(to_replace="*", value="Zero hours")
df = df.replace(to_replace=".*AL$", value="Annual leave", regex=True)
df["Description"] = df["shift"]
df["End Date"] = np.where(df["Description"]=="Nights", df["Start Date"]+dt.timedelta(days=1), df["Start Date"])

## drop defunct columns
# df = df.drop(columns=["date", "day_of_week", "shift"])
# print(df.head())

## add start times
df["Start Time"] = df["Description"]
df["Start Time"] = df["Start Time"].replace(["Ordinary", "Long day", "Nights", "Zero hours", "Annual leave"],\
                                            ["09:00", "09:00", "20:00", "09:00", "09:00"])

## add end times
df["End Time"] = df["Description"]
df["End Time"] = df["End Time"].replace(["Ordinary", "Long day", "Nights", "Zero hours", "Annual leave"],\
                                            ["17:00", "21:00", "09:00", "10:00", "10:00"])
#print(df[15:45])

# df.to_csv(path_or_buf="C:/Users/tonyr/Downloads/lidia_rota_file.csv",index=False)