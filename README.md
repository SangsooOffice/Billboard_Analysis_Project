# Project Title
Billboard Chart Song Analysis. This project was conducted during the Data Introduction to Data Science class in the second semester of 2023.

# Why I do this project?
In the modern world, music consumption has exploded with the development of digital streaming services. Here, the Billboard chart is an important indicator for showing popular songs and artists by ranking, understanding market trends and consumer preferences, and establishing effective marketing strategies. For this reason, I chose the theme of Billboard Music Analysis.

# Project Process

**Data Collection**
+ Data was collected by crawling Billboard Hot 100 songs.

![image](https://github.com/user-attachments/assets/54893d2f-83ef-4178-bf15-d4c0e3db6e49)

+ After that, the genre and lyrics of the Billboard Hot 100 songs were collected by crawling in Genie Music.

![image](https://github.com/user-attachments/assets/ee0a7f07-fa0a-48e2-a4d9-ce63a3b4b4e9)


**Preprocessing**

- After crawling, remove missing values of data if present.
- Deal with the terminology.
- Tokenize text in word units.


**Sentiment Analysis**
- Calculate the Sentiment score for each lyric.
- Classifying Sentiment into negative, neutral, and positive based on Sentiment scores.

**Topic modeling**
- Proceed with TF-IDF vectorization.
- Topic modeling was performed using the LDA model.

# Analysis of results
+ Genre trends by year

![image](https://github.com/user-attachments/assets/28028d88-112a-4ec1-aa95-5b189b3ebaf3)

+ trend of lyrics sentiment by month of the year

![image](https://github.com/user-attachments/assets/5b6d8d13-b692-4dd8-8fa7-a1bbb3c30453)

+ Top music title

![image](https://github.com/user-attachments/assets/091a4a84-d951-472b-b849-cf13f2a881fb)

+ Influence of certain genres and lyrics emotions and themes on chart-in.

![image](https://github.com/user-attachments/assets/efbc83b6-f65a-40c8-b538-33d44b4819fe)

- It can be seen that certain genres, lyrics emotions, and topics influence chart-in for a long time.

# contribution
- Insight will let the company know what kind of music can survive on Billboard.

- You can release popular songs in certain months to create effective marketing strategies that inspire empathy in the public.

- To make popular music in a specific month, you can preoccupy artists specializing in specific song themes, emotions, and specific genres.

- To help you stay longer on the chart, you can plan to long run on the chart by promoting song themes and music based on genres and emotions gained through insights.

# Difficult Point
- The part of data collection using crawling.