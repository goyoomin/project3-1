from datetime import datetime, timedelta

tasks = []  # ✅ 전역 리스트 선언

@todolist_bp.route("/calendar")
def calendar_view():
    tasks_for_calendar = []

    for task in tasks:
        print("📌 원본 task:", task)
        task_data = task.copy()
        due = task.get('due', '')

        if due:
            if 'to' in due:
                start_str, end_str = due.split(' to ')
                task_data['start'] = start_str.strip()
                task_data['end'] = (datetime.strptime(end_str.strip(), '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            else:
                task_data['start'] = due.strip()
                task_data['end'] = (datetime.strptime(due.strip(), '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            task_data['start'] = None
            task_data['end'] = None

        tasks_for_calendar.append(task_data)

    print("📅 캘린더로 보낼 tasks:", tasks_for_calendar)
    return render_template("calendar.html", tasks=tasks_for_calendar)
