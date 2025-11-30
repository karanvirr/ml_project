# Docker Deployment Guide for AI Mall

## ✅ **Option 1: Render.com** (Recommended - Free Tier Available)

Render has native Docker support and is the easiest option.

### Prerequisites
1. Create account at [Render.com](https://render.com)
2. Push your code to GitHub
3. Have your Gemini API key ready

### Steps

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml` and create both services

3. **Set Environment Variables:**
   - Go to Backend service → Environment
   - Add: `GEMINI_API_KEY=your_actual_api_key`

4. **Done!** Your app will be live at:
   - Backend: `https://aimall-backend.onrender.com`
   - Frontend: `https://aimall-frontend.onrender.com`

---

## ✅ **Option 2: Railway.app** (Easy Docker Deployment)

Railway also supports Docker natively.

### Steps

1. **Install Railway CLI:**
   ```bash
   npm install -g railway
   ```

2. **Login and Deploy:**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Set Environment Variables:**
   ```bash
   railway variables set GEMINI_API_KEY=your_api_key
   ```

4. **Generate Domain:**
   - Go to Railway dashboard
   - Click on your service → Settings → Generate Domain

---

## ✅ **Option 3: DigitalOcean App Platform**

Supports Docker and has $200 free credit.

### Steps

1. Connect GitHub repository
2. Select "Docker" as build source
3. Configure:
   - **Backend**: Port 8000, Dockerfile path `backend/Dockerfile`
   - **Frontend**: Port 3000, Dockerfile path `frontend/Dockerfile`
4. Add environment variables
5. Deploy!

---

## ✅ **Option 4: AWS (EC2 + Docker)**

For production-grade deployment.

### Steps

1. **Launch EC2 Instance** (Ubuntu 22.04)

2. **Install Docker:**
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose -y
   sudo systemctl start docker
   sudo usermod -aG docker ubuntu
   ```

3. **Clone & Deploy:**
   ```bash
   git clone YOUR_REPO_URL
   cd ai-mall-project
   
   # Create .env file
   echo "GEMINI_API_KEY=your_key" > backend/.env
   
   # Run
   docker-compose up -d
   ```

4. **Configure Security Group:**
   - Allow inbound: Port 3000 (frontend), 8000 (backend)

5. **Access:**
   - Frontend: `http://YOUR_EC2_IP:3000`
   - Backend: `http://YOUR_EC2_IP:8000`

---

## ✅ **Option 5: Google Cloud Run**

Serverless container platform.

### Steps

1. **Install gcloud CLI**

2. **Build & Push Images:**
   ```bash
   # Backend
   gcloud builds submit --tag gcr.io/YOUR_PROJECT/aimall-backend ./backend
   gcloud run deploy aimall-backend --image gcr.io/YOUR_PROJECT/aimall-backend
   
   # Frontend
   gcloud builds submit --tag gcr.io/YOUR_PROJECT/aimall-frontend ./frontend
   gcloud run deploy aimall-frontend --image gcr.io/YOUR_PROJECT/aimall-frontend
   ```

3. **Set Environment Variables:**
   ```bash
   gcloud run services update aimall-backend \
     --set-env-vars GEMINI_API_KEY=your_key
   ```

---

## 📋 **Pre-Deployment Checklist**

- [ ] `.env` file has valid Gemini API key
- [ ] Backend Dockerfile is production-ready
- [ ] Frontend has correct API URL
- [ ] All dependencies in requirements.txt
- [ ] Data files are accessible (mounted or in container)
- [ ] CORS configured for production domain

---

## 🔧 **Production Optimizations**

### Update Backend Dockerfile for Production

```dockerfile
FROM python:3.10-slim
WORKDIR /app

# Copy requirements first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Production command (no --reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Update Frontend for Production

Make sure frontend knows where backend is:
- Create `.env` in frontend:
  ```
  REACT_APP_API_URL=https://your-backend-url.com
  ```

- Update axios base URL in frontend code

---

## 🎯 **Recommended for You: Render.com**

Based on your setup, I recommend **Render.com** because:
- ✅ Native Docker support
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Easy environment variable management
- ✅ Auto-deploys on GitHub push
- ✅ No credit card required for free tier

---

## 🚀 **Quick Start with Render**

1. Create `render.yaml` (already provided above)
2. Push to GitHub
3. Connect to Render
4. Add GEMINI_API_KEY
5. Deploy! 🎉

Your app will be live in minutes!
