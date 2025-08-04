#!/bin/bash

# Nosyt AI Prompt Automation - Update Script
# Updates the system to latest version

set -e

echo "🔄 Nosyt AI Prompt Automation - Update Script"
echo "==========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Backup current installation
backup_system() {
    print_info "Creating backup..."
    
    timestamp=$(date +"%Y%m%d_%H%M%S")
    backup_dir="backup_${timestamp}"
    
    mkdir -p "$backup_dir"
    
    # Backup important files
    [ -f ".env" ] && cp .env "$backup_dir/"
    [ -d "data" ] && cp -r data "$backup_dir/"
    [ -d "logs" ] && cp -r logs "$backup_dir/"
    [ -f "*.db" ] && cp *.db "$backup_dir/" 2>/dev/null || true
    
    print_status "Backup created: $backup_dir"
}

# Update from git
update_from_git() {
    print_info "Updating from repository..."
    
    if [ -d ".git" ]; then
        git stash push -m "Auto-stash before update"
        git pull origin main
        print_status "Repository updated"
    else
        print_warning "Not a git repository. Manual update required."
    fi
}

# Update dependencies
update_dependencies() {
    print_info "Updating Python dependencies..."
    
    pip3 install --upgrade -r requirements.txt
    print_status "Dependencies updated"
}

# Migrate database if needed
migrate_database() {
    print_info "Checking database migrations..."
    
    # Run any necessary database migrations
    python3 -c "
from analytics_tracker import AnalyticsTracker
from customer_manager import CustomerManager
from config import Config

config = Config()
analytics = AnalyticsTracker(config)
customer_mgr = CustomerManager(config)

print('Database migrations completed')
" 2>/dev/null || print_warning "Database migration check failed"
    
    print_status "Database checked"
}

# Main update process
main() {
    backup_system
    update_from_git
    update_dependencies
    migrate_database
    
    echo ""
    print_status "Update completed successfully!"
    echo ""
    print_info "Restart the system to apply changes:"
    echo "./start_nosyt.sh"
    echo ""
}

main