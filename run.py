#!/usr/bin/env python3
"""
HLang Project Build Script

This Python script provides cross-platform build automation for the HLang project.
It replaces the Makefile functionality with native Python commands that work
on Windows, macOS, and Linux.

Usage:
    # On Windows:
    python run.py help
    python run.py setup
    python run.py build
    python run.py test-lexer
    python run.py test-parser
    python run.py clean

    # On macOS/Linux:
    python3 run.py help
    python3 run.py setup
    python3 run.py build
    python3 run.py test-lexer
    python3 run.py test-parser
    python3 run.py clean
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""

    def __init__(self):
        # Check if we're on Windows and if ANSI is supported
        self.supported = (
            platform.system() != "Windows"
            or os.environ.get("TERM")
            or os.environ.get("ANSICON")
            or "ANSI" in os.environ.get("TERM_PROGRAM", "")
        )

        if self.supported:
            self.RED = "\033[31m"
            self.GREEN = "\033[32m"
            self.YELLOW = "\033[33m"
            self.BLUE = "\033[34m"
            self.RESET = "\033[0m"
        else:
            self.RED = self.GREEN = self.YELLOW = self.BLUE = self.RESET = ""

    def red(self, text):
        return f"{self.RED}{text}{self.RESET}"

    def green(self, text):
        return f"{self.GREEN}{text}{self.RESET}"

    def yellow(self, text):
        return f"{self.YELLOW}{text}{self.RESET}"

    def blue(self, text):
        return f"{self.BLUE}{text}{self.RESET}"


class HLangBuilder:
    """Main builder class for HLang project."""

    def __init__(self):
        self.root_dir = Path(__file__).parent.absolute()
        self.external_dir = self.root_dir / "external"
        self.build_dir = self.root_dir / "build"
        self.report_dir = self.root_dir / "reports"
        self.venv_dir = self.root_dir / "venv"

        self.antlr_version = "4.13.2"
        self.antlr_jar = f"antlr-{self.antlr_version}-complete.jar"
        self.antlr_url = f"https://www.antlr.org/download/{self.antlr_jar}"

        self.python_version = "3.12"

        self.colors = Colors()

        # Platform-specific paths
        if platform.system() == "Windows":
            self.venv_python3 = self.venv_dir / "Scripts" / "python.exe"
            self.venv_pip = self.venv_dir / "Scripts" / "pip.exe"
        else:
            self.venv_python3 = self.venv_dir / "bin" / "python"
            self.venv_pip = self.venv_dir / "bin" / "pip"

    def run_command(self, cmd, cwd=None, check=True, capture_output=False):
        """Run a shell command."""
        try:
            if isinstance(cmd, str):
                # Shell mode for complex commands
                result = subprocess.run(
                    cmd,
                    shell=True,
                    cwd=cwd or self.root_dir,
                    check=check,
                    capture_output=capture_output,
                    text=True,
                )
            else:
                # List mode for simple commands
                result = subprocess.run(
                    cmd,
                    cwd=cwd or self.root_dir,
                    check=check,
                    capture_output=capture_output,
                    text=True,
                )
            return result
        except subprocess.CalledProcessError as e:
            if not capture_output:
                print(self.colors.red(f"Command failed: {e}"))
            if check:
                sys.exit(1)
            return e

    def command_exists(self, command):
        """Check if a command exists in PATH."""
        try:
            self.run_command([command, "--version"], capture_output=True, check=False)
            return True
        except:
            return False

    def find_python(self):
        """Find appropriate Python executable."""
        candidates = [f"python{self.python_version}", "python", "py"]

        for cmd in candidates:
            try:
                result = self.run_command(
                    [cmd, "--version"], capture_output=True, check=False
                )
                if result.returncode == 0 and self.python_version in result.stdout:
                    return cmd
            except:
                continue

        # Try py launcher with version
        if platform.system() == "Windows":
            try:
                result = self.run_command(
                    [f"py", f"-{self.python_version}", "--version"],
                    capture_output=True,
                    check=False,
                )
                if result.returncode == 0:
                    return f"py -{self.python_version}"
            except:
                pass

        return None

    def show_help(self):
        """Show help information."""
        print(self.colors.blue("HLang Project - Available Commands:"))
        print()
        print(self.colors.green("Setup & Build:"))
        print(
            self.colors.yellow(
                "  python3 run.py setup     - Install dependencies and set up environment"
            )
        )
        print(
            self.colors.yellow(
                "  python3 run.py build     - Compile ANTLR grammar files"
            )
        )
        print(
            self.colors.yellow(
                "  python3 run.py check     - Check if required tools are installed"
            )
        )
        print()
        print(self.colors.green("Testing:"))
        print(
            self.colors.yellow(
                "  python3 run.py test-lexer  - Run lexer tests and generate reports"
            )
        )
        print(
            self.colors.yellow(
                "  python3 run.py test-parser - Run parser tests and generate reports"
            )
        )
        print(
            self.colors.yellow(
                "  python3 run.py test-checker - Run semantic checker tests and generate reports"
            )
        )
        print()
        print(self.colors.green("Cleaning:"))
        print(
            self.colors.yellow(
                "  python3 run.py clean         - Clean build and external directories"
            )
        )
        print(
            self.colors.yellow(
                "  python3 run.py clean-cache   - Clean Python cache files"
            )
        )
        print(
            self.colors.yellow(
                "  python3 run.py clean-reports - Clean test reports directory"
            )
        )
        print(
            self.colors.yellow(
                "  python3 run.py clean-venv    - Remove virtual environment"
            )
        )
        print()
        print(self.colors.green("Environment:"))
        print(f"  Virtual environment: {self.venv_dir}")
        print(f"  Python version required: {self.python_version}")
        print(f"  ANTLR version: {self.antlr_version}")
        print()
        print(
            self.colors.blue(
                "Quick start: python3 run.py setup && python3 run.py build"
            )
        )

    def check_dependencies(self):
        """Check if required dependencies are installed."""
        print(self.colors.blue("Checking required dependencies..."))
        print()

        # Check Java
        print(self.colors.yellow("Checking Java installation..."))
        if self.command_exists("java"):
            print(self.colors.green("✓ Java is installed"))
            java_ok = True
        else:
            print(self.colors.red("✗ Java is not installed"))
            print(self.colors.yellow("  Please install Java manually:"))
            if platform.system() == "Windows":
                print(
                    self.colors.yellow(
                        "    - Download from https://adoptium.net/ or https://www.oracle.com/java/technologies/downloads/"
                    )
                )
                print(
                    self.colors.yellow("    - Or use Chocolatey: choco install openjdk")
                )
                print(self.colors.yellow("    - Or use Scoop: scoop install openjdk"))
            elif platform.system() == "Darwin":
                print(self.colors.yellow("    - On macOS: brew install openjdk"))
            else:
                print(
                    self.colors.yellow(
                        "    - On Ubuntu/Debian: sudo apt install openjdk-17-jdk"
                    )
                )
                print(
                    self.colors.yellow("    - Or download from https://adoptium.net/")
                )
            print(self.colors.yellow("  Make sure Java is in your PATH"))
            java_ok = False

        print()

        # Check Python
        print(
            self.colors.yellow(f"Checking Python {self.python_version} installation...")
        )
        python_cmd = self.find_python()
        if python_cmd:
            print(
                self.colors.green(f"✓ Python {self.python_version} found: {python_cmd}")
            )
            python_ok = True
        else:
            print(
                self.colors.red(
                    f"✗ Python {self.python_version} is not installed or not found"
                )
            )
            print(
                self.colors.yellow(
                    f"  Please install Python {self.python_version} manually:"
                )
            )
            print(
                self.colors.yellow(
                    "    - Download from https://www.python.org/downloads/"
                )
            )
            if platform.system() == "Windows":
                print(
                    self.colors.yellow(
                        f"    - Or use Chocolatey: choco install python3 --version={self.python_version}"
                    )
                )
                print(self.colors.yellow("    - Or use Scoop: scoop install python"))
            elif platform.system() == "Darwin":
                print(
                    self.colors.yellow(
                        f"    - On macOS: brew install python@{self.python_version}"
                    )
                )
            else:
                print(
                    self.colors.yellow(
                        f"    - On Ubuntu/Debian: sudo apt install python{self.python_version} python{self.python_version}-venv python3-pip"
                    )
                )
            print(self.colors.yellow("  Make sure Python is in your PATH"))
            python_ok = False

        print()
        print(self.colors.blue("Dependency check completed."))

        return java_ok and python_ok

    def setup_environment(self):
        """Set up the project environment."""
        print(self.colors.blue("Setting up project environment..."))

        # Create external directory
        self.external_dir.mkdir(exist_ok=True)

        # Check dependencies
        if not self.check_dependencies():
            print(self.colors.red("Setup failed due to missing dependencies."))
            sys.exit(1)

        python_cmd = self.find_python()

        # Create virtual environment
        print(self.colors.yellow("Creating virtual environment..."))
        if not self.venv_dir.exists():
            self.run_command([python_cmd, "-m", "venv", str(self.venv_dir)])
            print(self.colors.green(f"Virtual environment created at {self.venv_dir}"))
        else:
            print(
                self.colors.blue(
                    f"Virtual environment already exists at {self.venv_dir}"
                )
            )

        # Download ANTLR
        print(self.colors.yellow(f"Downloading ANTLR version {self.antlr_version}..."))
        print(self.colors.blue("This may take a moment..."))

        antlr_path = self.external_dir / self.antlr_jar
        if not antlr_path.exists():
            try:
                urllib.request.urlretrieve(self.antlr_url, antlr_path)
                print(self.colors.green(f"ANTLR downloaded to {antlr_path}"))
            except Exception as e:
                print(self.colors.red(f"Failed to download ANTLR: {e}"))
                sys.exit(1)
        else:
            print(self.colors.blue(f"ANTLR already exists at {antlr_path}"))

        # Upgrade pip
        print(self.colors.yellow("Upgrading pip in virtual environment..."))
        self.run_command([str(self.venv_pip), "install", "--upgrade", "pip"])
        print(self.colors.green("pip upgraded successfully."))

        # Install dependencies
        print(
            self.colors.yellow(
                "Installing Python dependencies in virtual environment..."
            )
        )
        self.run_command([str(self.venv_pip), "install", "-r", "requirements.txt"])
        print(
            self.colors.green("Python dependencies installed in virtual environment.")
        )

        print(
            self.colors.green(
                f"Setup completed! Virtual environment is ready at {self.venv_dir}"
            )
        )
        print(self.colors.blue("To activate the virtual environment manually:"))
        if platform.system() == "Windows":
            print(self.colors.blue(f"  {self.venv_dir}\\Scripts\\Activate.ps1"))
            print(self.colors.blue(f"  or: {self.venv_dir}\\Scripts\\activate.bat"))
        else:
            print(self.colors.blue(f"  source {self.venv_dir}/bin/activate"))

    def build_grammar(self):
        """Build ANTLR grammar files."""
        antlr_path = self.external_dir / self.antlr_jar
        if not antlr_path.exists():
            print(self.colors.red("ANTLR jar not found. Please run 'setup' first."))
            sys.exit(1)

        # Create build directories
        self.build_dir.mkdir(exist_ok=True)

        # Find grammar files
        grammar_files = list((self.root_dir / "src" / "grammar").glob("*.g4"))
        if not grammar_files:
            print(self.colors.red("No grammar files found in src/grammar/"))
            sys.exit(1)

        # Compile ANTLR grammar
        print(self.colors.yellow("Compiling ANTLR grammar files..."))
        cmd = [
            "java",
            "-jar",
            str(antlr_path),
            "-Dlanguage=Python3",
            "-visitor",
            "-no-listener",
            "-o",
            str(self.build_dir),
        ] + [str(f) for f in grammar_files]

        self.run_command(cmd)

        # Create __init__.py files
        print(self.colors.yellow("Creating __init__.py files..."))
        (self.build_dir / "__init__.py").touch()

        # Copy Python files
        print(
            self.colors.yellow(
                "Copying Python files from src/grammar/ to build/src/grammar/"
            )
        )
        lexererr_src = self.root_dir / "src" / "grammar" / "lexererr.py"
        lexererr_dst = self.build_dir / "lexererr.py"
        if lexererr_src.exists():
            shutil.copy2(lexererr_src, lexererr_dst)

        print(self.colors.green("ANTLR grammar files compiled to build/"))

    def clean_cache(self):
        """Clean Python cache files."""
        print(self.colors.yellow("Cleaning Python cache files..."))

        for pattern in ["**/__pycache__", "**/*.pyc", "**/.pytest_cache"]:
            for path in self.root_dir.glob(pattern):
                if path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    path.unlink(missing_ok=True)

        print(self.colors.green("Python cache files cleaned."))

    def clean_reports(self):
        """Clean reports directory."""
        print(self.colors.yellow("Cleaning reports directory..."))
        if self.report_dir.exists():
            shutil.rmtree(self.report_dir)
        print(self.colors.green("Reports directory cleaned."))

    def clean_venv(self):
        """Clean virtual environment."""
        print(self.colors.yellow("Cleaning virtual environment..."))
        if self.venv_dir.exists():
            shutil.rmtree(self.venv_dir)
        print(self.colors.green("Virtual environment cleaned."))

    def clean_all(self):
        """Clean build and external directories."""
        print(self.colors.yellow("Cleaning build directories..."))

        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)

        print(self.colors.green("Cleaned build directories."))
        self.clean_cache()

    def test_lexer(self):
        """Run lexer tests."""
        if not self.build_dir.exists():
            print(
                self.colors.yellow("Build directory not found. Running build first...")
            )
            self.build_grammar()

        print(self.colors.yellow("Running lexer tests..."))

        # Clean and create reports directory
        lexer_report_dir = self.report_dir / "lexer"
        if lexer_report_dir.exists():
            shutil.rmtree(lexer_report_dir)
        self.report_dir.mkdir(exist_ok=True)

        # Run tests
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.root_dir)

        self.run_command(
            [
                str(self.venv_python3),
                "-m",
                "pytest",
                "tests/test_lexer.py",
                f"--html={lexer_report_dir}/index.html",
                "--timeout=3",
                "--self-contained-html",
            ],
            check=False,
        )  # Don't fail on test failures

        print(
            self.colors.green(
                f"Lexer tests completed. Reports generated at {lexer_report_dir}/index.html"
            )
        )
        self.clean_cache()

    def test_parser(self):
        """Run parser tests."""
        if not self.build_dir.exists():
            print(
                self.colors.yellow("Build directory not found. Running build first...")
            )
            self.build_grammar()

        print(self.colors.yellow("Running parser tests..."))

        # Clean and create reports directory
        parser_report_dir = self.report_dir / "parser"
        if parser_report_dir.exists():
            shutil.rmtree(parser_report_dir)
        self.report_dir.mkdir(exist_ok=True)

        # Run tests
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.root_dir)

        self.run_command(
            [
                str(self.venv_python3),
                "-m",
                "pytest",
                "tests/test_parser.py",
                f"--html={parser_report_dir}/index.html",
                "--timeout=3",
                "--self-contained-html",
            ],
            check=False,
        )  # Don't fail on test failures

        print(
            self.colors.green(
                f"Parser tests completed. Reports generated at {parser_report_dir}/index.html"
            )
        )
        self.clean_cache()

    def test_ast(self):
        """Run AST generation tests."""
        if not self.build_dir.exists():
            print(
                self.colors.yellow("Build directory not found. Running build first...")
            )
            self.build_grammar()

        print(self.colors.yellow("Running AST generation tests..."))

        # Clean and create reports directory
        ast_report_dir = self.report_dir / "ast"
        if ast_report_dir.exists():
            shutil.rmtree(ast_report_dir)
        self.report_dir.mkdir(exist_ok=True)

        # Run tests
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.root_dir)

        self.run_command(
            [
                str(self.venv_python3),
                "-m",
                "pytest",
                "tests/test_ast_gen.py",
                f"--html={ast_report_dir}/index.html",
                "--timeout=5",
                "--self-contained-html",
                "-v",
            ],
            check=False,
        )  # Don't fail on test failures

        print(
            self.colors.green(
                f"AST generation tests completed. Reports generated at {ast_report_dir}/index.html"
            )
        )
        self.clean_cache()

    def test_checker(self):
        """Run semantic checker tests."""
        if not self.build_dir.exists():
            print(
                self.colors.yellow("Build directory not found. Running build first...")
            )
            self.build_grammar()

        print(self.colors.yellow("Running semantic checker tests..."))

        # Clean and create reports directory
        checker_report_dir = self.report_dir / "checker"
        if checker_report_dir.exists():
            shutil.rmtree(checker_report_dir)
        self.report_dir.mkdir(exist_ok=True)

        # Run tests
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.root_dir)

        self.run_command(
            [
                str(self.venv_python3),
                "-m",
                "pytest",
                "tests/test_checker.py",
                f"--html={checker_report_dir}/index.html",
                "--timeout=5",
                "--self-contained-html",
                "-v",
            ],
            check=False,
        )  # Don't fail on test failures

        print(
            self.colors.green(
                f"Semantic checker tests completed. Reports generated at {checker_report_dir}/index.html"
            )
        )
        self.clean_cache()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="HLang Project Build Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available commands:
  help          Show this help message
  check         Check if required tools are installed
  setup         Install dependencies and set up environment
  build         Compile ANTLR grammar files
  clean         Clean build and external directories
  clean-cache   Clean Python cache files
  clean-reports Clean test reports directory
  clean-venv    Remove virtual environment
  test-lexer    Run lexer tests and generate reports
  test-parser   Run parser tests and generate reports
  test-ast      Run AST generation tests
  test-checker  Run semantic checker tests

Examples:
  python3 run.py setup
  python3 run.py build
  python3 run.py test-lexer
  python3 run.py test-ast
        """,
    )

    parser.add_argument(
        "command",
        nargs="?",
        default="help",
        choices=[
            "help",
            "check",
            "setup",
            "build",
            "clean",
            "clean-cache",
            "clean-reports",
            "clean-venv",
            "test-lexer",
            "test-parser",
            "test-ast",
            "test-checker",
        ],
        help="Command to execute",
    )

    args = parser.parse_args()

    builder = HLangBuilder()

    commands = {
        "help": builder.show_help,
        "check": builder.check_dependencies,
        "setup": builder.setup_environment,
        "build": builder.build_grammar,
        "clean": builder.clean_all,
        "clean-cache": builder.clean_cache,
        "clean-reports": builder.clean_reports,
        "clean-venv": builder.clean_venv,
        "test-lexer": builder.test_lexer,
        "test-parser": builder.test_parser,
        "test-ast": builder.test_ast,
        "test-checker": builder.test_checker,
    }

    if args.command in commands:
        commands[args.command]()
    else:
        print(f"Unknown command: {args.command}")
        builder.show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
