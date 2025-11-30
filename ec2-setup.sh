#!/bin/bash
# EC2 Initial Setup Script for AI Mall
# Run this script on a fresh Ubuntu 22.04 EC2 instance

set -e

echo "================================================"
echo "   AI Mall - EC2 Setup Script"
echo "================================================"
echo ""

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm get-docker.sh

# Install Docker Compose
echo "🔧 Installing Docker Compose..."
sudo apt install docker-compose -y

# Add current user to docker group
echo "👤 Adding user to docker group..."
sudo usermod -aG docker $USER

# Start and enable Docker
echo "▶️  Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

# Install additional utilities
echo "🛠️  Installing utilities..."
sudo apt install -y git htop curl wget nano

# Install nginx (optional, comment out if not needed)
echo "🌐 Installing Nginx..."
sudo apt install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Create project directory
echo "📁 Creating project directory..."
mkdir -p ~/projects
cd ~/projects

echo ""
echo "================================================"
echo "✅ Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Log out and log back in for docker group changes"
echo "2. Clone your repository: git clone YOUR_REPO_URL"
echo "3. Configure environment variables"
echo "4. Run: docker-compose up -d"
echo ""
echo "Important: You MUST log out and log back in!"
echo "Run: exit"
echo ""
