# Citation Examples

Real-world examples of properly formatted research outputs.

## Example 1: TYPE B (Implementation Query)

**Query**: "How does FastAPI handle dependency injection?"

---

# 📚 FastAPI Dependency Injection Implementation

## TL;DR (요약)

FastAPI's dependency injection system uses Python's type hints and a `Depends()` function to automatically resolve and inject dependencies at request time. The core implementation lives in `fastapi/dependencies/utils.py`.

FastAPI의 의존성 주입 시스템은 Python의 타입 힌트와 `Depends()` 함수를 사용하여 요청 시점에 자동으로 의존성을 해결하고 주입합니다. 핵심 구현은 `fastapi/dependencies/utils.py`에 있습니다.

## Detailed Findings (상세 발견)

### Finding 1: Depends Function Definition

The `Depends` class is the entry point for dependency injection in FastAPI.

📍 **Evidence**: https://github.com/tiangolo/fastapi/blob/abc1234/fastapi/params.py#L45-L67

```python
class Depends:
    def __init__(
        self,
        dependency: Optional[Callable[..., Any]] = None,
        *,
        use_cache: bool = True,
    ):
        self.dependency = dependency
        self.use_cache = use_cache

    def __repr__(self) -> str:
        attr = getattr(self.dependency, "__name__", type(self.dependency).__name__)
        return f"{self.__class__.__name__}({attr})"
```

💡 **Context**: The `Depends` class stores a callable dependency and a cache flag. When `use_cache=True` (default), the same dependency instance is reused within a single request.

### Finding 2: Dependency Resolution Logic

Dependencies are resolved recursively in the `solve_dependencies` function.

📍 **Evidence**: https://github.com/tiangolo/fastapi/blob/abc1234/fastapi/dependencies/utils.py#L456-L520

```python
async def solve_dependencies(
    *,
    request: Union[Request, WebSocket],
    dependant: Dependant,
    body: Optional[Union[Dict[str, Any], FormData]] = None,
    dependency_overrides_provider: Optional[DependencyOverridesProvider] = None,
    dependency_cache: Optional[Dict[Tuple[Callable[..., Any], Tuple[str]], Any]] = None,
) -> Tuple[Dict[str, Any], List[ErrorWrapper], Optional[BackgroundTasks], ...]:
    values: Dict[str, Any] = {}
    errors: List[ErrorWrapper] = []

    for sub_dependant in dependant.dependencies:
        # Recursively solve sub-dependencies
        ...
```

💡 **Context**: This function walks the dependency tree, resolving each dependency in order. It handles both sync and async dependencies, caching results when appropriate.

## Historical Context (역사적 맥락)

### 🕵️ Why This Design?

**Issue #234**: "Support for dependency injection like Flask-Injector"

- Opened: 2019-03-15
- Discussion: Users wanted DI without external libraries

**PR #245**: "Add Depends() for dependency injection"

- Author: @tiangolo
- Decision: Use type hints for automatic injection rather than decorators

## Sources (출처)

| Type  | Link                                                                                     | Relevance                |
| ----- | ---------------------------------------------------------------------------------------- | ------------------------ |
| Code  | https://github.com/tiangolo/fastapi/blob/abc1234/fastapi/params.py#L45-L67               | Depends class definition |
| Code  | https://github.com/tiangolo/fastapi/blob/abc1234/fastapi/dependencies/utils.py#L456-L520 | Resolution logic         |
| Issue | https://github.com/tiangolo/fastapi/issues/234                                           | Original feature request |
| PR    | https://github.com/tiangolo/fastapi/pull/245                                             | Implementation PR        |
| Docs  | https://fastapi.tiangolo.com/tutorial/dependencies/                                      | Official documentation   |

---

_Research completed: 2025-01-02T10:30:00Z_
_Classification: TYPE B (Implementation)_

---

## Example 2: TYPE C (Context Query)

**Query**: "Why did React change to concurrent rendering?"

---

# 📚 React Concurrent Rendering: The Why

## TL;DR (요약)

React introduced concurrent rendering to solve UI responsiveness issues caused by synchronous rendering blocking the main thread. The decision was driven by years of research into scheduling and prioritization of updates.

React는 동기 렌더링이 메인 스레드를 차단하여 발생하는 UI 응답성 문제를 해결하기 위해 동시 렌더링을 도입했습니다. 이 결정은 업데이트의 스케줄링과 우선순위에 대한 수년간의 연구에 기반합니다.

## Detailed Findings (상세 발견)

### Finding 1: The Core Problem

📍 **Evidence**: https://github.com/facebook/react/blob/def5678/packages/react-reconciler/src/ReactFiberWorkLoop.js#L100-L125

```javascript
// The work loop is the main entry point for rendering.
// Before concurrent mode, this was synchronous and could block
// the main thread for long renders.
function workLoopSync() {
  while (workInProgress !== null) {
    performUnitOfWork(workInProgress);
  }
}

// Concurrent mode allows interruption
function workLoopConcurrent() {
  while (workInProgress !== null && !shouldYield()) {
    performUnitOfWork(workInProgress);
  }
}
```

💡 **Context**: The key difference is `shouldYield()` - concurrent rendering can pause work to let the browser handle user input.

## Historical Context (역사적 맥락)

### Timeline

1. **2017-03**: React Fiber announced (foundation for concurrent)
   - Issue #8854: "Fiber: umbrella issue"

2. **2018-03**: `<Suspense>` introduced
   - PR #12279: Initial Suspense implementation

3. **2019-10**: Concurrent Mode experimental
   - Blog post: "Introducing Concurrent Mode"

4. **2022-03**: React 18 released with concurrent features
   - PR #22380: "Enable concurrent features by default"

### Key Decision Quote

From @acdlite in PR #22380:

> "We've been working on concurrent rendering for years because we believe it's the right foundation for React's future. It allows React to prepare multiple versions of the UI at the same time."

## Sources (출처)

| Type  | Link                                                                               | Relevance                |
| ----- | ---------------------------------------------------------------------------------- | ------------------------ |
| Code  | https://github.com/facebook/react/blob/def5678/.../ReactFiberWorkLoop.js#L100-L125 | Work loop implementation |
| Issue | https://github.com/facebook/react/issues/8854                                      | Fiber umbrella issue     |
| PR    | https://github.com/facebook/react/pull/22380                                       | React 18 concurrent      |
| Blog  | https://react.dev/blog/2022/03/29/react-v18                                        | Official announcement    |

---

_Research completed: 2025-01-02T11:00:00Z_
_Classification: TYPE C (Context)_

---

## Anti-Patterns to Avoid

### ❌ Wrong: Branch-based permalink

```markdown
📍 Evidence: https://github.com/owner/repo/blob/main/file.py#L10
```

**Problem**: `main` can change; link may break or point to wrong code.

### ❌ Wrong: No line numbers

```markdown
📍 Evidence: https://github.com/owner/repo/blob/abc123/file.py
```

**Problem**: Reader must search entire file for relevant code.

### ❌ Wrong: Speculation without evidence

```markdown
FastAPI probably uses decorators for dependency injection.
```

**Problem**: No evidence provided. Either find proof or state "not found."

### ✅ Correct Format

````markdown
FastAPI uses a `Depends` class for dependency injection.

📍 **Evidence**: https://github.com/tiangolo/fastapi/blob/abc1234/fastapi/params.py#L45-L67

```python
class Depends:
    def __init__(self, dependency=None, *, use_cache=True):
        self.dependency = dependency
```
````

💡 **Context**: This class wraps callables as injectable dependencies.

```

```
