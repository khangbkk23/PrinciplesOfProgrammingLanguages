#!/usr/bin/env pwsh
<#
.SYNOPSIS
    HLang Project Build Script for Windows (PowerShell)

.DESCRIPTION
    This script provides cross-platform build automation for the HLang project.
    It replaces the Makefile functionality with native PowerShell commands.

.PARAMETER Command
    The command to execute. Available commands:
    - help: Show available commands
    - check: Check if required tools are installed
    - setup: Install dependencies and set up environment
    - build: Compile ANTLR grammar files
    - clean: Clean build and external directories
    - clean-cache: Clean Python cache files
    - clean-reports: Clean test reports directory
    - clean-venv: Remove virtual environment
    - test-lexer: Run lexer tests and generate reports
    - test-parser: Run parser tests and generate reports

.EXAMPLE
    .\build.ps1 help
    .\build.ps1 setup
    .\build.ps1 build
#>

param(
    [Parameter(Position = 0)]
    [string]$Command = "help"
)

# Configuration
$EXTERNAL_DIR = Join-Path $PSScriptRoot "external"
$BUILD_DIR = Join-Path $PSScriptRoot "build"
$REPORT_DIR = Join-Path $PSScriptRoot "reports"
$VENV_DIR = Join-Path $PSScriptRoot "venv"

$ANTLR_VERSION = "4.13.2"
$ANTLR_JAR = "antlr-$ANTLR_VERSION-complete.jar"
$ANTLR_URL = "https://www.antlr.org/download/$ANTLR_JAR"

$PYTHON_VERSION = "3.12"

# Color output functions
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    
    if ($Host.UI.SupportsVirtualTerminal -or $env:TERM) {
        $colors = @{
            "Red" = "`e[31m"
            "Green" = "`e[32m"
            "Yellow" = "`e[33m"
            "Blue" = "`e[34m"
            "Reset" = "`e[0m"
        }
        Write-Host "$($colors[$Color])$Message$($colors["Reset"])"
    } else {
        Write-Host $Message -ForegroundColor $Color
    }
}

# Helper functions
function Test-CommandExists {
    param([string]$Command)
    
    try {
        if (Get-Command $Command -ErrorAction Stop) {
            return $true
        }
    } catch {
        return $false
    }
    return $false
}

function Find-Python {
    $candidates = @("python$PYTHON_VERSION", "python", "py")
    
    foreach ($cmd in $candidates) {
        if (Test-CommandExists $cmd) {
            try {
                $version = & $cmd --version 2>&1 | Select-String -Pattern "$PYTHON_VERSION"
                if ($version) {
                    return $cmd
                }
            } catch {
                continue
            }
        }
    }
    
    # Try py launcher with version
    if (Test-CommandExists "py") {
        try {
            $version = & py -$PYTHON_VERSION --version 2>&1 | Select-String -Pattern "$PYTHON_VERSION"
            if ($version) {
                return "py -$PYTHON_VERSION"
            }
        } catch {
            # Ignore
        }
    }
    
    return $null
}

function Get-VenvPython {
    if ($IsWindows -or $env:OS -eq "Windows_NT") {
        return Join-Path $VENV_DIR "Scripts\python.exe"
    } else {
        return Join-Path $VENV_DIR "bin/python"
    }
}

function Get-VenvPip {
    if ($IsWindows -or $env:OS -eq "Windows_NT") {
        return Join-Path $VENV_DIR "Scripts\pip.exe"
    } else {
        return Join-Path $VENV_DIR "bin/pip"
    }
}

# Command implementations
function Show-Help {
    Write-ColorOutput "HLang Project - Available Commands:" "Blue"
    Write-Host ""
    Write-ColorOutput "Setup & Build:" "Green"
    Write-ColorOutput "  .\build.ps1 setup     - Install dependencies and set up environment" "Yellow"
    Write-ColorOutput "  .\build.ps1 build     - Compile ANTLR grammar files" "Yellow"
    Write-ColorOutput "  .\build.ps1 check     - Check if required tools are installed" "Yellow"
    Write-Host ""
    Write-ColorOutput "Testing:" "Green"
    Write-ColorOutput "  .\build.ps1 test-lexer  - Run lexer tests and generate reports" "Yellow"
    Write-ColorOutput "  .\build.ps1 test-parser - Run parser tests and generate reports" "Yellow"
    Write-Host ""
    Write-ColorOutput "Cleaning:" "Green"
    Write-ColorOutput "  .\build.ps1 clean         - Clean build and external directories" "Yellow"
    Write-ColorOutput "  .\build.ps1 clean-cache   - Clean Python cache files" "Yellow"
    Write-ColorOutput "  .\build.ps1 clean-reports - Clean test reports directory" "Yellow"
    Write-ColorOutput "  .\build.ps1 clean-venv    - Remove virtual environment" "Yellow"
    Write-Host ""
    Write-ColorOutput "Environment:" "Green"
    Write-Host "  Virtual environment: $VENV_DIR"
    Write-Host "  Python version required: $PYTHON_VERSION"
    Write-Host "  ANTLR version: $ANTLR_VERSION"
    Write-Host ""
    Write-ColorOutput "Quick start: .\build.ps1 setup; .\build.ps1 build" "Blue"
}

function Test-Dependencies {
    Write-ColorOutput "Checking required dependencies..." "Blue"
    Write-Host ""
    
    # Check Java
    Write-ColorOutput "Checking Java installation..." "Yellow"
    if (Test-CommandExists "java") {
        try {
            $javaVersion = & java -version 2>&1
            Write-ColorOutput "✓ Java is installed" "Green"
        } catch {
            Write-ColorOutput "✗ Java is not working properly" "Red"
            Write-ColorOutput "  Please reinstall Java" "Yellow"
            return $false
        }
    } else {
        Write-ColorOutput "✗ Java is not installed" "Red"
        Write-ColorOutput "  Please install Java manually:" "Yellow"
        Write-ColorOutput "    - Download from https://adoptium.net/ or https://www.oracle.com/java/technologies/downloads/" "Yellow"
        Write-ColorOutput "    - Or use Chocolatey: choco install openjdk" "Yellow"
        Write-ColorOutput "    - Or use Scoop: scoop install openjdk" "Yellow"
        Write-ColorOutput "  Make sure Java is in your PATH" "Yellow"
        return $false
    }
    
    Write-Host ""
    
    # Check Python
    Write-ColorOutput "Checking Python $PYTHON_VERSION installation..." "Yellow"
    $pythonCmd = Find-Python
    if ($pythonCmd) {
        Write-ColorOutput "✓ Python $PYTHON_VERSION found: $pythonCmd" "Green"
    } else {
        Write-ColorOutput "✗ Python $PYTHON_VERSION is not installed or not found" "Red"
        Write-ColorOutput "  Please install Python $PYTHON_VERSION manually:" "Yellow"
        Write-ColorOutput "    - Download from https://www.python.org/downloads/" "Yellow"
        Write-ColorOutput "    - Or use Chocolatey: choco install python --version=$PYTHON_VERSION" "Yellow"
        Write-ColorOutput "    - Or use Scoop: scoop install python" "Yellow"
        Write-ColorOutput "  Make sure Python is in your PATH" "Yellow"
        return $false
    }
    
    Write-Host ""
    Write-ColorOutput "Dependency check completed." "Blue"
    return $true
}

function Setup-Environment {
    Write-ColorOutput "Setting up project environment..." "Blue"
    
    # Create external directory
    if (-not (Test-Path $EXTERNAL_DIR)) {
        New-Item -ItemType Directory -Path $EXTERNAL_DIR -Force | Out-Null
    }
    
    # Check dependencies
    if (-not (Test-Dependencies)) {
        Write-ColorOutput "Setup failed due to missing dependencies." "Red"
        exit 1
    }
    
    $pythonCmd = Find-Python
    
    # Create virtual environment
    Write-ColorOutput "Creating virtual environment..." "Yellow"
    if (-not (Test-Path $VENV_DIR)) {
        & $pythonCmd -m venv $VENV_DIR
        if ($LASTEXITCODE -ne 0) {
            Write-ColorOutput "Failed to create virtual environment." "Red"
            exit 1
        }
        Write-ColorOutput "Virtual environment created at $VENV_DIR" "Green"
    } else {
        Write-ColorOutput "Virtual environment already exists at $VENV_DIR" "Blue"
    }
    
    # Download ANTLR
    Write-ColorOutput "Downloading ANTLR version $ANTLR_VERSION..." "Yellow"
    Write-ColorOutput "This may take a moment..." "Blue"
    
    $antlrPath = Join-Path $EXTERNAL_DIR $ANTLR_JAR
    if (-not (Test-Path $antlrPath)) {
        try {
            Invoke-WebRequest -Uri $ANTLR_URL -OutFile $antlrPath
            Write-ColorOutput "ANTLR downloaded to $antlrPath" "Green"
        } catch {
            Write-ColorOutput "Failed to download ANTLR: $_" "Red"
            exit 1
        }
    } else {
        Write-ColorOutput "ANTLR already exists at $antlrPath" "Blue"
    }
    
    # Upgrade pip
    Write-ColorOutput "Upgrading pip in virtual environment..." "Yellow"
    $venvPip = Get-VenvPip
    & $venvPip install --upgrade pip
    if ($LASTEXITCODE -ne 0) {
        Write-ColorOutput "Failed to upgrade pip." "Red"
        exit 1
    }
    Write-ColorOutput "pip upgraded successfully." "Green"
    
    # Install dependencies
    Write-ColorOutput "Installing Python dependencies in virtual environment..." "Yellow"
    & $venvPip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-ColorOutput "Failed to install Python dependencies." "Red"
        exit 1
    }
    Write-ColorOutput "Python dependencies installed in virtual environment." "Green"
    
    Write-ColorOutput "Setup completed! Virtual environment is ready at $VENV_DIR" "Green"
    Write-ColorOutput "To activate the virtual environment manually:" "Blue"
    if ($IsWindows -or $env:OS -eq "Windows_NT") {
        Write-ColorOutput "  $VENV_DIR\Scripts\Activate.ps1" "Blue"
        Write-ColorOutput "  or: $VENV_DIR\Scripts\activate.bat" "Blue"
    } else {
        Write-ColorOutput "  source $VENV_DIR/bin/activate" "Blue"
    }
}

function Build-Grammar {
    $antlrPath = Join-Path $EXTERNAL_DIR $ANTLR_JAR
    if (-not (Test-Path $antlrPath)) {
        Write-ColorOutput "ANTLR jar not found. Please run 'setup' first." "Red"
        exit 1
    }
    
    # Create build directories
    if (-not (Test-Path $BUILD_DIR)) {
        New-Item -ItemType Directory -Path $BUILD_DIR -Force | Out-Null
    }
    
    $buildSrcDir = Join-Path $BUILD_DIR "src"
    $buildGrammarDir = Join-Path $buildSrcDir "grammar"
    
    if (-not (Test-Path $buildSrcDir)) {
        New-Item -ItemType Directory -Path $buildSrcDir -Force | Out-Null
    }
    
    if (-not (Test-Path $buildGrammarDir)) {
        New-Item -ItemType Directory -Path $buildGrammarDir -Force | Out-Null
    }
    
    # Find grammar files
    $grammarFiles = Get-ChildItem -Path "src/grammar/*.g4" -File
    if ($grammarFiles.Count -eq 0) {
        Write-ColorOutput "No grammar files found in src/grammar/" "Red"
        exit 1
    }
    
    # Compile ANTLR grammar
    Write-ColorOutput "Compiling ANTLR grammar files..." "Yellow"
    $grammarPaths = $grammarFiles | ForEach-Object { $_.FullName }
    & java -jar $antlrPath -Dlanguage=Python3 -visitor -no-listener -o $BUILD_DIR @grammarPaths
    
    if ($LASTEXITCODE -ne 0) {
        Write-ColorOutput "Failed to compile ANTLR grammar files." "Red"
        exit 1
    }
    
    # Create __init__.py files
    Write-ColorOutput "Creating __init__.py files..." "Yellow"
    "" | Out-File -FilePath (Join-Path $BUILD_DIR "__init__.py") -Encoding utf8
    "" | Out-File -FilePath (Join-Path $buildSrcDir "__init__.py") -Encoding utf8
    "" | Out-File -FilePath (Join-Path $buildGrammarDir "__init__.py") -Encoding utf8
    
    # Copy Python files
    Write-ColorOutput "Copying Python files from src/grammar/ to build/src/grammar/" "Yellow"
    $lexererr = Join-Path "src" "grammar" "lexererr.py"
    if (Test-Path $lexererr) {
        Copy-Item $lexererr $buildGrammarDir -Force
    }
    
    Write-ColorOutput "ANTLR grammar files compiled to build/" "Green"
}

function Clean-Cache {
    Write-ColorOutput "Cleaning Python cache files..." "Yellow"
    
    # Remove __pycache__ directories
    Get-ChildItem -Path $PSScriptRoot -Recurse -Directory -Name "__pycache__" | ForEach-Object {
        $fullPath = Join-Path $PSScriptRoot $_
        Remove-Item $fullPath -Recurse -Force -ErrorAction SilentlyContinue
    }
    
    # Remove .pyc files
    Get-ChildItem -Path $PSScriptRoot -Recurse -File -Name "*.pyc" | ForEach-Object {
        $fullPath = Join-Path $PSScriptRoot $_
        Remove-Item $fullPath -Force -ErrorAction SilentlyContinue
    }
    
    # Remove .pytest_cache directories
    Get-ChildItem -Path $PSScriptRoot -Recurse -Directory -Name ".pytest_cache" | ForEach-Object {
        $fullPath = Join-Path $PSScriptRoot $_
        Remove-Item $fullPath -Recurse -Force -ErrorAction SilentlyContinue
    }
    
    Write-ColorOutput "Python cache files cleaned." "Green"
}

function Clean-Reports {
    Write-ColorOutput "Cleaning reports directory..." "Yellow"
    if (Test-Path $REPORT_DIR) {
        Remove-Item $REPORT_DIR -Recurse -Force
    }
    Write-ColorOutput "Reports directory cleaned." "Green"
}

function Clean-Venv {
    Write-ColorOutput "Cleaning virtual environment..." "Yellow"
    if (Test-Path $VENV_DIR) {
        Remove-Item $VENV_DIR -Recurse -Force
    }
    Write-ColorOutput "Virtual environment cleaned." "Green"
}

function Clean-All {
    Write-ColorOutput "Cleaning build and external directories..." "Yellow"
    
    if (Test-Path $BUILD_DIR) {
        Remove-Item $BUILD_DIR -Recurse -Force
    }
    
    if (Test-Path $EXTERNAL_DIR) {
        Remove-Item $EXTERNAL_DIR -Recurse -Force
    }
    
    Write-ColorOutput "Cleaned build and external directories." "Green"
    Clean-Cache
}

function Test-Lexer {
    if (-not (Test-Path $BUILD_DIR)) {
        Write-ColorOutput "Build directory not found. Running build first..." "Yellow"
        Build-Grammar
    }
    
    Write-ColorOutput "Running lexer tests..." "Yellow"
    
    # Clean and create reports directory
    $lexerReportDir = Join-Path $REPORT_DIR "lexer"
    if (Test-Path $lexerReportDir) {
        Remove-Item $lexerReportDir -Recurse -Force
    }
    if (-not (Test-Path $REPORT_DIR)) {
        New-Item -ItemType Directory -Path $REPORT_DIR -Force | Out-Null
    }
    
    # Run tests
    $venvPython = Get-VenvPython
    $env:PYTHONPATH = $PSScriptRoot
    & $venvPython -m pytest tests/test_lexer.py --html="$lexerReportDir/index.html" --timeout=3 --self-contained-html
    
    Write-ColorOutput "Lexer tests completed. Reports generated at $lexerReportDir/index.html" "Green"
    Clean-Cache
}

function Test-Parser {
    if (-not (Test-Path $BUILD_DIR)) {
        Write-ColorOutput "Build directory not found. Running build first..." "Yellow"
        Build-Grammar
    }
    
    Write-ColorOutput "Running parser tests..." "Yellow"
    
    # Clean and create reports directory
    $parserReportDir = Join-Path $REPORT_DIR "parser"
    if (Test-Path $parserReportDir) {
        Remove-Item $parserReportDir -Recurse -Force
    }
    if (-not (Test-Path $REPORT_DIR)) {
        New-Item -ItemType Directory -Path $REPORT_DIR -Force | Out-Null
    }
    
    # Run tests
    $venvPython = Get-VenvPython
    $env:PYTHONPATH = $PSScriptRoot
    & $venvPython -m pytest tests/test_parser.py --html="$parserReportDir/index.html" --timeout=3 --self-contained-html
    
    Write-ColorOutput "Parser tests completed. Reports generated at $parserReportDir/index.html" "Green"
    Clean-Cache
}

# Main execution
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "check" { Test-Dependencies }
    "setup" { Setup-Environment }
    "build" { Build-Grammar }
    "clean" { Clean-All }
    "clean-cache" { Clean-Cache }
    "clean-reports" { Clean-Reports }
    "clean-venv" { Clean-Venv }
    "test-lexer" { Test-Lexer }
    "test-parser" { Test-Parser }
    default {
        Write-ColorOutput "Unknown command: $Command" "Red"
        Write-Host ""
        Show-Help
        exit 1
    }
}
