# 🍿 PopcornPicks: AI-Powered Movie Recommendation System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://popcornpicks-movie-recommender.streamlit.app/)

PopcornPicks is a feature-rich, interactive web application that provides smart movie recommendations using AI. This project demonstrates a complete end-to-end data science workflow, from data acquisition and processing to machine learning model building and live deployment.

## ✨ Features

- **🤖 AI-Powered Recommendations**: Get personalized movie suggestions based on content-based filtering
- **🔍 Fuzzy Search**: Find movies with intelligent search that handles typos and partial matches
- **📊 Movie Explorer**: Browse and filter 20,000+ movies by genre, year, rating, and more
- **🏆 Curated Collections**: Discover critically acclaimed and highest-grossing movies
- **🎭 Actor & Genre Discovery**: Find movies by your favorite actors or explore specific genres
- **📱 Responsive Design**: Beautiful, modern UI that works on all devices
- **⚡ Fast Performance**: Optimized with KNN models and efficient caching

## 🛠️ Tech Stack

- **Backend & ML**: Python, Pandas, Scikit-learn, TF-IDF Vectorization
- **Web Framework**: Streamlit
- **Data Source**: The Movie Database (TMDb) API
- **Search**: RapidFuzz for fuzzy matching
- **Deployment**: Streamlit Community Cloud

## 🚀 Quick Start

### Option 1: Run the Enhanced Version (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/PopcornPicks-Movie-Recommender.git
   cd PopcornPicks-Movie-Recommender
   ```

2. **Set up environment:**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the enhanced app:**
   ```bash
   streamlit run app_enhanced.py
   ```

### Option 2: One-Click Setup (Enhanced Version)

```bash
python setup_enhanced.py
```

## 📊 Dataset

The enhanced version includes:
- **20,000+ movies** from multiple TMDb endpoints
- **Rich metadata**: Budget, runtime, production countries, cast, crew
- **Enhanced features**: Release decade, rating categories, revenue analysis
- **Optimized processing**: TF-IDF vectorization with 10,000 features

## 🔧 Configuration

### For Local Development

1. **Get TMDb API Key:**
   - Visit [TMDb](https://www.themoviedb.org/) and create a free account
   - Request an API key from your account settings

2. **Update API Key:**
   - Edit `fetch_tmdb_data_enhanced.py` and add your API key
   - Run the data pipeline if you want to regenerate data

### For Deployment

The app is ready for deployment on Streamlit Community Cloud. All necessary files are included and the app will work out of the box.

## 📁 Project Structure

```
PopcornPicks-Movie-Recommender/
├── app_enhanced.py              # Main Streamlit application (enhanced)
├── fetch_tmdb_data_enhanced.py  # Enhanced data fetching script
├── data_processing_enhanced.py  # Enhanced data processing
├── setup_enhanced.py           # One-click setup script
├── requirements.txt            # Python dependencies
├── .streamlit/                 # Streamlit configuration
│   └── config.toml
└── README.md                   # This file
```

## 🚀 Deployment

### Streamlit Community Cloud

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Set main file to `app_enhanced.py`
   - Deploy!

### Other Platforms

The app can also be deployed on:
- **Heroku**: Use the included `Procfile`
- **Railway**: Direct GitHub integration
- **Render**: Web service deployment
- **AWS/GCP/Azure**: Container deployment

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [The Movie Database (TMDb)](https://www.themoviedb.org/) for providing the movie data API
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [RapidFuzz](https://github.com/maxbachmann/RapidFuzz) for fast fuzzy string matching

---

**Made with ❤️ for movie lovers everywhere!**