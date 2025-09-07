# 🚀 Deployment Guide for PopcornPicks

This guide will help you deploy your PopcornPicks movie recommender app to various hosting platforms.

## 📋 Pre-Deployment Checklist

✅ **Files Ready for Deployment:**
- `app_enhanced.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `.streamlit/config.toml` - Streamlit configuration
- `Procfile` - For Heroku deployment
- `runtime.txt` - Python version specification
- Data files: `processed_tmdb_enhanced_dataset.csv`, `tmdb_tfidf_vectorizer.pkl`

## 🌐 Deployment Options

### Option 1: Streamlit Community Cloud (Recommended)

**Pros:** Free, easy, designed for Streamlit apps
**Cons:** Limited to Streamlit apps only

#### Steps:
1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - PopcornPicks Movie Recommender"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/PopcornPicks-Movie-Recommender.git
   git push -u origin main
   ```

2. **Deploy on Streamlit:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `YOUR_USERNAME/PopcornPicks-Movie-Recommender`
   - Set main file: `app_enhanced.py`
   - Click "Deploy!"

3. **Your app will be live at:**
   `https://YOUR_APP_NAME.streamlit.app/`

### Option 2: Heroku

**Pros:** Supports multiple frameworks, good free tier
**Cons:** Requires credit card for verification

#### Steps:
1. **Install Heroku CLI** from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login and create app:**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Deploy:**
   ```bash
   git push heroku main
   ```

4. **Open your app:**
   ```bash
   heroku open
   ```

### Option 3: Railway

**Pros:** Modern platform, easy GitHub integration
**Cons:** Limited free tier

#### Steps:
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `streamlit run app_enhanced.py --server.port=$PORT --server.address=0.0.0.0`
5. Deploy!

### Option 4: Render

**Pros:** Good free tier, easy setup
**Cons:** Cold starts can be slow

#### Steps:
1. Go to [render.com](https://render.com)
2. Connect GitHub repository
3. Create new Web Service
4. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app_enhanced.py --server.port=$PORT --server.address=0.0.0.0`
5. Deploy!

## 🔧 Environment Variables (if needed)

If you need to add API keys or other secrets:

### For Streamlit Community Cloud:
Create a `secrets.toml` file in `.streamlit/` folder:
```toml
[secrets]
TMDB_API_KEY = "your_api_key_here"
```

### For other platforms:
Set environment variables in your platform's dashboard:
- `TMDB_API_KEY=your_api_key_here`

## 📊 Performance Optimization

### For Large Datasets:
1. **Use Git LFS** for large files:
   ```bash
   git lfs install
   git lfs track "*.pkl"
   git lfs track "*.csv"
   git add .gitattributes
   ```

2. **Optimize data loading:**
   - The app already uses `@st.cache_resource` for efficient caching
   - Consider data compression for very large datasets

## 🐛 Troubleshooting

### Common Issues:

1. **"Module not found" errors:**
   - Check `requirements.txt` includes all dependencies
   - Ensure Python version compatibility

2. **Memory errors:**
   - The app is optimized with KNN models to avoid memory issues
   - If still occurring, consider reducing dataset size

3. **Slow loading:**
   - First load may be slow due to data processing
   - Subsequent loads will be faster due to caching

4. **Streamlit deployment fails:**
   - Ensure main file is `app_enhanced.py`
   - Check that all required files are in the repository
   - Verify `requirements.txt` is in the root directory

## 🎯 Recommended Deployment Flow

1. **Start with Streamlit Community Cloud** (easiest)
2. **Test thoroughly** on the deployed version
3. **Share the link** with friends and get feedback
4. **Consider other platforms** if you need more control or features

## 📈 Post-Deployment

After successful deployment:

1. **Test all features** on the live app
2. **Share your app** on social media
3. **Monitor performance** and user feedback
4. **Update regularly** with new features or data

## 🔗 Useful Links

- [Streamlit Community Cloud](https://share.streamlit.io)
- [Heroku Documentation](https://devcenter.heroku.com/)
- [Railway Documentation](https://docs.railway.app/)
- [Render Documentation](https://render.com/docs)

---

**Happy Deploying! 🚀**
