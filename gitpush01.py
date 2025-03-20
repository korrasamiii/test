import subprocess
import os
from datetime import datetime

def run_git_command(command):
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    return process.returncode, process.stdout, process.stderr

def get_current_date():
    return datetime.now().strftime('%y-%m-%d')

def get_all_branches():
    _, output, _ = run_git_command("git branch")
    branches = [branch.strip().replace('*', '').strip() for branch in output.splitlines()]
    return branches

def commit_changes(branch, date):
    run_git_command("git checkout " + branch)
    run_git_command("git add .")
    returncode, _, stderr = run_git_command(f'git commit -m "{date}"')
    return returncode == 0 or "nothing to commit" in stderr

def pull_branch(branch):
    run_git_command("git checkout " + branch)
    returncode, _, stderr = run_git_command("git pull")
    if returncode != 0:
        conflict_files = []
        for line in stderr.splitlines():
            if "CONFLICT" in line:
                conflict_files.append(line.split("in ")[-1])
        return False, conflict_files
    return True, []

def push_branch(branch):
    run_git_command("git checkout " + branch)
    run_git_command("git push")

def main():
    if not os.path.exists(".git"):
        print("错误：当前目录不是 Git 仓库")
        return

    date = get_current_date()
    branches = get_all_branches()

    for branch in branches:
        # 提交当前修改
        commit_changes(branch, date)

        # 拉取远程更新
        success, conflict_files = pull_branch(branch)
        if not success:
            print(f"分支 '{branch}' 拉取时发生冲突，以下文件需要手动解决：")
            for file in conflict_files:
                print(f"  - {file}")
            print("请手动编辑冲突文件后重新运行程序。")
            return

        # 再次提交并推送
        if commit_changes(branch, date):
            push_branch(branch)
            print(f"分支 '{branch}' 已成功更新并推送至远程仓库")
        else:
            print(f"分支 '{branch}' 无需提交，已直接推送")

if __name__ == "__main__":
    main()