#!/bin/bash

# Nosyt AI Prompt Automation - One-Click Install Script
# Automatically sets up the complete system

set -e

echo "🤖 Nosyt AI Prompt Automation - One-Click Installer"
echo "================================================="
echo ""
echo "🏢 Nosyt LLC - New Mexico"
echo "📍 Operated from Moncton, NB, Canada"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.8+ first."
        exit 1
    fi
    
    python_version=$(python3 --version | cut -d' ' -f2)
    print_status "Python $python_version found"
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is not installed. Please install pip first."
        exit 1
    fi
    
    print_status "pip3 found"
    
    # Check git
    if ! command -v git &> /dev/null; then
        print_warning "Git not found. Will skip repository cloning."
    else
        print_status "Git found"
    fi
}

# Install system
install_system() {
    print_info "Installing Nosyt AI Automation System..."
    
    # Create directory if not exists
    if [ ! -d "nosyt-ai-prompt-automation" ]; then
        if command -v git &> /dev/null; then
            print_info "Cloning repository..."
            git clone https://github.com/NosytLabs/nosyt-ai-prompt-automation.git
        else
            print_error "Git not available. Please download the repository manually."
            exit 1
        fi
    fi
    
    cd nosyt-ai-prompt-automation
    
    # Install dependencies
    print_info "Installing Python dependencies..."
    pip3 install -r requirements.txt
    print_status "Dependencies installed"
    
    # Setup environment file
    if [ ! -f ".env" ]; then
        print_info "Creating environment configuration..."
        cp .env.example .env
        print_warning "Please edit .env file with your API keys before running!"
    fi
    
    # Create necessary directories
    mkdir -p data logs templates
    print_status "Directories created"
}

# Configure system
configure_system() {
    print_info "System configuration..."
    
    # Check if API keys are configured
    if grep -q "your_openai_api_key_here" .env 2>/dev/null; then
        print_warning "OpenAI API key not configured in .env file"
        echo "Get your API key from: https://platform.openai.com/api-keys"
    fi
    
    if grep -q "your_whop_api_key_here" .env 2>/dev/null; then
        print_warning "WHOP API key not configured in .env file"
        echo "Get your API key from: https://dev.whop.com/"
    fi
}

# Run system check
run_system_check() {
    print_info "Running system health check..."
    
    # Test Python imports
    python3 -c "import asyncio, sqlite3, json, logging" 2>/dev/null
    if [ $? -eq 0 ]; then
        print_status "Core Python modules available"
    else
        print_error "Missing required Python modules"
        exit 1
    fi
    
    # Test optional imports
    python3 -c "import openai" 2>/dev/null
    if [ $? -eq 0 ]; then
        print_status "OpenAI module installed"
    else
        print_warning "OpenAI module not found - install with: pip3 install openai"
    fi
}

# Create startup script
create_startup_script() {
    print_info "Creating startup script..."
    
    cat > start_nosyt.sh << 'EOF'
#!/bin/bash

echo "🤖 Starting Nosyt AI Prompt Automation System..."
echo "Dashboard will be available at: http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

python3 main.py
EOF
    
    chmod +x start_nosyt.sh
    print_status "Startup script created: ./start_nosyt.sh"
}

# Create systemd service (Linux only)
create_systemd_service() {
    if [[ "$OSTYPE" == "linux"* ]]; then
        print_info "Creating systemd service (optional)..."
        
        cat > nosyt-automation.service << EOF
[Unit]
Description=Nosyt AI Prompt Automation
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=$(which python3) main.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=$(pwd)

[Install]
WantedBy=multi-user.target
EOF
        
        print_info "To install as system service:"
        echo "sudo cp nosyt-automation.service /etc/systemd/system/"
        echo "sudo systemctl enable nosyt-automation"
        echo "sudo systemctl start nosyt-automation"
    fi
}

# Display final instructions
show_final_instructions() {
    echo ""
    echo "🎉 Installation Complete! 🎉"
    echo "========================="
    echo ""
    print_status "Nosyt AI Prompt Automation System is ready!"
    echo ""
    print_info "Next Steps:"
    echo "1. Edit .env file with your API keys"
    echo "2. Run: ./start_nosyt.sh (or python3 main.py)"
    echo "3. Open browser to: http://localhost:8000"
    echo "4. Monitor the dashboard for automated operations"
    echo ""
    print_info "Expected Results:"
    echo "• Month 1: $500-2,000 revenue"
    echo "• Month 3: $2,000-5,000 revenue"
    echo "• Month 6: $5,000-15,000 revenue"
    echo ""
    print_info "Support:"
    echo "• Documentation: ./docs/SETUP.md"
    echo "• Email: support@nosyt.com"
    echo "• Discord: [Community Link]"
    echo ""
    print_warning "Important: Configure your API keys in .env before starting!"
    echo ""
    echo "🚀 Ready to build your AI prompt empire? Run: ./start_nosyt.sh"
    echo ""
    echo "Built with ❤️ by Nosyt LLC - New Mexico"
}

# Main installation flow
main() {
    check_prerequisites
    install_system
    configure_system
    run_system_check
    create_startup_script
    create_systemd_service
    show_final_instructions
}

# Run installation
main

echo "🤖 Installation completed successfully!"