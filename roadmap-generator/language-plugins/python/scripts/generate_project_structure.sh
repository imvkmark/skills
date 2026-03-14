#!/bin/bash

# Python 学习项目结构生成脚本
# 用法：./generate_project_structure.sh <项目名称>

PROJECT_NAME=$1
if [ -z "$PROJECT_NAME" ]; then
    PROJECT_NAME="python-learning"
fi

# 创建目录结构
mkdir -p $PROJECT_NAME/src
mkdir -p $PROJECT_NAME/tests
mkdir -p $PROJECT_NAME/docs
mkdir -p $PROJECT_NAME/.venv

# 创建 pyproject.toml
cat > $PROJECT_NAME/pyproject.toml << EOF
[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = "Python learning project with code examples and tests"
authors = [
  { name="Learning Generator", email="learn@example.com" }
]
requires-python = ">=3.10"
dependencies = [
  "pytest>=7.0.0",
  "pytest-cov>=4.0.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = "-v --cov=src --cov-report=term-missing"

[tool.ruff]
line-length = 88
target-version = "py310"
select = ["E", "F", "I", "UP"]
ignore = []

[tool.mypy]
python_version = "3.10"
strict = true
show_error_codes = true
exclude = ["tests/"]
EOF

# 创建 .gitignore
cat > $PROJECT_NAME/.gitignore << EOF
# Virtual environment
.venv/
env/
venv/
ENV/

# Python cache
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
EOF

# 创建 README
cat > $PROJECT_NAME/README.md << EOF
# Python 学习项目

这是一个自动生成的 Python 学习项目，包含结构化的知识点文档和可运行的单元测试用例。

## 项目结构
- src/ - 知识点代码示例
- tests/ - 单元测试用例
- docs/ - 学习文档

## 环境设置
\`\`\`bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

# 安装依赖
pip install -e .[dev]
\`\`\`

## 运行测试
\`\`\`bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=src --cov-report=html
\`\`\`

## 代码质量检查
\`\`\`bash
# 代码风格检查
ruff check src/ tests/

# 类型检查
mypy src/
\`\`\`
EOF

# 创建示例代码
cat > $PROJECT_NAME/src/example.py << EOF
"""
示例代码模块
"""

def add(a: int, b: int) -> int:
    """
    两个整数相加
    
    Args:
        a: 第一个整数
        b: 第二个整数
        
    Returns:
        两个数的和
    """
    return a + b
EOF

# 创建示例测试
cat > $PROJECT_NAME/tests/test_example.py << EOF
"""
示例测试模块
"""
import pytest
from example import add


class TestExample:
    """示例测试类"""
    
    def test_add_positive_numbers(self):
        """测试正数相加"""
        assert add(2, 3) == 5
    
    def test_add_negative_numbers(self):
        """测试负数相加"""
        assert add(-2, -3) == -5
    
    def test_add_zero(self):
        """测试与零相加"""
        assert add(0, 5) == 5
        assert add(5, 0) == 5
EOF

echo "Python 项目结构已生成到 $PROJECT_NAME/"
echo "可以使用 'cd $PROJECT_NAME && python -m venv .venv && source .venv/bin/activate && pip install -e .[dev]' 初始化环境"
echo "运行测试使用 'pytest'"