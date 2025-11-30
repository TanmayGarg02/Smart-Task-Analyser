# Smart Task Analyzer

## Overview
Smart Task Analyzer is a mini-application that intelligently scores and prioritizes tasks based on multiple factors. It helps users identify which tasks they should work on first by analyzing urgency, importance, effort, and dependencies. Additionally, it detects circular dependencies among tasks to prevent scheduling conflicts.

## Features
- Add tasks individually or in bulk (JSON input)
- Analyze tasks using multiple strategies:
  - **Fastest Wins**: Prioritizes low-effort tasks
  - **High Impact**: Prioritizes high importance
  - **Deadline Driven**: Prioritizes urgent tasks
  - **Smart Balance**: Balances importance, effort, deadline, and dependencies
- Detect circular dependencies in tasks
- Suggest top 3 tasks to work on with detailed reasoning
- Clean and responsive frontend UI
- Visual priority indicators for tasks


## Backend Logic

### 1. Task Model
Each task contains:
- `id` (auto-assigned)
- `title`
- `deadline` (YYYY-MM-DD format)
- `effort` (estimated hours)
- `priority` (1-10 scale)
- `dependencies` (list of task IDs)

### 2. Priority Scoring Algorithm
We calculate a **score** for each task using multiple factors:

1. **Priority Score**: `priority * 10`
2. **Deadline Score**: Tasks closer to the deadline get higher scores
3. **Dependency Score**: Tasks blocking others get extra points
4. **Effort Score**: Lower-effort tasks ("quick wins") get extra points

We use **weights per strategy**:

| Strategy        | Priority | Deadline | Dependency | Effort |
|-----------------|----------|----------|------------|--------|
| priority         | 1.0      | 0.3      | 0.3        | 0.3    |
| deadline         | 0.3      | 1.0      | 0.3        | 0.3    |
| dependency       | 0.3      | 0.3      | 1.0        | 0.3    |
| effort           | 0.3      | 0.3      | 0.3        | 1.0    |
| overall (smart)  | 1.0      | 1.0      | 1.0        | 1.0    |

### 3. Cycle Detection
Tasks may have circular dependencies. For example: A → B → C → A.  
We detect cycles using **DFS (Depth-First Search)** on the dependency graph and mark tasks with `"has_cycle": true`.  

### 4. API Endpoints

#### a. Create Task
`POST /api/tasks/create/`

Request body:

```json
{
    "title": "Fix login bug",
    "deadline": "2025-12-01",
    "effort": 3,
    "priority": 8,
    "dependencies": []
}
````


#### b. Analyze Tasks

`POST /api/tasks/analyze/`

Request body:
````json
{
    "tasks": [
        {"id": 1, "title": "Fix bug", "deadline": "2025-12-01", "effort": 3, "priority": 8, "dependencies": []}
    ],
    "strategy": "overall"
}
````
