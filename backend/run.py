#!/usr/bin/env python3
"""
easy-ics backend startup script

Usage:
    python run.py.py                    # Show startup info
    python run.py.py --run              # Start service
    python run.py.py --test --*name     # Run test
    python run.py.py --check            # Env check only
"""

import sys
import subprocess
import shutil
from pathlib import Path
from typing import Tuple

class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.BLUE}{'─'*60}{Colors.END}")

def print_success(text: str):
    print(f"{Colors.GREEN}\u2713 {text}{Colors.END}")

def print_error(text: str):
    print(f"{Colors.RED}\u2718 {text}{Colors.END}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}!  {text}{Colors.END}")

def print_info(text: str):
    print(f"{Colors.CYAN}INFO:  {text}{Colors.END}")

def check_python_version() -> bool:
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} (python version 3.11+ required)")
        return False

def check_command(name: str, command: str) -> bool:
    if shutil.which(command):
        result = subprocess.run([command, "--version"], capture_output=True, text=True)
        version_line = result.stdout.split('\n')[0] if result.stdout else "Installed"
        print_success(f"{name}: {version_line.strip()}")
        return True
    else:
        print_error(f"{name}: not installed")
        return False

def check_python_package(name: str, import_name: str) -> bool:
    try:
        __import__(import_name)
        print_success(f"{name}")
        return True
    except ImportError:
        print_error(f"{name}: not installed")
        return False

def check_file(name: str, path: str) -> bool:
    if Path(path).exists():
        print_success(f"{name}: {path}")
        return True
    else:
        print_error(f"{name}: {path} (not found)")
        return False

def run_checks() -> dict:
    results = {
        "python": False,
        "tesseract": False,
        "packages": 0,
        "files": 0
    }
    
    print(f"""
    ╔════════════════════════════════════════════════════════════╗
    ║          easy-ics backend startup.                         ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    print_header("1. Python version check")
    results["python"] = check_python_version()
    
    print_header("2. System command check")
    results["tesseract"] = check_command("Tesseract OCR", "tesseract")
    
    print_header("3. Python dependencies check")
    packages = [
        ("FastAPI", "fastapi"),
        ("Pydantic", "pydantic"),
        ("Pytesseract", "pytesseract"),
        ("Pillow", "PIL"),
        ("Python-multipart", "multipart"),
        ("Uvicorn", "uvicorn"),
    ]
    
    for name, import_name in packages:
        if check_python_package(name, import_name):
            results["packages"] += 1
    
    print_info(f" {results['packages']}/{len(packages)} dependencies installed")
    
    print_header("4. project structure check")
    backend_dir = Path(__file__).parent
    
    files = [
        ("Main app", backend_dir / "app" / "main.py"),
        ("API router", backend_dir / "app" / "api.py"),
        ("OCR service", backend_dir / "app" / "services" / "ocr_service.py"),
        ("Project config", backend_dir / "pyproject.toml"),
    ]
    
    for name, path in files:
        if check_file(name, str(path)):
            results["files"] += 1
    
    print_info(f" {results['files']}/{len(files)} files found")
    return results

def run_tests(test_unit: str = None) -> dict:
    """运行指定的测试
    
    Args:
        test_unit: 测试单位，支持 'ocr', 'ics' 等，如果为 None 则运行所有测试
    """
    backend_dir = Path(__file__).parent
    tests_dir = backend_dir / "tests"
    test_units = {
        "ocr": "ocr_test.py",
        "ics": "ics_test.py",
    }
    results = {
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "total": 0
    }
    try:
        if test_unit:
            if test_unit not in test_units:
                print_error(f"Unknown test unit: {test_unit}")
                print_info(f"Supported test units: {', '.join(test_units.keys())}")
                return results
            
            test_file = tests_dir / test_units[test_unit]
            print_header(f"Runing {test_unit.upper()} test")
            
            if not test_file.exists():
                print_error(f"Test file doesn't exist: {test_file}")
                return results
            
            print_info(f"Test file: {test_file.name}")
            print_info(f"Start running...\n")
            
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    str(test_file),
                    "-v",
                    "--tb=short",
                    "-ra"
                ],
                cwd=str(backend_dir),
                capture_output=False
            )
            
            if result.returncode == 0:
                print_success("All tests pass!!!")
                results["passed"] = 1
            else:
                print_warning("Some tests failed")
                results["failed"] = 1
            
            results["total"] = 1
        else:
            print_header("Running all tests")
            print_info("Start running all tests...\n")
            
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    str(tests_dir),
                    "-v",
                    "--tb=short",
                    "-ra"
                ],
                cwd=str(backend_dir),
                capture_output=False
            )
            
            if result.returncode == 0:
                print_success("All tests pass!!!")
                results["passed"] = 1
            else:
                print_warning("Some tests failed")
                results["failed"] = 1
            
            results["total"] = 1
        
        return results
        
    except Exception as e:
        print_error(f"Fail running tests: {e}")
        results["failed"] = 1
        results["total"] = 1
        return results

def show_startup_guide():
    print_header("5. Quick start guide")
    
    print(f"""
{Colors.YELLOW}Method 1: dev mode{Colors.END}
  cd backend
  uvicorn app.main:app --reload

{Colors.YELLOW}Method 2: prod mode{Colors.END}
  cd backend
  uvicorn app.main:app --host 0.0.0.0 --port 8000

{Colors.YELLOW}Method 3: use Python module{Colors.END}
  cd backend
  python -m uvicorn app.main:app --reload
    """)

def show_api_endpoints():
    print_header("6. API endpoints")
    
    endpoints = [
        ("timezone managements", [
            ("GET", "/api/timezones/common", "get common timezone list"),
            ("GET", "/api/timezones/all", "get all IANA timezones"),
            ("POST", "/api/timezones/validate", "validate timezone code"),
        ]),
        ("OCR service", [
            ("GET", "/api/ocr/health", "Health check"),
            ("POST", "/api/ocr/upload", "upload image"),
        ]),
        ("Text parsing", [
            ("POST", "/api/text/parse", "text parsing"),
        ]),
        ("file generate", [
            ("POST", "/api/ics/generate", "generate ICS file"),
        ]),
        ("process", [
            ("POST", "/api/process", "whole process"),
        ]),
    ]
    
    for category, routes in endpoints:
        print(f"\n{Colors.CYAN}{category}{Colors.END}")
        for method, path, desc in routes:
            method_color = {
                "GET": Colors.GREEN,
                "POST": Colors.YELLOW,
            }.get(method, Colors.BLUE)
            print(f"  {method_color}{method:6}{Colors.END} {path:30} {desc}")

def show_testing_guide():
    print_header("7. text methods")
    
    print(f"""
{Colors.YELLOW}API doc and interactive tests{Colors.END}
  start service and click:
  • Swagger UI: http://localhost:8000/docs
  • ReDoc: http://localhost:8000/redoc

{Colors.YELLOW}Single endpoint check (use curl){Colors.END}
  # health check
  curl http://localhost:8000/api/ocr/health | jq

  # verify timezone
  curl -X POST http://localhost:8000/api/timezones/validate \\
    -F "timezone=Asia/Shanghai" | jq
    """)

def show_troubleshooting():
    print_header("8. troubleshooting")
    
    print(f"""
{Colors.YELLOW}WARNING: port 8000 occupied{Colors.END}
  Solution: uvicorn app.main:app --port 8001

{Colors.YELLOW}WARNING: Module import error{Colors.END}
  Solution: Make sure running in /backend, or:
        export PYTHONPATH=$PWD:$PYTHONPATH

{Colors.YELLOW}WARNING: Cannot use Tesseract{Colors.END}
  Solution: macOS: brew install tesseract
        Linux: sudo apt-get install tesseract-ocr
        Windows: download form https://github.com/UB-Mannheim/tesseract/wiki 

{Colors.YELLOW}WARNING: dependencies installation failed{Colors.END}
  Solution: cd backend && pip install -e .[dev]

{Colors.YELLOW}WARNING: test connect rejected{Colors.END}
  Solution: Make sure FastAPI service is running:
        cd backend && uvicorn app.main:app --reload
    """)

def start_server():
    print_header("Satrt FastAPI service(dev)")
    
    print("\n" + Colors.CYAN + "Start: uvicorn app.main:app --reload" + Colors.END)
    print(Colors.CYAN + "Access: http://localhost:8000/docs" + Colors.END)
    print(Colors.CYAN + "Ctrl+C to terminate service\n" + Colors.END)
    
    try:
        import os
        backend_dir = Path(__file__).parent / "backend"
        os.chdir(backend_dir)
        subprocess.run(
            ["uvicorn", "app.main:app", "--reload"],
            check=False
        )
    except KeyboardInterrupt:
        print("\n" + Colors.YELLOW + "Service terminated" + Colors.END)
    except Exception as e:
        print_error(f"Start failed: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--check":
            run_checks()
        elif arg == "--run":
            results = run_checks()
            if results["python"]:
                start_server()
            else:
                print_error("env check failed, unable to start service")
                sys.exit(1)
        elif arg == "--test":
            results = run_checks()
            if results["python"]:
                # 获取可选的测试单位参数
                test_unit = sys.argv[2] if len(sys.argv) > 2 else None
                run_tests(test_unit)
            else:
                print_error("env check failed, unable to run tests")
                sys.exit(1)
        elif arg == "--help":
            print(f"""
{Colors.BOLD}usage:{Colors.END}
    python run.py.py              # Show startup info
    python run.py.py --run        # Start service
    python run.py.py --test [unit]# Run tests (optional: ocr, ics)
    python run.py.py --check      # Env check only
    python run.py.py --help       # Show this message

{Colors.BOLD}examples:{Colors.END}
    python run.py --test          # Run all tests
    python run.py --test ocr      # Run OCR tests only
    python run.py --test ics      # Run ICS tests only
            """)
        else:
            print_error(f"Unknown args: {arg}")
            print("use --help to check for help info")
            sys.exit(1)
    else:
        results = run_checks()
        show_startup_guide()
        show_api_endpoints()
        show_testing_guide()
        show_troubleshooting()
        print_header("Starting...")
        
        print(f"""
{Colors.GREEN}Next step:{Colors.END}

1. Start backend service:
   cd backend
   uvicorn app.main:app --reload

2. Access API doc:
   http://localhost:8000/docs

3. Run tests:
   python run.py --test ocr      # Run OCR tests
   python run.py --test ics      # Run ICS tests
   python run.py --test          # Run all tests
        """)

if __name__ == "__main__":
    main()
