---
description: Deploy AI Mall to AWS EC2
---

# Deploy AI Mall to AWS EC2

This workflow guides you through deploying the AI Mall application to AWS EC2 using Docker.

## Prerequisites

Before starting:
- [ ] AWS account with EC2 access
- [ ] SSH key pair for EC2
- [ ] Gemini API key
- [ ] Code pushed to Git repository

## Steps

### 1. Launch EC2 Instance

**In AWS Console:**
1. Go to EC2 Dashboard → Launch Instance
2. Select **Ubuntu 22.04 LTS** AMI
3. Choose instance type:
   - Development: `t2.micro` (free tier)
   - Production: `t2.medium` (recommended)
4. Configure storage: 20GB minimum
5. Configure Security Group with these ports:
   - SSH (22) - Your IP only
   - HTTP (80) - 0.0.0.0/0
   - HTTPS (443) - 0.0.0.0/0
   - Custom TCP (3000) - 0.0.0.0/0 (Frontend)
   - Custom TCP (8000) - 0.0.0.0/0 (Backend)
6. Select or create SSH key pair
7. Launch instance

### 2. Connect to EC2

```bash
ssh -i /path/to/your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### 3. Run Initial Setup Script

Upload and run the setup script:

```bash
# On your local machine, copy the setup script
scp -i /path/to/your-key.pem ec2-setup.sh ubuntu@YOUR_EC2_IP:~/

# On EC2 instance
chmod +x ~/ec2-setup.sh
./ec2-setup.sh

# Log out and back in for group changes
exit
ssh -i /path/to/your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### 4. Clone Repository

```bash
cd ~/projects
git clone YOUR_REPOSITORY_URL
cd ai-mall-project
```

### 5. Configure Environment

```bash
# Create .env file
cd backend
cat > .env << EOF
GEMINI_API_KEY=your_actual_gemini_api_key
EOF
cd ..
```

### 6. Deploy Application

// turbo
```bash
docker-compose up -d
```

### 7. Verify Deployment

```bash
# Check containers are running
docker-compose ps

# View logs
docker-compose logs -f

# Test access
curl http://localhost:8000/health
```

### 8. Access Application

Open in browser:
- Frontend: `http://YOUR_EC2_IP:3000`
- Backend: `http://YOUR_EC2_IP:8000`
- API Docs: `http://YOUR_EC2_IP:8000/docs`

## Production Setup (Optional)

### Enable Nginx Reverse Proxy

```bash
# Copy nginx config
sudo cp nginx.conf /etc/nginx/sites-available/aimall

# Enable site
sudo ln -s /etc/nginx/sites-available/aimall /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

### Enable HTTPS (if you have a domain)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

## Future Deployments

For updates, use the deployment script:

```bash
# Copy deploy script to EC2
scp -i /path/to/your-key.pem deploy.sh ubuntu@YOUR_EC2_IP:~/

# Make executable
chmod +x ~/deploy.sh

# Run updates
~/deploy.sh
```

## Troubleshooting

**Containers won't start:**
```bash
docker-compose logs
docker-compose down
docker-compose up -d --build
```

**Can't access application:**
1. Check security group allows ports 3000, 8000, 80, 443
2. Verify containers are running: `docker ps`
3. Check logs: `docker-compose logs`

**Need to restart:**
```bash
docker-compose restart
```

For detailed troubleshooting, see the full deployment guide in `ec2-deployment-guide.md`.
