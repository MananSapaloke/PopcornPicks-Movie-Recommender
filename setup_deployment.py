#!/usr/bin/env python3
"""
Deployment setup script for PopcornPicks
This script generates the necessary data files for deployment
"""

import os
import sys
import subprocess
import pandas as pd
from pathlib import Path

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        'fetch_tmdb_data_enhanced.py',
        'data_processing_enhanced.py',
        'app_enhanced.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def main():
    """Main deployment setup"""
    print("🚀 PopcornPicks Deployment Setup")
    print("=" * 50)
    
    # Check required files
    if not check_required_files():
        sys.exit(1)
    
    # Step 1: Fetch data
    if not run_script('fetch_tmdb_data_enhanced.py', 'Fetching TMDB data'):
        print("⚠️  Data fetching failed, but continuing...")
    
    # Step 2: Process data
    if not run_script('data_processing_enhanced.py', 'Processing data and building model'):
        print("❌ Data processing failed - deployment cannot continue")
        sys.exit(1)
    
    # Check if essential files were created
    essential_files = [
        'processed_tmdb_enhanced_dataset.csv',
        'tmdb_tfidf_vectorizer.pkl'
    ]
    
    missing_essential = []
    for file in essential_files:
        if not os.path.exists(file):
            missing_essential.append(file)
    
    if missing_essential:
        print(f"❌ Essential files not created: {missing_essential}")
        sys.exit(1)
    
    print("\n🎉 Deployment setup completed successfully!")
    print("📁 Essential files created:")
    for file in essential_files:
        size = os.path.getsize(file) / (1024 * 1024)  # MB
        print(f"   - {file} ({size:.1f} MB)")
    
    print("\n🚀 Ready for deployment!")

if __name__ == "__main__":
    main()
