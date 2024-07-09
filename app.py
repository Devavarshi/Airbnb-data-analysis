import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from mpl_toolkits.mplot3d import Axes3D

# Setting Webpage Configurations
st.set_page_config(page_icon="🌎",page_title="Airbnb", layout="wide")

logo_path = "https://www.zilliondesigns.com/blog/wp-content/uploads/Airbnb-Logo-Contest-830x400.png"  # Replace with the actual path to your logo
# Display the logo
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="{logo_path}" alt="Logo" style="width:200px;">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: blue;'>Airbnb Data Visualization By Devavarshini</h1>", unsafe_allow_html=True)
col1, col2 = st.columns(2, gap='medium')
with col1:

    col1.markdown("## :blue[Domain] : Travel Industry, Property Management and Tourism")
    col1.markdown("## :blue[Technologies used] : Python, Pandas, Plotly, Streamlit, MongoDB")
    col1.markdown("## :blue[Overview] : To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")
with col2:
    col2.markdown("#   ")
    st.image("https://i.gifer.com/7lI8.gif")
    col2.markdown("#   ")

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title(':rainbow[Airbnb Analysis] 🔍')

df = pd.read_csv(r'C:\Users\varshinikarthik\Desktop\Varshini\airbnb\Airbnb.csv')

aggregated = df.groupby(['Country','Longitude','Latitude']).count()

tab1,tab2,tab3 = st.tabs(['Airbnb data Analysis 🌍','Exploratory Data Analysis 📈','Insights 🧐'])

with tab1:
    country = st.multiselect('Select a Country', sorted(df['Country'].unique()), sorted(df['Country'].unique()))
    prop = st.multiselect('Select Property Type', sorted(df['Property Type'].unique()), sorted(df['Property Type'].unique()))
    room = st.multiselect('Select Room Type', sorted(df['Room Type'].unique()), sorted(df['Room Type'].unique()))
    price = st.slider('Select price range', int(df['Price'].min()), int(df['Price'].max()), (int(df['Price'].min()), int(df['Price'].max())))

    # Filter data based on selections
    filtered_df = df[(df['Country'].isin(country)) & 
                     (df['Property Type'].isin(prop)) & 
                     (df['Room Type'].isin(room)) & 
                     (df['Price'] >= price[0]) & (df['Price'] <= price[1])]

    st.write("Filtered Data")
    st.dataframe(filtered_df)

    st.header("Listings Count by Country")
    if not filtered_df.empty:
        # Count the number of listings per country
        country_counts = filtered_df['Country'].value_counts().reset_index()
        country_counts.columns = ['Country', 'Count']

        # Create a bar chart
        fig, ax = plt.subplots()
        sns.barplot(x='Country', y='Count', data=country_counts, ax=ax)
        ax.set_title("Number of Listings by Country")
        st.pyplot(fig)
    else:
        st.write("No data to display.")

with tab2:

    col1,col2 = st.columns(2)
    with col1:
     option = st.selectbox('Price Analysis',('Select an Analysis','Price Analysis by Country', 'Distribution of Price using plots','Price vs rating','Price vs Availability'))
    st.divider() 
    # Filter dataframe based on selections
    filtered_df = df[df['Country'].isin(country) & df['Property Type'] & df['Room Type'] & df['Price']]

    if option == 'Price Analysis by Country':
        fig = px.histogram(df,x = 'Country',y ='Price', animation_frame='Price',color = 'Country')
        fig.update_layout(width=1200,height=500, title="Animated Histogram by Country",xaxis_title="Country",yaxis_title="Price")
        st.plotly_chart(fig)
    elif option == 'Distribution of Price using plots':
        # Price distribution
        st.header('Price Distribution')
        fig, ax = plt.subplots()
        sns.histplot(filtered_df['Price'], kde=True, ax=ax, binrange=(price[0], price[1]))
        st.pyplot(fig)

    elif option == 'Price vs rating':
        # Price vs. Rating
        st.header('Price vs. Rating')
        fig, ax = plt.subplots()
        sns.scatterplot(data=filtered_df, x='Price', y='Rating', ax=ax)
        st.pyplot(fig)
    elif option == 'Price vs Availability':
        st.header('Price vs Availability')
        scatter_plot = go.Figure()

        scatter_plot.add_trace(go.Scatter(
            x=filtered_df['Price'],
            y=filtered_df['Availability 365'],
            mode='markers',
            marker=dict(
                size=10,
                color=filtered_df['Price'],  # Color based on price
                colorscale='Viridis',  # Color scale
                showscale=True  # Show color scale
            )
        ))

        scatter_plot.update_layout(
            title='Price vs Availability 365',
            xaxis_title='Price',
            yaxis_title='Availability 365',
            height=750,
            width=1200
        )

        st.plotly_chart(scatter_plot)

    col1,col2 = st.columns(2)
    with col1:
     option = st.selectbox('Review & availability Analysis',('Select an Analysis','Review frequency by year','Review frequency by month','Distribution of Number of Reviews', 'Availability Analysis'))
    st.divider()
    df['Review Date'] = pd.to_datetime(df['Review Date'], errors='coerce')
    review_df = df.dropna(subset=['Review Date'])
    # Extract year and month for analysis
    review_df['Review Year'] = review_df['Review Date'].dt.year
    review_df['Review Month'] = review_df['Review Date'].dt.month
    reviews_per_month_year = review_df.groupby(['Review Year', 'Review Month']).size().reset_index(name='Number of Reviews')
    col1,col2 = st.columns(2)
    with col1:
        if option == 'Review frequency by year':
            st.header('Review Frequency by Year')
            reviews_per_year = review_df.groupby('Review Year').size()
            fig, ax = plt.subplots()
            reviews_per_year.plot(kind='bar', ax=ax)
            ax.set_title('Number of Reviews per Year')
            ax.set_xlabel('Year')
            ax.set_ylabel('Number of Reviews')
            st.pyplot(fig)
        if option == 'Review frequency by month':
            # Review frequency by month
            # Prepare data for 3D plot
            x = reviews_per_month_year['Review Year']
            y = reviews_per_month_year['Review Month']
            z = reviews_per_month_year['Number of Reviews']

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            # Create the 3D bar plot
            ax.bar3d(x, y, [0]*len(z), 1, 1, z, shade=True)
 
            ax.set_title('Number of Reviews by Year and Month')
            ax.set_xlabel('Year')
            ax.set_ylabel('Month')
            ax.set_zlabel('Number of Reviews')

            st.header('Review Frequency by Year and Month')
            st.pyplot(fig)
    col1,col2 = st.columns(2)
    with col1:
        if option == 'Distribution of Number of Reviews':
            fig, ax = plt.subplots()
            df['Number Of Reviews'].plot(kind='hist', bins=50, ax=ax)
            ax.set_title('Distribution of Number of Reviews')
            ax.set_xlabel('Number of Reviews')
            ax.set_ylabel('Frequency')
            st.pyplot(fig)
    col1,col2 = st.columns(2)
    with col1:    
            # AVAILABILITY BY ROOM TYPE BOX PLOT
        if option == 'Availability Analysis':
            fig = px.box(data_frame=df,
                        x='Room Type',
                        y='Availability 365',
                        color='Room Type',
                        title='Availability by Room_type'
                        )
            st.plotly_chart(fig, use_container_width=True)
with tab3:
    col1,col2 = st.columns(2)
    with col1:
     option = st.selectbox('Insights Questions',('1,What is the average availability & most booked roomtype?','2,What is the average rating per room type?','3,What is the relationship between price and availability?',
                                                 '4,How many listings are there per country?','5,Busiest month of the year','6,Number of review by Year','7,How does the security deposit vary by property type?',
                                                 '8,How does the price vary by neighborhood?','9,Which Country have the highest average ratings?','10,What is the distribution of the minimum nights required?'))
    st.divider()
    if option == '1,What is the average availability & most booked roomtype?':
        avg_availability_per_room = df.groupby('Room Type')['Availability 365'].mean().reset_index()
        most_booked_room_type = avg_availability_per_room.loc[avg_availability_per_room['Availability 365'].idxmin()]
        st.header('Most Booked Room Type')
        st.write(f"The most booked room type is **{most_booked_room_type['Room Type']}** with an average availability of {most_booked_room_type['Availability 365']:.2f} days per year.")
        fig = px.bar(avg_availability_per_room, x='Room Type', y='Availability 365', title='Average Availability per Room Type')
        fig.update_layout(xaxis_title='Room Type', yaxis_title='Average Availability (days)', yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig)
    if option == '2,What is the average rating per room type?':
        st.header('Average Rating per Room Type')
        avg_rating_per_room = df.groupby('Room Type')['Rating'].mean().sort_values()
        fig = px.bar(avg_rating_per_room, x=avg_rating_per_room.index, y=avg_rating_per_room.values, title='Average Rating per Room Type')
        st.plotly_chart(fig)
    if option == '3,What is the relationship between price and availability?':
        st.header('Price vs Availability')
        fig = px.scatter(df, x='Price', y='Availability 365', title='Price vs Availability')
        st.plotly_chart(fig)
    if option == '4,How many listings are there per country?':
        st.header('Listings per Country')
        st.write('United states is highest in listing with 1222')
        listings_per_country = df['Country'].value_counts()
        fig = px.bar(listings_per_country, x=listings_per_country.index, y=listings_per_country.values, title='Listings per Country')
        st.plotly_chart(fig)
    if option == '5,Busiest month of the year': 
        df['Review Date'] = pd.to_datetime(df['Review Date'])
        # Extract month and year from 'Review Date'
        df['Review Month'] = df['Review Date'].dt.month
        df['Review Year'] = df['Review Date'].dt.year
        reviews_per_month_year = df.groupby(['Review Year','Review Month']).size().reset_index(name='Number of Reviews')

        # Create a pivot table for better visualization
        pivot_reviews = reviews_per_month_year.pivot(index='Review Month', columns='Review Year', values='Number of Reviews')

        # Plotting the busiest month
        fig, ax = plt.subplots(figsize=(12, 6))
        pivot_reviews.plot(kind='bar', ax=ax)
        ax.set_title('Number of Reviews per Month')
        ax.set_xlabel('Month')
        ax.set_ylabel('Number of Reviews')
        st.pyplot(fig)
        # Identifying the busiest month
        busiest_month = reviews_per_month_year.loc[reviews_per_month_year['Number of Reviews'].idxmax()]
        st.header('Busiest Month')
        st.write("Busiest month is Feb of 2019 with highest reviews")       
    if option == '6,Number of review by Year':
        st.header('Number of Reviews vs Last Review Date')
        df['review_year'] = df['Review Date'].dt.year
        reviews_per_year = df.groupby('review_year')['Number Of Reviews'].sum()
        fig = px.line(reviews_per_year, x=reviews_per_year.index, y=reviews_per_year.values, title='Number of Reviews per Year')
        st.plotly_chart(fig)
    if option == '7,How does the security deposit vary by property type?':
        st.header('Security Deposit by Property Type')
        avg_security_deposit_per_property = df.groupby('Property Type')['Security Deposit'].mean()
        fig = px.bar(avg_security_deposit_per_property, x=avg_security_deposit_per_property.index, y=avg_security_deposit_per_property.values, title='Average Security Deposit per Property Type')
        st.plotly_chart(fig)
    if option == '8,How does the price vary by neighborhood?':
        st.header('Price Variation by Neighborhood')
        avg_price_per_neighborhood = df.groupby('Host Neighbourhood')['Price'].mean().sort_values()
        fig = px.bar(avg_price_per_neighborhood, x=avg_price_per_neighborhood.index, y=avg_price_per_neighborhood.values, title='Average Price per Neighborhood')
        st.plotly_chart(fig)
    if option == '9,Which Country have the highest average ratings?':
        st.header('Top Cities by Average Rating')
        avg_rating_per_city = df.groupby('Country')['Rating'].mean().sort_values(ascending=False).head(10)
        fig = px.bar(avg_rating_per_city, x=avg_rating_per_city.index, y=avg_rating_per_city.values, title='Top Cities by Average Rating')
        st.plotly_chart(fig)
    if option == '10,What is the distribution of the minimum nights required?':
        st.header('Distribution of Minimum Nights')
        minimum_nights_distribution = df['Minimum Nights'].value_counts().sort_index().reset_index()
        minimum_nights_distribution.columns = ['Minimum Nights', 'Frequency']
        fig = px.line(minimum_nights_distribution, 
                    x='Minimum Nights', 
                    y='Frequency', 
                    title='Distribution of Minimum Nights',
                    labels={'Minimum Nights': 'Minimum Nights', 'Frequency': 'Frequency'})
        st.plotly_chart(fig)

    st.title("Airbnb Data Analysis Report")

    # Room Booking
    st.subheader("Room Booking")
    st.markdown("""
    - The chart indicates that the most booked room type is **Private room** with an average availability of **167 days per annum**.
    - The average price for shared rooms is **349.5904**, with one extreme value at **48K** between **11K** to **50K**.
    - Out of the total **5555 listings**, only **83** are shared rooms, indicating very low booking numbers for shared rooms.
    """)

    st.subheader("Ratings")
    st.markdown("""
    - The average number of ratings is highest for **Entire home/apt** at **72**.
    - To encourage more reviews, promotional offers can be sent to customers after their booking completion.
    """)
    st.subheader("Geographic Distribution")
    st.markdown("""
    - The **United States** has the highest number of listings with **1222**.
    """)
    st.subheader("Price and Availability")
    st.markdown("""
    - Properties priced at **48K** have an availability of **365 days**.
    - Most of the booking resides between 10$ to 11K $ .
    """)

    st.subheader("Busiest Months")
    st.write("The busiest months are **January, February, and March**.")
    
    st.subheader("Review Frequency")
    st.write("Reviews peaked in the year **2019** with **124 reviews**.")

    # Security Deposit
    st.subheader("Security Deposit")
    st.write("**Service apartments** have high security deposits, whereas **hotels** have lower security deposits.")

    st.subheader("Highest Price")
    st.write("The neighborhood with the highest price is **Venice**, indicating it has the highest booking prices.")

    st.subheader("Geographic Ratings")
    st.write("The **United States** has the highest ratings, while **Turkey** has the lowest ratings.")

    # Minimum Night Stay
    st.header("Minimum Night Stay")
    st.write("For the **5555 listings**, the minimum night maximum count distribution is:")
    st.write("- **1 night**: 1862 listings")
    st.write("- **2 nights**: 1505 listings")
    
    st.header("Business Improvement Plan")
    st.markdown("""
    - To increase hosts and bookings in countries like **China** and **India** due to their high populations, Airbnb can focus on more advertisements in these regions.
    - **Finland** should also be targeted for more advertisement as studies show that people in Finland travel on average **7.50 times** per person.            
    - To increase the occupancy of shared rooms, more offers and promotions can be provided to the people who are booking shared room to attract customers.
    - Hosts can be advised to reduce price of 50 K staycation to increase booking numbers since it is available for 365 days.
    - Promotional offers should be avoided during these months and focus on months with lower bookings like **June and July**.
    - To increate the reviews for host and booking  Airbnb can offer discound to the customers for the next visit.         
    """)


    