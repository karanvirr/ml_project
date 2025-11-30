#!/bin/bash
# Deployment automation script for AI Mall on EC2
# Place this in your home directory on EC2 and run after initial setup

set -e

# Configuration
PROJECT_DIR="$HOME/ai-mall-project"  # Adjust if needed
BRANCH="main"  # or "master"

echo "🚀 Starting AI Mall Deployment..."
echo "=================================="

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Error: Project directory not found at $PROJECT_DIR"
    echo "Please clone your repository first:"
    echo "  git clone YOUR_REPO_URL $PROJECT_DIR"
    exit 1
fi

# Navigate to project
cd "$PROJECT_DIR"

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Warning: backend/.env not found!"
    echo "Creating template .env file..."
    cat > backend/.env << EOF
# Gemini API Configuration
GEMINI_API_KEY=your_api_key_here
EOF
    echo "❌ Please edit backend/.env with your actual API key and run this script again"
    exit 1
fi

# Pull latest changes
echo "📥 Pulling latest code from $BRANCH..."
git fetch origin
git pull origin $BRANCH

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Remove old images (optional - uncomment to clean up)
# echo "🧹 Cleaning up old images..."
# docker-compose down --rmi all

# Build fresh images
echo "🔨 Building Docker images..."
docker-compose build --no-cache

# Start containers
echo "▶️  Starting containers..."
docker-compose up -d

# Wait for containers to start
echo "⏳ Waiting for containers to start..."
sleep 5

# Check container status
echo "📊 Container status:"
docker-compose ps

# Show logs (last 20 lines)
echo ""
echo "📋 Recent logs:"
docker-compose logs --tail=20

# Get public IP
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)

echo ""
echo "=================================="
echo "✅ Deployment Complete!"
echo "=================================="
echo ""
echo "Your application is running at:"
echo "  Frontend: http://$PUBLIC_IP:3000"
echo "  Backend:  http://$PUBLIC_IP:8000"
echo "  API Docs: http://$PUBLIC_IP:8000/docs"
echo ""
echo "To view live logs, run:"
echo "  docker-compose logs -f"
echo ""
