from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from .strategies import compute_score


@api_view(["POST"])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
def analyze_tasks(request):
    data = request.data
    tasks = data.get("tasks", [])
    strategy = data.get("strategy", "overall")

    if not isinstance(tasks, list) or len(tasks) == 0:
        return Response({"error": "Task list is required"}, status=400)

    for task in tasks:
        task["score"] = compute_score(task, tasks, strategy)

    tasks.sort(key=lambda t: t["score"], reverse=True)

    return Response({
        "strategy": strategy,
        "sorted_tasks": tasks
    })


@api_view(["GET"])
def suggest_tasks(request):
    strategy = request.GET.get("strategy", "overall")

    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    task_list = serializer.data

    for task in task_list:
        task["score"] = compute_score(task, task_list, strategy)

    task_list.sort(key=lambda t: t["score"], reverse=True)
    top_three = task_list[:3]

    for task in top_three:
        task["reason"] = get_reason(task)

    return Response({
        "strategy": strategy,
        "suggestions": top_three
    })


def get_reason(task):
    reasons = []

    if task.get("priority", 0) >= 7:
        reasons.append("High priority")

    if task.get("effort", 0) <= 3:
        reasons.append("Low effort and easy to finish")

    if task.get("score", 0) >= 50:
        reasons.append("Overall high impact")

    if not reasons:
        return "Important task based on selected strategy"

    return ", ".join(reasons)
