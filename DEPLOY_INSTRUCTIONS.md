# 🚀 Quick Deployment Instructions

## For Streamlit Community Cloud:

1. **Push to GitHub** (already done)
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Connect your GitHub repository**
4. **Set these deployment settings:**
   - **Main file path:** `app_enhanced.py`
   - **Python version:** 3.11
   - **Requirements file:** `requirements.txt`

5. **Add this to your Streamlit secrets** (if you have a TMDB API key):
   ```
   [secrets]
   TMDB_API_KEY = "your_api_key_here"
   ```

## For Heroku:

1. **Install Heroku CLI**
2. **Run these commands:**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

## For Railway:

1. **Connect your GitHub repo**
2. **Set build command:** `python setup_deployment.py`
3. **Set start command:** `streamlit run app_enhanced.py --server.port=$PORT --server.address=0.0.0.0`

## Data Generation:

The app will automatically generate the required data files on first run using:
- `fetch_tmdb_data_enhanced.py` - Fetches movie data
- `data_processing_enhanced.py` - Processes data and builds ML model

**Note:** First deployment may take 10-15 minutes due to data fetching and processing.
