#!/bin/bash

# PHP 学习项目结构生成脚本
# 用法：./generate_project_structure.sh <项目名称>

PROJECT_NAME=$1
if [ -z "$PROJECT_NAME" ]; then
    PROJECT_NAME="php-learning"
fi

# 创建目录结构
mkdir -p $PROJECT_NAME/src
mkdir -p $PROJECT_NAME/tests
mkdir -p $PROJECT_NAME/docs
mkdir -p $PROJECT_NAME/public
mkdir -p $PROJECT_NAME/config
mkdir -p $PROJECT_NAME/storage/cache
mkdir -p $PROJECT_NAME/storage/logs

# 创建 composer.json
cat > $PROJECT_NAME/composer.json << EOF
{
    "name": "learning/$PROJECT_NAME",
    "description": "PHP learning project with code examples and tests",
    "type": "project",
    "require": {
        "php": "^8.0",
        "ext-json": "*"
    },
    "require-dev": {
        "phpunit/phpunit": "^9.0",
        "squizlabs/php_codesniffer": "^3.7",
        "phpstan/phpstan": "^1.10",
        "friendsofphp/php-cs-fixer": "^3.14"
    },
    "autoload": {
        "psr-4": {
            "App\\\\": "src/"
        }
    },
    "autoload-dev": {
        "psr-4": {
            "Tests\\\\": "tests/"
        }
    },
    "scripts": {
        "test": "phpunit",
        "test-coverage": "phpunit --coverage-html coverage",
        "cs-check": "phpcs",
        "cs-fix": "php-cs-fixer fix",
        "analyse": "phpstan analyse src tests --level 8"
    }
}
EOF

# 创建 phpunit.xml
cat > $PROJECT_NAME/phpunit.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="https://schema.phpunit.de/9.6/phpunit.xsd"
         bootstrap="vendor/autoload.php"
         colors="true"
         verbose="true">
    <testsuites>
        <testsuite name="Project Test Suite">
            <directory>tests</directory>
        </testsuite>
    </testsuites>
    <coverage>
        <include>
            <directory suffix=".php">src</directory>
        </include>
        <report>
            <html outputDirectory="coverage" lowUpperBound="50" highLowerBound="90"/>
        </report>
    </coverage>
</phpunit>
EOF

# 创建 .php-cs-fixer.php
cat > $PROJECT_NAME/.php-cs-fixer.php << EOF
<?php

$finder = PhpCsFixer\Finder::create()
    ->in(__DIR__ . '/src')
    ->in(__DIR__ . '/tests')
;

$config = new PhpCsFixer\Config();
return $config->setRules([
        '@PSR12' => true,
        'array_syntax' => ['syntax' => 'short'],
        'ordered_imports' => true,
        'no_unused_imports' => true,
        'return_type_declaration' => ['space_before' => 'none'],
    ])
    ->setFinder($finder)
;
EOF

# 创建 phpstan.neon
cat > $PROJECT_NAME/phpstan.neon << EOF
parameters:
    level: 8
    paths:
        - src
        - tests
    excludePaths:
        - */vendor/*
EOF

# 创建 .gitignore
cat > $PROJECT_NAME/.gitignore << EOF
# Vendor directory
vendor/
composer.lock

# PHPUnit
coverage/
.phpunit.result.cache

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs and cache
storage/logs/*.log
storage/cache/*
!storage/cache/.gitkeep

# Environment
.env
.env.local
EOF

# 创建 README
cat > $PROJECT_NAME/README.md << EOF
# PHP 学习项目

这是一个自动生成的 PHP 学习项目，包含结构化的知识点文档和可运行的单元测试用例。

## 项目结构
- src/ - 知识点代码示例
- tests/ - 单元测试用例
- public/ - Web 入口文件
- config/ - 配置文件
- docs/ - 学习文档
- storage/ - 缓存和日志文件

## 环境设置
\`\`\`bash
# 安装依赖
composer install
\`\`\`

## 常用命令
\`\`\`bash
# 运行所有测试
composer test

# 运行测试并生成覆盖率报告
composer test-coverage

# 代码风格检查
composer cs-check

# 代码风格修复
composer cs-fix

# 静态代码分析
composer analyse
\`\`\`

## 代码规范
- 遵循 PSR-12 编码规范
- 使用 PHP 7.4+ 类型声明
- 编写有意义的测试用例
- 合理使用命名空间
EOF

# 创建示例代码
cat > $PROJECT_NAME/src/Example/Calculator.php << EOF
<?php

namespace App\Example;

/**
 * 示例计算器类
 */
class Calculator
{
    /**
     * 两个整数相加
     *
     * @param int \$a 第一个整数
     * @param int \$b 第二个整数
     * @return int 两个数的和
     */
    public function add(int $a, int $b): int
    {
        return $a + $b;
    }

    /**
     * 计算多个整数的和
     *
     * @param int ...\$nums 整数列表
     * @return int 总和
     */
    public function sum(int ...$nums): int
    {
        return array_sum($nums);
    }
}
EOF

# 创建示例测试
cat > $PROJECT_NAME/tests/Unit/Example/CalculatorTest.php << EOF
<?php

namespace Tests\Unit\Example;

use App\Example\Calculator;
use PHPUnit\Framework\TestCase;

/**
 * 计算器测试类
 */
class CalculatorTest extends TestCase
{
    /**
     * 测试加法功能
     */
    public function testAdd(): void
    {
        $calculator = new Calculator();
        
        $this->assertEquals(5, $calculator->add(2, 3));
        $this->assertEquals(-5, $calculator->add(-2, -3));
        $this->assertEquals(5, $calculator->add(0, 5));
    }

    /**
     * 测试求和功能
     */
    public function testSum(): void
    {
        $calculator = new Calculator();
        
        $this->assertEquals(15, $calculator->sum(1, 2, 3, 4, 5));
        $this->assertEquals(0, $calculator->sum());
        $this->assertEquals(42, $calculator->sum(42));
    }
}
EOF

# 创建入口文件
cat > $PROJECT_NAME/public/index.php << EOF
<?php

require_once __DIR__ . '/../vendor/autoload.php';

use App\Example\Calculator;

$calculator = new Calculator();

echo "2 + 3 = " . $calculator->add(2, 3) . PHP_EOL;
echo "1+2+3+4+5 = " . $calculator->sum(1, 2, 3, 4, 5) . PHP_EOL;
EOF

# 创建必要的空文件
touch $PROJECT_NAME/storage/cache/.gitkeep
touch $PROJECT_NAME/storage/logs/.gitkeep

echo "PHP 项目结构已生成到 $PROJECT_NAME/"
echo "可以使用 'cd $PROJECT_NAME && composer install' 初始化依赖"
echo "运行测试使用 'composer test'"