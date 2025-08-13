@echo off
REM 🧠 Memory Context Manager v2 - Easy Setup Script for Windows
REM This script makes it super easy to get your brain-enhanced AI running on Windows!

setlocal enabledelayedexpansion

REM Colors for output (Windows 10+)
set "BLUE=[94m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "NC=[0m"

REM Function to print colored output
:print_status
echo %BLUE%🔧 %~1%NC%
goto :eof

:print_success
echo %GREEN%✅ %~1%NC%
goto :eof

:print_warning
echo %YELLOW%⚠️  %~1%NC%
goto :eof

:print_error
echo %RED%❌ %~1%NC%
goto :eof

:print_header
echo %BLUE%
echo 🧠 Memory Context Manager v2 - Easy Setup for Windows
echo ======================================================
echo %NC%
goto :eof

REM Check if Docker is installed and running
:check_docker
call :print_status "Checking Docker installation..."

docker --version >nul 2>&1
if errorlevel 1 (
    call :print_error "Docker is not installed!"
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
    call :print_error "Docker is not running!"
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

call :print_success "Docker is ready!"
goto :eof

REM Check if required files exist
:check_files
call :print_status "Checking required files..."

set "required_files=docker-compose-shareable.yml Dockerfile.shareable main.py pyproject.toml"

for %%f in (%required_files%) do (
    if not exist "%%f" (
        call :print_error "Missing required file: %%f"
        pause
        exit /b 1
    )
)

call :print_success "All required files found!"
goto :eof

REM Build and start services
:start_services
call :print_status "Building and starting services..."

REM Stop any existing containers
docker-compose -f docker-compose-shareable.yml down >nul 2>&1

REM Build the containers
call :print_status "Building containers (this may take a few minutes)..."
docker-compose -f docker-compose-shareable.yml build
if errorlevel 1 (
    call :print_error "Failed to build containers"
    pause
    exit /b 1
)

REM Start services
call :print_status "Starting services..."
docker-compose -f docker-compose-shareable.yml up -d
if errorlevel 1 (
    call :print_error "Failed to start services"
    pause
    exit /b 1
)

call :print_success "Services started successfully!"
goto :eof

REM Wait for services to be ready
:wait_for_services
call :print_status "Waiting for services to be ready..."

REM Wait for Ollama
call :print_status "Waiting for Ollama service..."
set "max_attempts=30"
for /l %%i in (1,1,%max_attempts%) do (
    curl -s http://localhost:11434/api/tags >nul 2>&1
    if not errorlevel 1 (
        call :print_success "Ollama service is ready!"
        goto :ollama_ready
    )
    
    if %%i==%max_attempts% (
        call :print_error "Ollama service failed to start"
        pause
        exit /b 1
    )
    
    echo    Attempt %%i/%max_attempts%... (waiting 10 seconds)
    timeout /t 10 /nobreak >nul
)

:ollama_ready
REM Wait for model setup to complete
call :print_status "Waiting for AI models to download..."
echo 📥 This may take 10-20 minutes depending on your internet connection...

set "max_attempts=120"
for /l %%i in (1,1,%max_attempts%) do (
    docker-compose -f docker-compose-shareable.yml ps model_setup | findstr "exited (0)" >nul
    if not errorlevel 1 (
        call :print_success "AI models downloaded successfully!"
        goto :models_ready
    )
    
    docker-compose -f docker-compose-shareable.yml ps model_setup | findstr "exited (" >nul
    if not errorlevel 1 (
        call :print_error "Model download failed"
        pause
        exit /b 1
    )
    
    if %%i==%max_attempts% (
        call :print_warning "Model download taking longer than expected, continuing anyway..."
        goto :models_ready
    )
    
    echo    Still downloading models... (%%i/%max_attempts% - waiting 1 minute)
    timeout /t 60 /nobreak >nul
)

:models_ready
goto :eof

REM Test the installation
:test_installation
call :print_status "Testing installation..."

REM Test Ollama
curl -s http://localhost:11434/api/tags >nul 2>&1
if not errorlevel 1 (
    call :print_success "Ollama is responding"
) else (
    call :print_error "Ollama is not responding"
)

REM Test Web UI
curl -s http://localhost:3000 >nul 2>&1
if not errorlevel 1 (
    call :print_success "Web UI is accessible"
) else (
    call :print_warning "Web UI is not accessible (this is optional)"
)

REM Test MCP server container
docker-compose -f docker-compose-shareable.yml ps memory_mcp_server | findstr "Up" >nul
if not errorlevel 1 (
    call :print_success "MCP server container is running"
) else (
    call :print_error "MCP server container is not running"
)
goto :eof

REM Show usage information
:show_usage
echo.
echo %GREEN%🎉 SETUP COMPLETE! 🎉%NC%
echo.
echo 📋 Your services are running:
echo    🤖 Ollama LLM:        http://localhost:11434
echo    🌐 Web UI:            http://localhost:3000
echo    🧠 MCP Server:        Container 'memory_mcp_server_shared'
echo.
echo 🔧 Useful commands:
echo    View logs:            docker-compose -f docker-compose-shareable.yml logs -f
echo    Stop services:        docker-compose -f docker-compose-shareable.yml down
echo    Restart services:     docker-compose -f docker-compose-shareable.yml up -d
echo    Shell into MCP:       docker-compose -f docker-compose-shareable.yml exec memory_mcp_server_shared bash
echo.
echo 🧠 Test your memory system:
echo    1. Connect to your MCP server
echo    2. Run: test_memory_system
echo    3. Run: ai_chat_with_memory --user_message "Hi, I'm testing the memory system!"
echo.
echo 🌐 Access Web UI at: http://localhost:3000
echo    - Chat directly with the LLM
echo    - Test different models
echo    - Monitor performance
echo.
echo 🔍 Check service status: docker-compose -f docker-compose-shareable.yml ps
echo.
echo %BLUE%🎯 Next steps:%NC%
echo 1. Your memory-enhanced AI is ready!
echo 2. Connect to your MCP server and test the memory features
echo 3. Use ai_chat_with_memory to chat with memory-enhanced AI
echo 4. Visit http://localhost:3000 for direct LLM interaction
goto :eof

REM Main function
:main
call :print_header

call :check_docker
if errorlevel 1 exit /b 1

call :check_files
if errorlevel 1 exit /b 1

call :start_services
if errorlevel 1 exit /b 1

call :wait_for_services
if errorlevel 1 exit /b 1

call :test_installation
if errorlevel 1 exit /b 1

call :show_usage

echo.
echo Press any key to exit...
pause >nul
exit /b 0

REM Start the main function
call :main
