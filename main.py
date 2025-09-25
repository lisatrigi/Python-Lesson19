import pandas as pd
import streamlit as st
import plotly.express as px

books_df = pd.read_csv('file.csv')

st.title("Bestselling Books Analysis")
st.write("This app analyzes the Amazon Top Selling books from 2009 to 2022.")
st.subheader("Summary Statistics")
total_books = books_df.shape[0]
unique_titles = books_df['Name'].nunique()
average_rating = books_df['User Rating'].mean()
average_price = books_df['Price'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Books", total_books)
col2.metric("Unique Titles", unique_titles)
col3.metric("Average Rating", f"{average_rating:.2f}")
col4.metric("Average Price", f"${average_price:.2f}")
# col3.metric("Average Rating", average_rating) does not round the number
# col4.metric("Average Price", average_price) -||-

# df = pd.DataFrame({
#     'Name': ['Lisa', 'Suela', 'Rita'],
#     'Age' : [15,16,17],
#     'City' : ['Stockholm', 'Edinburgh', 'Paris']
# }
# )

# st.write(df)

st.subheader('Stats')
st.write(books_df.head())

col1, col2 = st.columns(2, gap="small")

with col1:
    st.subheader("Top 10 Books")
    top_titles = books_df['Name'].value_counts().head(10)
    st.bar_chart(top_titles)

with col2:
    st.subheader("Top 10 authors")
    top_authors = books_df['Author'].value_counts().head(10)
    st.bar_chart(top_authors)

st.subheader("Genre Distribution")
fig = px.pie(books_df, names= "Genre", title='Most liked Genre 2009-2022', color="Genre", 
color_discrete_sequence=px.colors.sequential.Plasma)
st.plotly_chart(fig)

st.subheader("Top 15 Authors")
top_authors = books_df["Author"].value_counts().head(15).reset_index()
top_authors.columns = ['Author', 'Count']

figg = px.bar(top_authors, x="Count", y="Author", orientation="h", 
              title="Top 15 authors",
              labels={"Count": "Count of Books Published", "Author":"Author"},
              color= 'Count', color_continuous_scale=px.colors.sequential.Plasma
)

st.plotly_chart(figg)

st.subheader("Filter Data by Genre")
genre_filter = st.selectbox("Select Genre", books_df['Genre'].unique())
filtered_df = books_df[books_df['Genre'] == genre_filter]
st.write(filtered_df)

st.sidebar.header("Add a new book data")
with st.sidebar.form("book_form"):
    new_name = st.text_input("Book Name")
    new_author = st.text_input("Author Name")
    new_user_rating = st.slider("User Rating", 0.0,5.0,0.0,0.1)
    new_reviews = st.number_input("Reviews", min_value=0, step=1)
    new_price = st.number_input("Price", min_value=0, step=1)
    new_year = st.number_input("Year", min_value=2009, max_value=2022, step=1)
    new_genre = st.selectbox("Genre", books_df['Genre'].unique())
    submit_button = st.form_submit_button(label="Add Book")

if submit_button:
    new_data = {
        'Name': new_name,
        'Author': new_author,
        'User Rating': new_user_rating,
        'Reviews': new_reviews,
        'Price': new_price,
        'Year': new_year,
        'Genre': new_genre
    }
    books_df = pd.concat([pd.DataFrame(new_data, index=[0]), books_df], ignore_index=True)
    books_df.to_csv("file.csv")
    st.sidebar.success("New book added successfully")

st.sidebar.header("Filter Option")
selected_author = st.sidebar.selectbox("Selected Author", ["All"] + list(books_df['Author'].unique()))
selected_year = st.sidebar.selectbox("Select Year", ["All"] +list(books_df['Year'].unique()))
selected_genre = st.sidebar.selectbox("Select Genre", ["All"] + list(books_df['Genre'].unique()))
min_rating = st.sidebar.slider("Minimum USe Rating", 0.0,5.0,0.0,0.1)
max_price = st.sidebar.slider("Max Price",0, books_df['Price'].max(),books_df['Price'].max())