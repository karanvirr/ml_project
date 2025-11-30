# EC2 Deployment - Quick Reference

Quick commands for deploying and managing AI Mall on AWS EC2.

## 🚀 First Time Setup

```bash
# 1. Connect to EC2
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# 2. Run setup script (copies to EC2 first from local machine)
chmod +x ec2-setup.sh
./ec2-setup.sh

# 3. Log out and back in
exit
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# 4. Clone repository
git clone YOUR_REPO_URL
cd ai-mall-project

# 5. Configure environment
cd backend
echo "GEMINI_API_KEY=your_key_here" > .env
cd ..

# 6. Deploy
docker-compose up -d
```

## 🔄 Updating Application

```bash
# On EC2 - use the deployment script
~/deploy.sh

# OR manually:
cd ~/ai-mall-project
git pull origin main
docker-compose down
docker-compose up -d --build
```

## 📊 Monitoring

```bash
# View logs
docker-compose logs -f

# Container status
docker-compose ps
docker stats

# System resources
htop
df -h
```

## 🛠️ Common Commands

```bash
# Restart containers
docker-compose restart

# Stop containers
docker-compose down

# Start containers
docker-compose up -d

# Rebuild specific service
docker-compose up -d --build backend

# Access container shell
docker-compose exec backend bash

# Clean up Docker
docker system prune -a
```

## 🌐 Access URLs

- Frontend: `http://YOUR_EC2_IP:3000`
- Backend: `http://YOUR_EC2_IP:8000`
- API Docs: `http://YOUR_EC2_IP:8000/docs`

## 🔧 Troubleshooting

```bash
# Container won't start
docker-compose logs
docker-compose down
docker-compose up -d --build

# Port already in use
sudo lsof -i :3000
sudo kill -9 PID

# Restart Docker service
sudo systemctl restart docker
```

## 🔐 Security Group Ports

| Port | Service |
|------|---------|
| 22 | SSH |
| 80 | HTTP |
| 443 | HTTPS |
| 3000 | Frontend |
| 8000 | Backend |

## 📁 File Locations

- Project: `~/ai-mall-project`
- Nginx config: `/etc/nginx/sites-available/aimall`
- Docker compose: `~/ai-mall-project/docker-compose.yml`
- Environment: `~/ai-mall-project/backend/.env`
- Deployment script: `~/deploy.sh`

## ⚡ Quick Deploy Workflow

1. Make changes locally
2. Push to Git: `git push origin main`
3. SSH to EC2: `ssh -i key.pem ubuntu@IP`
4. Run deploy script: `~/deploy.sh`
5. Done! ✅

---

For detailed instructions, see **ec2-deployment-guide.md** in the artifacts folder.
