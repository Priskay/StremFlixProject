import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------
# Database Connection
# ---------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="#",            # your MySQL username
    password="#",            # your MySQL password
    database="#"    # your database name
)

# ---------------------------
# 1. User Distribution by Country
# ---------------------------
query_country = """
SELECT
    country,
    COUNT(userID) AS total_users
FROM users
GROUP BY country
ORDER BY total_users DESC;
"""

df_country = pd.read_sql(query_country, conn)
print("\nUser Distribution by Country:\n", df_country)

plt.figure(figsize=(8,5))
plt.bar(df_country['country'], df_country['total_users'])
plt.title('User Distribution by Country')
plt.xlabel('Country')
plt.ylabel('Number of Users')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ---------------------------
# 2. Top 10 Movies by Average Ratings
# ---------------------------
query_top_movies = """
SELECT 
    m.Title,
    ROUND(AVG(r.Rating), 2) AS AvgRating,
    COUNT(r.RatingID) AS TotalRatings
FROM Ratings r
JOIN Movies m ON r.MovieID = m.MovieID
GROUP BY m.Title
ORDER BY AvgRating DESC
LIMIT 10;
"""

df_top_movies = pd.read_sql(query_top_movies, conn)
print("\nTop 10 Movies by Average Ratings:\n", df_top_movies)

plt.figure(figsize=(10,6))
plt.barh(df_top_movies['Title'], df_top_movies['AvgRating'], color='skyblue')
plt.title('Top 10 Movies by Average Ratings')
plt.xlabel('Average Rating')
plt.ylabel('Movie Title')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()


# ---------------------------
# 3. Most Popular Genres
# ---------------------------
query_genres = """
SELECT 
    m.Genres,
    COUNT(r.RatingID) AS TotalRatings
FROM Ratings r
JOIN Movies m ON r.MovieID = m.MovieID
GROUP BY m.Genres
ORDER BY TotalRatings DESC
LIMIT 10;
"""

df_genres = pd.read_sql(query_genres, conn)
print("\nMost Popular Genres:\n", df_genres)

plt.figure(figsize=(10,6))
plt.barh(df_genres['Genres'], df_genres['TotalRatings'], color='coral')
plt.title('Most Popular Genres')
plt.xlabel('Total Ratings')
plt.ylabel('Genres')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()


# ---------------------------
# 4. User Distribution by Age Group
# ---------------------------
query_age_group = """
SELECT
    CASE
        WHEN Age < 18 THEN '<18'
        WHEN Age BETWEEN 18 AND 25 THEN '18-25'
        WHEN Age BETWEEN 26 AND 35 THEN '26-35'
        WHEN Age BETWEEN 36 AND 50 THEN '36-50'
        ELSE '50+'
    END AS AgeGroup,
    COUNT(*) AS TotalUsers
FROM Users
GROUP BY AgeGroup
ORDER BY AgeGroup;
"""

df_age_group = pd.read_sql(query_age_group, conn)
print("\nUser Distribution by Age Group:\n", df_age_group)

plt.figure(figsize=(8,5))
plt.bar(df_age_group['AgeGroup'], df_age_group['TotalUsers'], color='purple')
plt.title('User Distribution by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Total Users')
plt.tight_layout()
plt.show()


# ---------------------------
# 5. Distribution by Subscription Status
# ---------------------------
query_subscription = """
SELECT 
    SubscriptionStatus,
    COUNT(UserID) AS TotalUsers
FROM Users
GROUP BY SubscriptionStatus;
"""

df_subscription = pd.read_sql(query_subscription, conn)
print("\nDistribution of Users by Subscription Status:\n", df_subscription)

plt.figure(figsize=(6,6))
plt.pie(df_subscription['TotalUsers'], labels=df_subscription['SubscriptionStatus'], autopct='%1.1f%%', startangle=90)
plt.title('Distribution of Users by Subscription Status')
plt.tight_layout()
plt.show()


# ---------------------------
# 6. Distribution of Device Usage Among Users
# ---------------------------
query_device = """
SELECT 
    Device,
    COUNT(UserID) AS TotalUsers
FROM Users
GROUP BY Device
ORDER BY TotalUsers DESC;
"""

df_device = pd.read_sql(query_device, conn)
print("\nDistribution of Device Usage Among Users:\n", df_device)

plt.figure(figsize=(8,5))
plt.barh(df_device['Device'], df_device['TotalUsers'], color='green')
plt.title('Device Usage Distribution')
plt.xlabel('Device')
plt.ylabel('Total Users')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()



#7. User Distribution by Age Group 2
# ---------------------------
query_age_group2 = """
SELECT 
    CASE 
        WHEN Age BETWEEN 0 AND 10 THEN '0-10'
        WHEN Age BETWEEN 11 AND 20 THEN '11-20'
        WHEN Age BETWEEN 21 AND 30 THEN '21-30'
        WHEN Age BETWEEN 31 AND 40 THEN '31-40'
        WHEN Age BETWEEN 41 AND 50 THEN '41-50'
        WHEN Age BETWEEN 51 AND 60 THEN '51-60'
        ELSE '60+'
    END AS AgeGroup,
    COUNT(*) AS TotalUsers
FROM Users
GROUP BY AgeGroup
ORDER BY MIN(Age);
"""

df_age_group2 = pd.read_sql(query_age_group2, conn)
print("\nUser Distribution by Age Group:\n", df_age_group2)

plt.figure(figsize=(8,5))
plt.bar(df_age_group2['AgeGroup'], df_age_group2['TotalUsers'], color='purple')
plt.title('User Distribution by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Total Users')
plt.tight_layout()
plt.show()

"""
query_gender_preferences = 
SELECT
    YEAR(m.Year) AS Year,
    m.Genres,
    COUNT(r.RatingID) AS TotalRatings
FROM Ratings r
JOIN Movies m ON r.MovieID = m.MovieID
JOIN Users u ON r.UserID = u.UserID
WHERE u.Gender = 'F'
  AND m.Year BETWEEN 1975 AND 2025
GROUP BY YEAR(m.Year), m.Genres
ORDER BY YEAR(m.Year);


df_gender_pref = pd.read_sql(query_gender_preferences, conn)

print(df_gender_pref.head())

# Optional: Pivot for easier plotting
pivot_df = df_gender_pref.pivot_table(
    index='Year',
    columns='Genres',
    values='TotalRatings',
    aggfunc='sum'
).fillna(0)

plt.figure(figsize=(10,6))
for genre in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[genre], label=genre)

plt.title("Evolution of Genre Preferences Among Women (1975–2025)")
plt.xlabel("Year")
plt.ylabel("Number of Ratings (Female Viewers)")
plt.legend(title="Genre", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
"""


# Load the datasets from SQL
users_df = pd.read_sql("SELECT * FROM Users", conn)
movies_df = pd.read_sql("SELECT * FROM Movies", conn)
ratings_df = pd.read_sql("SELECT * FROM Ratings", conn)
 
# --- STEP 1: Filter for female users only ---
female_ratings = ratings_df.merge(users_df, on="UserID")
female_ratings = female_ratings[female_ratings["Gender"] == "F"]
 
# --- STEP 2: Join with movie data & filter for movies released after 1975 ---
female_ratings = female_ratings.merge(movies_df, on="MovieID")
female_ratings = female_ratings[female_ratings["Year"] >= 1975]
 
# --- STEP 3: Extract primary genre for simplicity ---
female_ratings["PrimaryGenre"] = female_ratings["Genres"].str.split('|').str[0]
 
# --- STEP 4: Group by year and genre to get average ratings ---
genre_trends = (
    female_ratings.groupby(["Year", "PrimaryGenre"])["Rating"]
    .mean()
    .reset_index()
)
 
# --- STEP 5: Plot the evolution of female genre preferences ---
plt.figure(figsize=(12, 7))
sns.lineplot(
    data=genre_trends,
    x="Year",
    y="Rating",
    hue="PrimaryGenre",
    linewidth=2.5
)
genre_trends
""" 
plt.title("Evolution of Genre Preferences Among Female Users (1975–2025)", fontsize=14)
plt.xlabel("Release Year", fontsize=12)
plt.ylabel("Average Rating (by Female Users)", fontsize=12)
plt.legend(title="Genre", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()"""
# ---------------------------
# Close the connection
# ---------------------------
conn.close()

print("\nAll queries executed and visualizations completed successfully!")
