#!/usr/bin/env python3
"""
easy-ics 后端启动检查和运行脚本
easy-ics backend startup script

用法:
    python backend_startup.py              # 显示启动信息
    python backend_startup.py --run        # 启动服务
    python backend_startup.py --test       # 运行快速测试
    python backend_startup.py --check      # 仅检查环境
"""

import sys
import subprocess
import shutil
from pathlib import Path
from typing import Tuple

# 颜色定义
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    """打印标题"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.BLUE}{'─'*60}{Colors.END}")

def print_success(text: str):
    """打印成功信息"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text: str):
    """打印错误信息"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text: str):
    """打印警告信息"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text: str):
    """打印信息"""
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.END}")

def check_python_version() -> bool:
    """检查 Python 版本"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} (需要 3.11+)")
        return False

def check_command(name: str, command: str) -> bool:
    """检查命令是否可用"""
    if shutil.which(command):
        result = subprocess.run([command, "--version"], capture_output=True, text=True)
        version_line = result.stdout.split('\n')[0] if result.stdout else "已安装"
        print_success(f"{name}: {version_line.strip()}")
        return True
    else:
        print_error(f"{name}: 未安装")
        return False

def check_python_package(name: str, import_name: str) -> bool:
    """检查 Python 包"""
    try:
        __import__(import_name)
        print_success(f"{name}")
        return True
    except ImportError:
        print_error(f"{name}: 未安装")
        return False

def check_file(name: str, path: str) -> bool:
    """检查文件是否存在"""
    if Path(path).exists():
        print_success(f"{name}: {path}")
        return True
    else:
        print_error(f"{name}: {path} (未找到)")
        return False

def run_checks() -> dict:
    """运行所有检查"""
    results = {
        "python": False,
        "tesseract": False,
        "packages": 0,
        "files": 0
    }
    
    print(f"""
    ╔════════════════════════════════════════════════════════════╗
    ║          easy-ics 后端启动环境检查                          ║
    ║          Backend Startup Environment Check                ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # 1. Python 版本
    print_header("1. Python 版本检查")
    results["python"] = check_python_version()
    
    # 2. 系统命令
    print_header("2. 系统命令检查")
    results["tesseract"] = check_command("Tesseract OCR", "tesseract")
    
    # 3. Python 包
    print_header("3. Python 依赖检查")
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
    
    print_info(f"已安装 {results['packages']}/{len(packages)} 个依赖")
    
    # 4. 项目文件
    print_header("4. 项目结构检查")
    backend_dir = Path(__file__).parent / "backend"
    
    files = [
        ("主应用", backend_dir / "app" / "main.py"),
        ("API 路由", backend_dir / "app" / "api.py"),
        ("OCR 服务", backend_dir / "app" / "services" / "ocr_service.py"),
        ("项目配置", backend_dir / "pyproject.toml"),
    ]
    
    for name, path in files:
        if check_file(name, str(path)):
            results["files"] += 1
    
    print_info(f"已找到 {results['files']}/{len(files)} 个文件")
    
    return results

def show_startup_guide():
    """显示启动指南"""
    print_header("5. 快速启动指南")
    
    print(f"""
{Colors.YELLOW}方式 1: 开发模式 (推荐){Colors.END}
  cd backend
  uvicorn app.main:app --reload

{Colors.YELLOW}方式 2: 生产模式{Colors.END}
  cd backend
  uvicorn app.main:app --host 0.0.0.0 --port 8000

{Colors.YELLOW}方式 3: 使用 Python 模块{Colors.END}
  cd backend
  python -m uvicorn app.main:app --reload
    """)

def show_api_endpoints():
    """显示 API 端点"""
    print_header("6. API 端点一览")
    
    endpoints = [
        ("时区管理", [
            ("GET", "/api/timezones/common", "获取常用时区列表"),
            ("GET", "/api/timezones/all", "获取所有 IANA 时区"),
            ("POST", "/api/timezones/validate", "验证时区代码"),
        ]),
        ("OCR 服务", [
            ("GET", "/api/ocr/health", "健康检查"),
            ("POST", "/api/ocr/upload", "上传图片识别"),
        ]),
        ("文本处理", [
            ("POST", "/api/text/parse", "解析文本提取事件"),
        ]),
        ("日历生成", [
            ("POST", "/api/ics/generate", "生成 ICS 文件"),
        ]),
        ("完整流程", [
            ("POST", "/api/process", "图片→ICS 完整处理"),
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
    """显示测试指南"""
    print_header("7. 测试方式")
    
    print(f"""
{Colors.YELLOW}API 文档和交互式测试{Colors.END}
  启动服务后访问:
  • Swagger UI: http://localhost:8000/docs
  • ReDoc: http://localhost:8000/redoc

{Colors.YELLOW}单个端点测试 (使用 curl){Colors.END}
  # 测试健康检查
  curl http://localhost:8000/api/ocr/health | jq

  # 验证时区
  curl -X POST http://localhost:8000/api/timezones/validate \\
    -F "timezone=Asia/Shanghai" | jq
    """)

def show_troubleshooting():
    """显示故障排除"""
    print_header("8. 故障排除")
    
    print(f"""
{Colors.YELLOW}问题: 端口 8000 已被占用{Colors.END}
  解决: uvicorn app.main:app --port 8001

{Colors.YELLOW}问题: 模块导入错误{Colors.END}
  解决: 确保在 backend 目录中运行，或:
        export PYTHONPATH=$PWD:$PYTHONPATH

{Colors.YELLOW}问题: Tesseract 不可用{Colors.END}
  解决: macOS: brew install tesseract
        Linux: sudo apt-get install tesseract-ocr
        Windows: 从 https://github.com/UB-Mannheim/tesseract/wiki 下载

{Colors.YELLOW}问题: 依赖安装失败{Colors.END}
  解决: cd backend && pip install -e .[dev]

{Colors.YELLOW}问题: 测试连接被拒绝{Colors.END}
  解决: 确保 FastAPI 服务正在运行:
        cd backend && uvicorn app.main:app --reload
    """)

def start_server():
    """启动 FastAPI 服务"""
    print_header("启动 FastAPI 服务 (开发模式)")
    
    print("\n" + Colors.CYAN + "启动命令: uvicorn app.main:app --reload" + Colors.END)
    print(Colors.CYAN + "访问地址: http://localhost:8000/docs" + Colors.END)
    print(Colors.CYAN + "按 Ctrl+C 停止服务\n" + Colors.END)
    
    try:
        import os
        backend_dir = Path(__file__).parent / "backend"
        os.chdir(backend_dir)
        subprocess.run(
            ["uvicorn", "app.main:app", "--reload"],
            check=False
        )
    except KeyboardInterrupt:
        print("\n" + Colors.YELLOW + "服务已停止" + Colors.END)
    except Exception as e:
        print_error(f"启动失败: {e}")
        sys.exit(1)

def main():
    """主函数"""
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--check":
            run_checks()
        elif arg == "--run":
            results = run_checks()
            if results["python"]:
                start_server()
            else:
                print_error("环境检查失败，无法启动服务")
                sys.exit(1)
        elif arg == "--help":
            print(f"""
{Colors.BOLD}使用方法:{Colors.END}
  python backend_startup.py              # 显示启动信息和检查
  python backend_startup.py --run        # 启动 FastAPI 服务
  python backend_startup.py --check      # 仅运行环境检查
  python backend_startup.py --help       # 显示此帮助信息
            """)
        else:
            print_error(f"未知选项: {arg}")
            print("使用 --help 查看帮助信息")
            sys.exit(1)
    else:
        # 默认: 显示完整的启动信息
        results = run_checks()
        show_startup_guide()
        show_api_endpoints()
        show_testing_guide()
        show_troubleshooting()
        
        # 最后的提示
        print_header("准备完毕！开始开发 🚀")
        
        print(f"""
{Colors.GREEN}下一步操作:{Colors.END}

1. 启动后端服务:
   cd backend
   uvicorn app.main:app --reload

2. 访问 API 文档:
   http://localhost:8000/docs

{Colors.CYAN}相关文档:{Colors.END}
  • API 路由文档: docs/API_TIMEZONE_ROUTES.md
        """)

if __name__ == "__main__":
    main()
