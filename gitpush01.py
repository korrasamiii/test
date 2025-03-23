import os
import subprocess
from datetime import datetime

def run_git_command(command):
    return subprocess.check_output(command, shell=True, text=True).strip()

def get_branches():
    branches = run_git_command("git branch --list").splitlines()
    return [branch.replace('*', '').strip() for branch in branches]

def get_current_branch():
    return run_git_command("git rev-parse --abbrev-ref HEAD")

def display_branches(branches):
    print("当前本地分支列表：")
    for i, branch in enumerate(branches, 1):
        print(f"{i}. {branch}")

def main():
    if not os.path.exists('.git'):
        print("错误：当前目录不是一个Git仓库")
        return

    while True:
        # 获取并显示分支列表
        branches = get_branches()
        display_branches(branches)
        
        # 获取当前分支
        current_branch = get_current_branch()
        print(f"\n当前分支为：{current_branch}")
        
        # 询问是否对当前分支操作
        choice = input("是否对当前分支执行add和commit操作？(y/n): ").lower()
        if choice == 'y':
            date_str = datetime.now().strftime('%y-%m-%d')
            print(f"正在对 {current_branch} 执行 git add .")
            run_git_command("git add .")
            print(f"正在对 {current_branch} 执行 git commit，提交信息：{date_str}")
            run_git_command(f"git commit -m '{date_str}'")
            print("提交完成！")
        
        # 询问是否刷新重试
        retry = input("\n是否刷新分支列表并继续操作？(y/n): ").lower()
        if retry != 'y':
            break

    # 选择要推送的分支
    print("\n请选择要推送到远程仓库的分支序号（支持单选、多选或全选，用逗号分隔，输入'all'全选）：")
    display_branches(branches)
    selection = input("请输入序号或'all': ").strip()
    
    if selection.lower() == 'all':
        selected_branches = branches
    else:
        try:
            indices = [int(i.strip()) - 1 for i in selection.split(',')]
            selected_branches = [branches[i] for i in indices if 0 <= i < len(branches)]
        except (ValueError, IndexError):
            print("输入无效，程序结束")
            return

    # 执行推送操作
    for branch in selected_branches:
        print(f"\n正在推送分支 {branch} 到远程仓库...")
        run_git_command(f"git push origin {branch}")
        print(f"分支 {branch} 推送完成！")

    print("\n所有操作已完成！")

if __name__ == "__main__":
    main()