# 🍿 PopcornPicks: An AI-Powered Movie Recommendation System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://popcornpicks-movie-recommender-jdfgvtfzgvy6yhznumodbp.streamlit.app/)

PopcornPicks is a feature-rich, interactive web application that provides smart movie recommendations. This project demonstrates a complete end-to-end data science workflow, from data acquisition and processing to machine learning model building and live deployment.

---

## ✨ Features Showcase

PopcornPicks is more than just a recommender. It's a full-fledged movie discovery platform.

#### 🤖 AI Recommender
Get personalized movie suggestions based on a content-based filtering model. The AI analyzes plot, genres, cast, and director to find movies with a similar "DNA".
<img width="1919" alt="AI Recommender" src="https://github.com/user-attachments/assets/ef7a5118-dfcd-4213-8168-51c6872241a6" />

---

#### 🔎 Movie Explorer
A powerful tool to filter the entire 5,000-movie dataset by genre, release year, and minimum rating.
<img width="1911" alt="Movie Explorer" src="https://github.com/user-attachments/assets/453d1c2c-c815-44a3-9de8-01bea7b9cfaa" />

---

#### 🏆 Critically Acclaimed & 💰 Highest Grossing
Discover top-performing movies based on real rating and revenue data.
<img width="1919" alt="Critically Acclaimed" src="https://github.com/user-attachments/assets/c1b9f1e3-19cb-4655-b75a-c193f92f7f0e" />

---

#### 🧑‍🎤 Search by Actor
Find all movies in the dataset starring your favorite actor.
<img width="1919" alt="Search by Actor" src="https://github.com/user-attachments/assets/0616e7e2-4284-4b90-8466-78dbde24dd91" />

---

#### 🎬 Discover by Genre
Explore the best movies within a specific genre.
<img width="1919" alt="Discover by Genre" src="https://github.com/user-attachments/assets/a1ddee0a-1504-4145-a0fd-a2aa442246ff" />

---

## 🛠️ Tech Stack

- **Backend & ML:** Python, Pandas, Scikit-learn
- **Web Framework:** Streamlit
- **Data Source:** The Movie Database (TMDb) API
- **Deployment:** Streamlit Community Cloud
- **Version Control:** Git & Git LFS (for handling large model files)

## 🚀 How to Run Locally

To run this project on your own machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MananSapaloke/PopcornPicks-Movie-Recommender.git
    cd PopcornPicks-Movie-Recommender
    ```

2.  **Set up a Python virtual environment:**
    *(A stable version like Python 3.11 is recommended)*
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Git LFS to handle large model files:**
    *(Download from https://git-lfs.github.com/ if not installed)*
    ```bash
    git lfs install
    git lfs pull
    ```

4.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Get your TMDb API Key:**
    - Go to [The Movie Database (TMDb)](https://www.themoviedb.org/) and create a free account.
    - Request an API key from your account settings.

6.  **Run the data pipeline (only if you want to regenerate the data):**
    - Open `fetch_tmdb_data.py` and paste your API key into the `API_KEY` variable.
    - Run the scripts in order:
      ```bash
      python fetch_tmdb_data.py
      python data_processing.py
      python model_builder.py
      ```

7.  **Launch the app:**
    ```bash
    streamlit run app.py
    ```