#!/bin/bash

# Premium Gastro Deployment Script
echo "🚀 DEPLOYING PREMIUM GASTRO PSYCHOLOGICAL SYSTEM"
echo "=================================================="

# Get Supabase key from 1Password
echo "🔑 Getting Supabase credentials..."
SUPABASE_KEY=$(op read "op://AI/SupabaseAPI/credential")

if [ -z "$SUPABASE_KEY" ]; then
    echo "❌ Failed to get Supabase key from 1Password"
    exit 1
fi

echo "✅ Credentials loaded"

# Create environment file
echo "📝 Creating environment configuration..."
cat > .env << EOF
SUPABASE_URL=https://lowgijppjapmetedkvjb.supabase.co
SUPABASE_KEY=${SUPABASE_KEY}
FLASK_ENV=production
EOF

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data logs

# Build and start services
echo "🐳 Building Docker containers..."
docker-compose down 2>/dev/null
docker-compose build

echo "🚀 Starting Premium Gastro services..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Health check
echo "🏥 Performing health checks..."
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ Web server is healthy"
else
    echo "❌ Web server health check failed"
fi

if curl -f http://localhost:5000/mr-plate/health > /dev/null 2>&1; then
    echo "✅ API server is healthy"
else
    echo "❌ API server health check failed"
fi

echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo "========================"
echo "🌐 Web Interface: http://localhost"
echo "🤖 Mr. Plate API: http://localhost:5000/mr-plate/"
echo "📊 Health Check: http://localhost/health"
echo ""
echo "📋 To view logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 To stop:"
echo "   docker-compose down"