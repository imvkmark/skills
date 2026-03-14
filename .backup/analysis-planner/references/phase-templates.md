# Phase Templates

Common phase patterns for different project types.

## Microservices Architecture

**Phase 1: Infrastructure (2-3 docs)**
- Architecture overview, service map
- Shared libraries, utilities
- Configuration, service discovery

**Phase 2: Core Services (1 doc per service)**
- Service interface, API contracts
- Internal implementation
- Dependencies and data flow

**Phase 3: Communication (2-3 docs)**
- Inter-service communication
- Message queues, event bus
- API gateway

**Phase 4: Data Layer (2-3 docs)**
- Database design per service
- Caching strategies
- Data consistency

**Phase 5: Operations (2-3 docs)**
- Monitoring, logging, tracing
- Deployment, scaling
- Reliability, fault tolerance

**Phase 6: Summary (2-3 docs)**
- Architecture evaluation
- Best practices
- Improvement suggestions

## Monolithic Application

**Phase 1: Foundation (2-3 docs)**
- Architecture overview
- Module structure
- Core utilities

**Phase 2: Domain Modules (1 doc per module)**
- Module responsibilities
- Key classes/functions
- Module interactions

**Phase 3: Data Access (2 docs)**
- Database schema
- Repository patterns

**Phase 4: External Interfaces (2 docs)**
- API design
- Third-party integrations

**Phase 5: Cross-cutting (2-3 docs)**
- Authentication/Authorization
- Logging, error handling
- Performance

**Phase 6: Summary (2 docs)**
- Evaluation, recommendations

## Library/SDK

**Phase 1: Overview (2 docs)**
- API surface, public interfaces
- Design philosophy

**Phase 2: Core Implementation (3-4 docs)**
- Main functionality areas
- Internal architecture

**Phase 3: Integration (2 docs)**
- Usage patterns
- Extension points

**Phase 4: Quality (2 docs)**
- Testing strategies
- Documentation quality

## Document Requirement Patterns

### For Service Analysis
```markdown
**要求**:
- 服务接口定义 (API contracts)
- 核心业务逻辑
- 数据模型
- 依赖服务调用
- 错误处理策略
```

### For Data Layer Analysis
```markdown
**要求**:
- 数据模型设计
- 索引策略
- 查询优化
- 事务处理
- 数据迁移方案
```

### For Performance Analysis
```markdown
**要求**:
- 性能瓶颈识别
- 优化策略
- 并发控制
- 资源池化
- 监控指标
```

### For Summary Documents
```markdown
**要求**:
- 关键发现总结
- 架构评估
- 最佳实践提取
- 改进建议
- 技术债务识别
```
