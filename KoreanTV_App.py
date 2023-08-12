# function to import library
import streamlit as st
import pandas as pd



# Function to clean the data
def clean_data(tv):
    # Cleaning up Rating, Votes:, Time, and Short Story columns
    tv['Year'] = tv['Year'].fillna(0)
    tv['Release_year'] = tv['Year'].apply(lambda y: str(y).split("–")[0]).replace('\D+','',regex = True)

    tv['Rating'] = tv['Rating'].str.replace("-","0")

    tv = tv.rename(columns = {'Votes:':'Vote'}) # Rename the Vote column, so that it's easier to work with
    tv['Vote'] = tv['Vote'].str.replace("-","0")
    tv['Vote'] = tv['Vote'].str.replace(",","")

    tv['Time'] = tv['Time'].apply(lambda y: str(y).replace("-","0").replace("min","").strip())

    tv['Short Story'] = tv['Short Story'].str.replace("\n","")

    for col in ['Release_year','Rating','Vote','Time']:
        tv[col] = tv[col].apply(pd.to_numeric)

    tv.drop('Year',axis = 1,inplace = True)

    return tv


# Function to select genre
def filter_and_sort_tv_data(tv, genre):
    filtered_tv = tv[tv['Genre'].str.contains(genre) & (tv['Vote'] > tv['Vote'].quantile(0.00))].sort_values(by='Vote', ascending=False)
    return filtered_tv


# Main function
def main():
    st.title("Aplikasi Perbandingan Rating dan Vote Drama Korea")
    url1 = 'https://static.cdntap.com/tap-assets-prod/wp-content/uploads/sites/24/2021/11/drama-korea-rating-tinggi-lead.jpg'
    st.image(url1)

    # Getting the file path
    # Load the TV data
    tv = pd.read_csv("koreanTV.csv")

    # Clean the data
    tv = clean_data(tv)

    # Main function for select genre
    genres = tv['Genre'].unique()
    selected_genre = st.selectbox("Pilih Genre", genres)
    filtered_tv = filter_and_sort_tv_data(tv, selected_genre)
    st.dataframe(filtered_tv)
        

if __name__ == "__main__":
    main()