#!/bin/bash

# Go 学习项目结构生成脚本
# 用法：./generate_project_structure.sh <项目名称>

PROJECT_NAME=$1
if [ -z "$PROJECT_NAME" ]; then
    PROJECT_NAME="go-learning"
fi

# 创建目录结构
mkdir -p $PROJECT_NAME/cmd
mkdir -p $PROJECT_NAME/internal
mkdir -p $PROJECT_NAME/pkg
mkdir -p $PROJECT_NAME/test
mkdir -p $PROJECT_NAME/docs
mkdir -p $PROJECT_NAME/scripts

# 创建 go.mod
cat > $PROJECT_NAME/go.mod << EOF
module $PROJECT_NAME

go 1.21

require (
	github.com/stretchr/testify v1.8.4
)
EOF

# 创建 Makefile
cat > $PROJECT_NAME/Makefile << EOF
.PHONY: all test build clean lint coverage

# Default target
all: test build

# Run tests
test:
	go test -v ./...

# Run tests with coverage
coverage:
	go test -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html

# Run linter
lint:
	golangci-lint run ./...

# Build the project
build:
	go build -o bin/ ./cmd/...

# Clean build artifacts
clean:
	rm -rf bin/
	rm -f coverage.out coverage.html
EOF

# 创建 .gitignore
cat > $PROJECT_NAME/.gitignore << EOF
# Binaries
bin/
*.exe
*.dll
*.so
*.dylib

# Go files
*.out
*.test
*.prof

# Dependencies
vendor/
go.sum

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Coverage
coverage.out
coverage.html
EOF

# 创建 README
cat > $PROJECT_NAME/README.md << EOF
# Go 学习项目

这是一个自动生成的 Go 学习项目，包含结构化的知识点文档和可运行的单元测试用例。

## 项目结构
遵循 Go 标准项目布局：
- cmd/ - 主应用程序入口
- internal/ - 内部私有包
- pkg/ - 可公开使用的包
- test/ - 额外的测试代码
- docs/ - 学习文档
- scripts/ - 脚本文件

## 环境设置
\`\`\`bash
# 安装依赖
go mod download

# 安装开发工具
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
go install github.com/stretchr/testify@latest
\`\`\`

## 常用命令
\`\`\`bash
# 运行所有测试
make test
# 或者直接使用 go 命令
go test -v ./...

# 运行测试并生成覆盖率报告
make coverage

# 运行代码检查
make lint

# 构建项目
make build
\`\`\`

## 代码规范
- 遵循 Go 官方编码规范
- 使用 gofmt 自动格式化代码
- 遵循 Go 项目标准布局
- 编写有意义的测试用例
EOF

# 创建示例代码
cat > $PROJECT_NAME/pkg/example/example.go << EOF
/*
示例代码包
*/
package example

// Add 两个整数相加
func Add(a int, b int) int {
	return a + b
}

// Sum 计算多个整数的和
func Sum(nums ...int) int {
	total := 0
	for _, num := range nums {
		total += num
	}
	return total
}
EOF

# 创建示例测试
cat > $PROJECT_NAME/pkg/example/example_test.go << EOF
/*
示例测试包
*/
package example

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestAdd(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name     string
		a        int
		b        int
		expected int
	}{
		{
			name:     "正数相加",
			a:        2,
			b:        3,
			expected: 5,
		},
		{
			name:     "负数相加",
			a:        -2,
			b:        -3,
			expected: -5,
		},
		{
			name:     "零相加",
			a:        0,
			b:        5,
			expected: 5,
		},
	}

	for _, tt := range tests {
		tt := tt
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			result := Add(tt.a, tt.b)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestSum(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name     string
		nums     []int
		expected int
	}{
		{
			name:     "多个数求和",
			nums:     []int{1, 2, 3, 4, 5},
			expected: 15,
		},
		{
			name:     "空数组求和",
			nums:     []int{},
			expected: 0,
		},
		{
			name:     "单个数字求和",
			nums:     []int{42},
			expected: 42,
		},
	}

	for _, tt := range tests {
		tt := tt
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			result := Sum(tt.nums...)
			assert.Equal(t, tt.expected, result)
		})
	}
}
EOF

# 创建主程序入口
cat > $PROJECT_NAME/cmd/main.go << EOF
/*
主程序入口
*/
package main

import (
	"fmt"

	"$PROJECT_NAME/pkg/example"
)

func main() {
	fmt.Printf("2 + 3 = %d\n", example.Add(2, 3))
	fmt.Printf("1+2+3+4+5 = %d\n", example.Sum(1, 2, 3, 4, 5))
}
EOF

echo "Go 项目结构已生成到 $PROJECT_NAME/"
echo "可以使用 'cd $PROJECT_NAME && go mod download' 初始化依赖"
echo "运行测试使用 'go test -v ./...' 或 'make test'"