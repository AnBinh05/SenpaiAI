#!/bin/bash
# SenpaiAI Installation Script for Linux/Mac

echo ""
echo "========================================"
echo "  SenpaiAI Installation Script"
echo "========================================"
echo ""

# Check Python
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.10+ first"
    exit 1
fi
python3 --version
echo "✅ Python found"

# Check Node.js
echo ""
echo "[2/5] Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi
node --version
echo "✅ Node.js found"

# Setup Backend
echo ""
echo "[3/5] Setting up Backend..."
cd backend || exit 1

# Create virtual environment if not exists
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install backend dependencies"
    cd ..
    exit 1
fi

echo "✅ Backend dependencies installed"

# Create .env file if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit backend/.env to configure your settings"
fi

cd ..

# Setup Frontend
echo ""
echo "[4/5] Setting up Frontend..."
cd frontend || exit 1

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install frontend dependencies"
    cd ..
    exit 1
fi

echo "✅ Frontend dependencies installed"

# Create .env file if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp env.example .env
fi

cd ..

# Summary
echo ""
echo "========================================"
echo "  Installation Complete!"
echo "========================================"
echo ""
echo "✅ Backend: Dependencies installed in backend/.venv"
echo "✅ Frontend: Dependencies installed in frontend/node_modules"
echo ""
echo "📝 Next steps:"
echo "   1. Edit backend/.env if needed"
echo "   2. Edit frontend/.env if needed"
echo "   3. Run ./start.sh to start the application"
echo ""
echo "💡 To activate backend virtual environment manually:"
echo "   cd backend"
echo "   source .venv/bin/activate"
echo ""







