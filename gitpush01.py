import os
import subprocess
from datetime import datetime

def is_git_repo():
    return os.path.isdir(".git")

def get_branches():
    result = subprocess.run(["git", "branch"], capture_output=True, text=True)
    branches = [line.strip()[2:] if line.startswith("*") else line.strip() for line in result.stdout.splitlines()]
    return branches

def get_current_branch():
    result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
    return result.stdout.strip()

def display_branches(branches):
    print("当前分支列表：")
    for i, branch in enumerate(branches):
        print(f"{i}. {branch}")

def commit_current_branch():
    date_str = datetime.now().strftime("%y-%m-%d")
    print("正在提交当前分支...")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"提交日期：{date_str}"])
    print("提交完成！")

def push_branches(selected_branches, all_branches):
    for idx in selected_branches:
        branch = all_branches[idx]
        print(f"正在推送分支 {branch} 到远程仓库...")
        subprocess.run(["git", "push", "origin", branch])
        print(f"分支 {branch} 推送完成！")

def main():
    if not is_git_repo():
        print("错误：当前目录不是 Git 仓库！")
        return

    while True:
        branches = get_branches()
        display_branches(branches)
        
        current_branch = get_current_branch()
        print(f"当前分支：{current_branch}")
        
        choice = input("是否提交当前分支？(y/n)：").lower()
        if choice == 'y':
            commit_current_branch()
        
        selection = input("请选择要推送的分支序号（例如：1 或 1,2 或 all）：").strip()
        if not selection:
            retry = input("是否返回刷新分支？(y/n)：").lower()
            if retry == 'y':
                continue
            else:
                print("操作结束。")
                break
        
        if selection.lower() == "all":
            selected_indices = list(range(len(branches)))
        else:
            selected_indices = [int(x.strip()) for x in selection.split(",") if x.strip().isdigit()]
            if not all(0 <= i < len(branches) for i in selected_indices):
                print("错误：无效的分支序号！")
                continue
        
        push_branches(selected_indices, branches)
        
        retry = input("是否返回刷新分支？(y/n)：").lower()
        if retry != 'y':
            print("操作结束。")
            break

if __name__ == "__main__":
    main()