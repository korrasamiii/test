import os
import subprocess
import sys

def get_git_repos():
    print("正在扫描当前目录中的所有 .git 仓库...")
    repos = [item for item in os.listdir('.') if os.path.isdir(item) and os.path.exists(os.path.join(item, '.git'))]
    if not repos:
        print("未找到任何 .git 仓库，程序结束。")
        sys.exit(0)
    for i, repo in enumerate(repos):
        print(f"{i}. {repo}")
    return repos

def select_repos(repos):
    print("\n请选择需要操作的仓库：")
    print("输入序号（如 0 或 0,1,2）进行单选/多选，输入 'all' 全选")
    choice = input("请输入您的选择：").strip().lower()
    
    if choice == 'all':
        return repos
    else:
        try:
            indices = [int(x.strip()) for x in choice.split(',')]
            selected = [repos[i] for i in indices if 0 <= i < len(repos)]
            if not selected:
                print("选择无效，程序结束。")
                sys.exit(0)
            print(f"已选择仓库：{selected}")
            return selected
        except (ValueError, IndexError):
            print("输入无效，程序结束。")
            sys.exit(0)

def get_branches(repo):
    print(f"正在获取仓库 {repo} 的所有分支...")
    os.chdir(repo)
    result = subprocess.run(['git', 'branch'], capture_output=True, text=True)
    branches = [line.strip().replace('*', '').strip() for line in result.stdout.splitlines()]
    os.chdir('..')
    print(f"仓库 {repo} 的分支：{branches}")
    return branches

def pull_branch(repo, branch):
    print(f"正在处理仓库 {repo} 的分支 {branch}...")
    os.chdir(repo)
    subprocess.run(['git', 'checkout', branch], capture_output=True, text=True)
    print(f"已切换到 {repo} 的 {branch} 分支，开始执行 git pull...")
    result = subprocess.run(['git', 'pull'], capture_output=True, text=True)
    os.chdir('..')
    
    if result.returncode != 0:
        print(f"警告：仓库 {repo} 的分支 {branch} 在拉取时发生冲突！")
        error_output = result.stderr
        conflicting_files = []
        for line in error_output.splitlines():
            if 'merge' in line.lower() or 'conflict' in line.lower():
                print(line)
            if 'path' in line.lower():
                conflicting_files.append(line.split(':')[-1].strip())
        print(f"发生冲突的文件：{conflicting_files}")
        print("请手动解决冲突后重新运行程序。")
        print("程序即将终止，请关闭当前窗口。")
        sys.exit(1)
    else:
        print(f"仓库 {repo} 的分支 {branch} 已成功拉取最新状态。")

def main():
    repos = get_git_repos()
    selected_repos = select_repos(repos)
    
    for repo in selected_repos:
        branches = get_branches(repo)
        for branch in branches:
            pull_branch(repo, branch)
    
    print("所有选定仓库的分支已处理完成！")

if __name__ == "__main__":
    main()
