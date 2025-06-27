#!/usr/bin/env python3
"""
Deployment script for LLM Stock Analyst backend
"""

import os
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    
    # Check if .env file exists
    if not Path(".env").exists():
        print("❌ .env file not found. Please create one with your API keys.")
        return False
    
    print("✅ Requirements check passed")
    return True

def deploy_to_railway():
    """Deploy to Railway"""
    print("🚀 Deploying to Railway...")
    
    try:
        # Check if Railway CLI is installed
        result = subprocess.run(["railway", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Railway CLI not found. Please install it first:")
            print("   npm install -g @railway/cli")
            return False
        
        # Login to Railway
        print("📝 Logging in to Railway...")
        subprocess.run(["railway", "login"], check=True)
        
        # Initialize project
        print("🔧 Initializing Railway project...")
        subprocess.run(["railway", "init"], check=True)
        
        # Deploy
        print("🚀 Deploying...")
        subprocess.run(["railway", "up"], check=True)
        
        print("✅ Deployment successful!")
        print("📋 Next steps:")
        print("   1. Go to Railway dashboard")
        print("   2. Add environment variables")
        print("   3. Get your deployment URL")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Railway deployment failed: {e}")
        return False

def deploy_to_render():
    """Deploy to Render"""
    print("🚀 Deploying to Render...")
    
    print("📋 Manual deployment required for Render:")
    print("   1. Go to https://render.com")
    print("   2. Create a new Web Service")
    print("   3. Connect your GitHub repository")
    print("   4. Set build command: pip install -r backend/requirements.txt")
    print("   5. Set start command: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT")
    print("   6. Add environment variables")
    print("   7. Deploy")
    
    return True

def deploy_to_heroku():
    """Deploy to Heroku"""
    print("🚀 Deploying to Heroku...")
    
    try:
        # Check if Heroku CLI is installed
        result = subprocess.run(["heroku", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Heroku CLI not found. Please install it first:")
            print("   https://devcenter.heroku.com/articles/heroku-cli")
            return False
        
        # Login to Heroku
        print("📝 Logging in to Heroku...")
        subprocess.run(["heroku", "login"], check=True)
        
        # Create app
        app_name = input("Enter Heroku app name (or press Enter for auto-generated): ").strip()
        if app_name:
            subprocess.run(["heroku", "create", app_name], check=True)
        else:
            subprocess.run(["heroku", "create"], check=True)
        
        # Set environment variables
        print("🔧 Setting environment variables...")
        env_vars = [
            "OPENAI_API_KEY",
            "OPENAI_MODEL",
            "POWERBI_CLIENT_ID",
            "POWERBI_CLIENT_SECRET",
            "POWERBI_TENANT_ID",
            "POWERBI_WORKSPACE_ID"
        ]
        
        for var in env_vars:
            value = os.getenv(var)
            if value:
                subprocess.run(["heroku", "config:set", f"{var}={value}"], check=True)
                print(f"   ✅ Set {var}")
            else:
                print(f"   ⚠️  {var} not found in .env file")
        
        # Deploy
        print("🚀 Deploying...")
        subprocess.run(["git", "push", "heroku", "main"], check=True)
        
        print("✅ Deployment successful!")
        print("📋 Your app URL:")
        subprocess.run(["heroku", "open"], check=True)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Heroku deployment failed: {e}")
        return False

def test_local_backend():
    """Test the local backend"""
    print("🧪 Testing local backend...")
    
    try:
        # Change to backend directory
        os.chdir("backend")
        
        # Install dependencies
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        
        # Start the server
        print("🚀 Starting local server...")
        print("   Press Ctrl+C to stop")
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--reload", "--port", "8000"], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Local test failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        return True

def main():
    """Main deployment function"""
    print("🚀 LLM Stock Analyst - Backend Deployment")
    print("=" * 50)
    
    if not check_requirements():
        return
    
    print("\n📋 Choose deployment option:")
    print("1. Deploy to Railway (Recommended)")
    print("2. Deploy to Render")
    print("3. Deploy to Heroku")
    print("4. Test local backend")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        deploy_to_railway()
    elif choice == "2":
        deploy_to_render()
    elif choice == "3":
        deploy_to_heroku()
    elif choice == "4":
        test_local_backend()
    elif choice == "5":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main() 