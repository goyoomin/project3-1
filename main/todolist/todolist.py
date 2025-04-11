

tasks = []

def show_todolist():
    while True:
        print("\n📋 [할 일 목록 메뉴]")
        print("1. 할 일 추가")
        print("2. 할 일 목록 보기")
        print("3. 할 일 삭제")
        print("0. 뒤로 가기")
        choice = input("원하는 작업을 선택하세요: ")

        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            delete_task()
        elif choice == '0':
            print("메인 메뉴로 돌아갑니다.")
            break
        else:
            print("❗ 잘못된 입력입니다.")

def add_task():
    task = input("➕ 추가할 할 일을 입력하세요: ")
    if task:
        tasks.append(task)
        print(f"✅ '{task}'를 추가했습니다.")
    else:
        print("⚠️ 빈 값은 추가할 수 없습니다.")

def view_tasks():
    print("\n📑 현재 할 일 목록:")
    if not tasks:
        print("🙅‍♀️ 할 일이 없습니다.")
    else:
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task}")

def delete_task():
    view_tasks()
    if tasks:
        try:
            num = int(input("❌ 삭제할 번호를 입력하세요: "))
            if 1 <= num <= len(tasks):
                removed = tasks.pop(num - 1)
                print(f"🗑️ '{removed}'를 삭제했습니다.")
            else:
                print("⚠️ 유효한 번호를 입력하세요.")
        except ValueError:
            print("⚠️ 숫자를 입력해주세요.")

if __name__ == "__main__":
    show_todolist()
