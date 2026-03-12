#!/bin/bash

# Java 学习项目结构生成脚本
# 用法：./generate_project_structure.sh <项目名称>

PROJECT_NAME=$1
if [ -z "$PROJECT_NAME" ]; then
    PROJECT_NAME="java-learning"
fi

# 创建目录结构
mkdir -p $PROJECT_NAME/src/main/java/com/example/java/learning
mkdir -p $PROJECT_NAME/src/test/java/com/example/java/learning
mkdir -p $PROJECT_NAME/docs
mkdir -p $PROJECT_NAME/.mvn/wrapper

# 创建 pom.xml
cat > $PROJECT_NAME/pom.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>java-learning</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>8</maven.compiler.source>
        <maven.compiler.target>8</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <junit.version>5.9.2</junit.version>
    </properties>

    <dependencies>
        <!-- JUnit 5 -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-api</artifactId>
            <version>\${junit.version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-engine</artifactId>
            <version>\${junit.version}</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.1.2</version>
            </plugin>
        </plugins>
    </build>
</project>
EOF

# 创建 README
cat > $PROJECT_NAME/README.md << EOF
# Java 学习项目

这是一个自动生成的 Java 学习项目，包含结构化的知识点文档和可运行的单元测试用例。

## 项目结构
- src/main/java/ - 知识点代码示例
- src/test/java/ - 单元测试用例
- docs/ - 学习文档

## 运行测试
\`\`\`bash
mvn test
\`\`\`
EOF

echo "项目结构已生成到 $PROJECT_NAME/"
echo "可以使用 'cd $PROJECT_NAME && mvn test' 运行测试"
