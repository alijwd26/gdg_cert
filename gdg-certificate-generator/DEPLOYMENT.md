# 🚀 Deploying to Streamlit Cloud (Free!)

You can run this certificate generator online **without installing Python** using Streamlit Cloud's free hosting.

## Prerequisites

- A GitHub account (free at [github.com](https://github.com))
- A Streamlit Cloud account (free, sign up with GitHub at [share.streamlit.io](https://share.streamlit.io))

## Step-by-Step Deployment Guide

### Step 1: Push Code to GitHub

1. **Create a new repository on GitHub**:
   - Go to [github.com/new](https://github.com/new)
   - Name it: `gdg-certificate-generator`
   - Make it Public
   - Don't initialize with README (we already have one)
   - Click "Create repository"

2. **Upload your files to GitHub**:
   
   **Option A - Using GitHub Web Interface (Easier):**
   - On your new repository page, click "uploading an existing file"
   - Drag and drop ALL files from `C:\Users\Chawi\.gemini\antigravity\scratch\gdg-certificate-generator\`:
     - `app.py`
     - `certificate_generator.py`
     - `requirements.txt`
     - `README.md`
     - `.gitignore`
     - `sample_attendees.csv`
     - `.streamlit/config.toml` (create `.streamlit` folder first if needed)
   - Add commit message: "Initial commit"
   - Click "Commit changes"

   **Option B - Using Git (if you have it installed):**
   ```bash
   cd C:\Users\Chawi\.gemini\antigravity\scratch\gdg-certificate-generator
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/gdg-certificate-generator.git
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Click "Sign in with GitHub"
   - Authorize Streamlit to access your repositories

2. **Create a new app**:
   - Click "New app"
   - Select your repository: `gdg-certificate-generator`
   - Branch: `main`
   - Main file path: `app.py`
   - Click "Deploy!"

3. **Wait for deployment**:
   - Streamlit Cloud will install all dependencies automatically
   - This takes about 2-3 minutes
   - You'll see logs as it builds

4. **Get your app URL**:
   - Once deployed, you'll get a URL like:
   - `https://YOUR_USERNAME-gdg-certificate-generator.streamlit.app`
   - Share this URL with your team!

## Using Your Online App

Once deployed, anyone can access your certificate generator at the URL without installing anything!

### Important Notes

> [!IMPORTANT]
> **Free Tier Limits**: Streamlit Cloud free tier has:
> - Apps sleep after inactivity (wake up when accessed)
> - 1GB memory limit
> - 1 CPU core
> - Should be sufficient for this app!

> [!TIP]
> **Custom Domain**: You can configure a custom domain in Streamlit Cloud settings if you have one.

> [!WARNING]
> **Data Privacy**: Don't upload this to public GitHub if your certificate templates or attendee data are confidential. Use a private repository instead (requires Streamlit Cloud paid plan, or deploy elsewhere).

## Alternative Deployment Options

If you prefer not to use Streamlit Cloud, here are other free options:

### 1. **Hugging Face Spaces** (Free)
   - Sign up at [huggingface.co](https://huggingface.co)
   - Create a new Space (Streamlit type)
   - Upload your files
   - Auto-deploys!

### 2. **Render** (Free tier available)
   - Sign up at [render.com](https://render.com)
   - Connect your GitHub repository
   - Select "Web Service"
   - Build command: `pip install -r requirements.txt`
   - Start command: `streamlit run app.py --server.port=$PORT`

### 3. **Railway** (Free trial)
   - Sign up at [railway.app](https://railway.app)
   - Deploy from GitHub
   - Similar to Render

## Updating Your Deployed App

To update your online app after making changes:

1. **Edit files on GitHub**:
   - Go to your repository
   - Click on any file and click the pencil icon to edit
   - Make changes and commit

2. **Automatic redeployment**:
   - Streamlit Cloud automatically detects changes
   - Redeploys your app within 1-2 minutes

## Troubleshooting

**App won't deploy?**
- Check that all files are uploaded
- Verify `requirements.txt` is present
- Check deployment logs for errors

**Out of memory?**
- Large templates can cause issues
- Try compressing certificate templates before upload
- Keep QR codes reasonably sized

**App is slow?**
- Free tier apps sleep after inactivity
- First access after sleep takes 30-60 seconds to wake up
- Subsequent accesses are fast

**Fonts not loading?**
- Streamlit Cloud has internet access
- Google Fonts download automatically on first use
- Cached for subsequent uses

## Security Considerations

> [!CAUTION]
> **Sensitive Data**: If you're handling sensitive attendee information:
> - Use a private GitHub repository
> - Or deploy to a platform with private deployment options
> - Or run locally after all (with Python installed)

## Quick Start Checklist

- [ ] Create GitHub account
- [ ] Create new repository on GitHub
- [ ] Upload all project files
- [ ] Sign up for Streamlit Cloud
- [ ] Deploy app from your repository
- [ ] Test the deployed app
- [ ] Share the URL with your team!

---

**Need Help?**
- Streamlit Docs: [docs.streamlit.io](https://docs.streamlit.io/streamlit-cloud)
- Community Forum: [discuss.streamlit.io](https://discuss.streamlit.io)

Good luck with your deployment! 🚀
