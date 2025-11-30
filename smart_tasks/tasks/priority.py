import datetime

def calculate_priority(task, all_tasks):

    score = 0

    # 1. Urgency (closer due dates = higher score)
    due_date = task.get("due_date")
    if due_date:
        due = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
        today = datetime.date.today()
        days_left = (due - today).days

        if days_left < 0:
            # overdue tasks
            score += 40
        else:
            score += max(0, 30 - days_left)

    # 2. Importance (1-10 scale)
    importance = task.get("importance", 5)
    score += importance * 5

    # 3. Effort (low effort = quick win)
    hours = task.get("estimated_hours") or 0
    if hours > 0:
        score += max(0, 20 - hours * 2)

    # 4. Dependencies (tasks that block others get boosted)
    dependencies = task.get("dependencies", [])
    dependents_count = sum(1 for t in all_tasks if task["id"] in t.get("dependencies", []))
    score += dependents_count * 5

    return round(score, 2)
