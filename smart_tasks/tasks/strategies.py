from datetime import datetime

def priority_score(task):
    return task.get("priority", 0) * 10

def deadline_score(task):
    deadline_str = task.get("deadline")
    if not deadline_str:
        return 0
    try:
        deadline = datetime.fromisoformat(deadline_str)
    except:
        return 0
    days_left = (deadline - datetime.now()).days
    return max(0, 30 - days_left)

def dependency_score(task, all_tasks):
    dependents_count = sum(
        1 for t in all_tasks
        if task["id"] in t.get("dependencies", [])
    )
    return dependents_count * 5

def effort_score(task):
    return max(0, 20 - task.get("effort", 0))

STRATEGY_WEIGHTS = {
    "priority": {"priority": 1.0, "deadline": 0.3, "dependency": 0.3, "effort": 0.3},
    "deadline": {"priority": 0.3, "deadline": 1.0, "dependency": 0.3, "effort": 0.3},
    "dependency": {"priority": 0.3, "deadline": 0.3, "dependency": 1.0, "effort": 0.3},
    "effort": {"priority": 0.3, "deadline": 0.3, "dependency": 0.3, "effort": 1.0},
    "overall": {"priority": 1.0, "deadline": 1.0, "dependency": 1.0, "effort": 1.0},
}

def compute_score(task, all_tasks, selected_strategy):
    weights = STRATEGY_WEIGHTS.get(selected_strategy, STRATEGY_WEIGHTS["overall"])
    score = (
        priority_score(task) * weights["priority"] +
        deadline_score(task) * weights["deadline"] +
        dependency_score(task, all_tasks) * weights["dependency"] +
        effort_score(task) * weights["effort"]
    )
    return round(score, 2)

def has_cycle(tasks):
    graph = {task["id"]: task.get("dependencies", []) for task in tasks}
    visited = set()
    rec_stack = set()

    def dfs(node):
        if node in rec_stack: return True
        if node in visited: return False
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph.get(node, []):
            if dfs(neighbor): return True
        rec_stack.remove(node)
        return False

    for task_id in graph:
        if dfs(task_id): return True
    return False
