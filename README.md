# HLang Compiler Project

A comprehensive compiler implementation for HLang, a simple programming language, using the ANTLR4 parser generator.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![ANTLR](https://img.shields.io/badge/ANTLR-4.13.2-orange.svg)](https://www.antlr.org/)
[![License](https://img.shields.io/badge/License-Academic-green.svg)](LICENSE)

## Overview

This is a mini project for the **Principle of Programming Languages course (CO3005)** at Ho Chi Minh City University of Technology (VNU-HCM) that implements a compiler for **HLang**, a custom programming language designed for educational purposes.

The project demonstrates fundamental concepts of compiler construction including:
- **Lexical Analysis**: Tokenization and error handling for invalid characters, unclosed strings, and illegal escape sequences
- **Syntax Analysis**: Grammar-based parsing using ANTLR4 (ANother Tool for Language Recognition)
- **Error Handling**: Comprehensive error reporting for both lexical and syntactic errors
- **Testing Framework**: Automated testing with HTML report generation

## Project Structure

```
.
├── Makefile              # Cross-platform build automation (Windows, macOS, Linux)
├── run.py                # Main project entrypoint for build and test operations
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
├── venv/                 # Python virtual environment (auto-generated)
├── build/                # Generated parser and lexer code
│   └── src/
│       └── grammar/      # Compiled ANTLR4 output
│           ├── HLangLexer.py      # Generated lexer
│           ├── HLangParser.py     # Generated parser  
│           ├── HLangVisitor.py    # Generated visitor
│           └── *.tokens           # Token definitions
├── external/             # External dependencies
│   └── antlr-4.13.2-complete.jar # ANTLR4 tool
├── reports/              # Automated test reports (HTML format)
│   ├── lexer/            # Lexer test reports with coverage
│   └── parser/           # Parser test reports with coverage
├── src/                  # Source code
│   └── grammar/          # Grammar definitions
│       ├── HLang.g4      # ANTLR4 grammar specification
│       └── lexererr.py   # Custom lexer error classes
└── tests/                # Comprehensive test suite
    ├── test_lexer.py     # Lexer functionality tests
    ├── test_parser.py    # Parser functionality tests
    └── utils.py          # Testing utilities and helper classes
```


## Setup and Usage

### Prerequisites

- **Python 3.12+** (recommended) or Python 3.8+
- **Java Runtime Environment (JRE) 8+** (required for ANTLR4)
- **Git** (for cloning the repository)

The project includes a comprehensive Makefile that supports:
- ✅ **Windows** (PowerShell/CMD)
- ✅ **macOS** (Terminal/Zsh/Bash)  
- ✅ **Linux** (Bash/Zsh)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd project
   ```

2. **Check system requirements:**
   ```bash
   make check
   # OR using the entrypoint script:
   # Windows:
   python run.py check
   # macOS/Linux:
   python3 run.py check
   ```

3. **Set up the environment and install dependencies:**
   ```bash
   make setup
   # OR using the entrypoint script:
   # Windows:
   python run.py setup
   # macOS/Linux:
   python3 run.py setup
   ```
   This command:
   - Creates a Python virtual environment
   - Installs required Python packages
   - Downloads ANTLR4 JAR file automatically

4. **Activate the virtual environment (REQUIRED before building and testing):**
   ```bash
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

5. **Build the compiler:**
   ```bash
   make build
   # OR using the entrypoint script:
   # Windows:
   python run.py build
   # macOS/Linux:
   python3 run.py build
   ```

6. **Run tests:**
   ```bash
   make test-lexer   # Test lexical analysis
   make test-parser  # Test syntax analysis
   # OR using the entrypoint script:
   # Windows:
   python run.py test-lexer
   python run.py test-parser
   # macOS/Linux:
   python3 run.py test-lexer
   python3 run.py test-parser
   ```

### Available Commands

**Using Makefile (recommended):**
```bash
make help  # Get a full list of available commands
```

**Using run.py entrypoint:**
```bash
# Windows:
python run.py help         # Get help for run.py commands
python run.py setup        # Setup environment
python run.py build        # Build compiler
python run.py test-lexer   # Test lexer
python run.py test-parser  # Test parser
python run.py clean        # Clean build files

# macOS/Linux:
python3 run.py help        # Get help for run.py commands
python3 run.py setup       # Setup environment
python3 run.py build       # Build compiler
python3 run.py test-lexer  # Test lexer
python3 run.py test-parser # Test parser
python3 run.py clean       # Clean build files
```

> **⚠️ Important**: Always activate the virtual environment before running build and test commands:
> ```bash
> # On macOS/Linux:
> source venv/bin/activate
> 
> # On Windows:
> venv\Scripts\activate
> ```

#### Setup & Build Commands
- `make setup` or `python run.py setup` (Windows) / `python3 run.py setup` (macOS/Linux) - Install dependencies and set up environment  
- `make build` or `python run.py build` (Windows) / `python3 run.py build` (macOS/Linux) - Compile ANTLR grammar files to Python code
- `make check` or `python run.py check` (Windows) / `python3 run.py check` (macOS/Linux) - Verify required tools are installed

#### Testing Commands  
- `make test-lexer` or `python run.py test-lexer` (Windows) / `python3 run.py test-lexer` (macOS/Linux) - Run lexer tests with HTML report generation
- `make test-parser` or `python run.py test-parser` (Windows) / `python3 run.py test-parser` (macOS/Linux) - Run parser tests with HTML report generation

#### Maintenance Commands
- `make clean` or `python run.py clean` (Windows) / `python3 run.py clean` (macOS/Linux) - Remove build directories
- `make clean-cache` or `python run.py clean-cache` (Windows) / `python3 run.py clean-cache` (macOS/Linux) - Clean Python cache files (__pycache__, .pyc)
- `make clean-reports` or `python run.py clean-reports` (Windows) / `python3 run.py clean-reports` (macOS/Linux) - Remove generated test reports
- `make clean-venv` or `python run.py clean-venv` (Windows) / `python3 run.py clean-venv` (macOS/Linux) - Remove virtual environment

## Testing Framework

The project includes a comprehensive testing framework with:

### Test Structure
- **Unit Tests**: Individual component testing using pytest
- **Integration Tests**: End-to-end compilation testing
- **HTML Reports**: Detailed test results with coverage information
- **Automated CI**: Ready for continuous integration setup

### Test Files
- `tests/test_lexer.py` - Lexical analysis tests
- `tests/test_parser.py` - Syntax analysis tests  
- `tests/utils.py` - Testing utilities and helper classes

### Running Tests
```bash
# Activate virtual environment first (REQUIRED)
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run lexer tests
make test-lexer
# OR
# Windows:
python run.py test-lexer
# macOS/Linux:
python3 run.py test-lexer

# Run parser tests  
make test-parser
# OR  
# Windows:
python run.py test-parser
# macOS/Linux:
python3 run.py test-parser

# View reports
# Windows:
start reports/lexer/index.html
start reports/parser/index.html

# macOS:
open reports/lexer/index.html
open reports/parser/index.html

# Linux:
xdg-open reports/lexer/index.html
xdg-open reports/parser/index.html
```

### Test Report Features
- ✅ **Pass/Fail Status** for each test case
- ✅ **Execution Time** measurements
- ✅ **Error Messages** with stack traces
- ✅ **Code Coverage** analysis
- ✅ **HTML Export** for easy sharing

## Development Guide

### Architecture Overview

The HLang compiler follows a traditional compiler architecture:

```
Source Code (.hlang) 
    ↓
Lexical Analysis (HLangLexer)
    ↓  
Token Stream
    ↓
Syntax Analysis (HLangParser)
    ↓
Parse Tree
    ↓
[Future: AST Generation]
    ↓
[Future: Semantic Analysis]
    ↓
[Future: Code Generation]
```

### Extending the Grammar

To add new language features:

1. **Modify the grammar** in `src/grammar/HLang.g4`:
   ```antlr
   // Add new rule
   assignment: ID '=' exp ';' ;
   
   // Add new token
   ASSIGN: '=' ;
   ```

2. **Rebuild the parser**:
   ```bash
   # Activate virtual environment first
   source venv/bin/activate  # macOS/Linux
   # venv\Scripts\activate   # Windows
   
   make build
   # OR
   # Windows:
   python run.py build
   # macOS/Linux:
   python3 run.py build
   ```

3. **Add test cases** in `tests/`:
   ```python
   def test_assignment():
       source = "x = 42;"
       expected = "success"
       assert Parser(source).parse() == expected
   ```

4. **Run tests** to verify:
   ```bash
   # Activate virtual environment first
   source venv/bin/activate  # macOS/Linux
   # venv\Scripts\activate   # Windows
   
   make test-parser
   # OR
   # Windows:
   python run.py test-parser
   # macOS/Linux:
   python3 run.py test-parser
   ```

### Adding New Test Cases

#### Lexer Tests (`tests/test_lexer.py`)
```python
def test_new_feature():
    source = "your_test_input"
    expected = "expected,tokens,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected
```

#### Parser Tests (`tests/test_parser.py`)  
```python
def test_new_syntax():
    source = """your test program"""
    expected = "success"  # or specific error message
    assert Parser(source).parse() == expected
```

### File Naming Convention
- Test functions must start with `test_`
- Use descriptive names: `test_variable_declaration()`, `test_function_call()`
- Number tests sequentially: `test_001()`, `test_002()`, etc.

## Dependencies

### Core Dependencies
- **antlr4-python3-runtime==4.13.2** - ANTLR4 Python runtime for generated parsers
- **pytest** - Testing framework for unit and integration tests
- **pytest-html** - HTML report generation for test results
- **pytest-timeout** - Test timeout handling for long-running tests

### External Tools
- **ANTLR 4.13.2** - Parser generator tool (auto-downloaded)
- **Java Runtime Environment** - Required to run ANTLR4 tool

### Virtual Environment
The project automatically creates and manages a Python virtual environment to isolate dependencies.

## Troubleshooting

### Common Issues

#### "Java not found" error
```bash
# Install Java (macOS with Homebrew)
brew install openjdk

# Install Java (Ubuntu/Debian)
sudo apt update && sudo apt install openjdk-11-jre

# Install Java (Windows)
# Download from: https://www.oracle.com/java/technologies/downloads/
```

#### "Python 3.12 not found" error  
```bash
# macOS with Homebrew
brew install python@3.12

# Ubuntu/Debian  
sudo apt install python3.12

# Windows
# Download from: https://www.python.org/downloads/
```

#### ANTLR download failures
```bash
# Manual download if auto-download fails
mkdir -p external
cd external
curl -O https://www.antlr.org/download/antlr-4.13.2-complete.jar
cd ..
make build
```

#### Virtual environment issues
```bash
# Clean and recreate virtual environment
make clean-venv
make setup

# Remember to activate before building/testing
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

#### Permission errors (Linux/macOS)
```bash
# Ensure you have write permissions
chmod +x Makefile
```

### Getting Help

1. **Check Prerequisites**: Run `make check` to verify system setup
2. **View Logs**: Check terminal output for detailed error messages  
3. **Clean Build**: Try `make clean && make setup && make build`
4. **Check Java**: Ensure Java is properly installed and in PATH
5. **Virtual Environment**: Always activate the virtual environment before running build/test commands:
   ```bash
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate   # Windows
   ```


## License

This project is developed for educational purposes as part of the **Principle of Programming Languages course (CO3005)** at the **Department of Computer Science, Faculty of Computer Science and Engineering - Ho Chi Minh City University of Technology (VNU-HCM)**.

## Acknowledgments

- **ANTLR Project**: For providing an excellent parser generator tool
- **Course Instructors**: For guidance and project requirements
- **Python Community**: For the robust ecosystem of testing and development tools

---

**Course**: CO3005 - Principle of Programming Languages  
**Institution**: Ho Chi Minh City University of Technology (VNU-HCM)  
**Department**: Computer Science, Faculty of Computer Science and Engineering

