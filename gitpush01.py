import subprocess
import os
from datetime import datetime

def run_git_command(command, check=True):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if check and result.returncode != 0:
        raise Exception(f"Git command failed: {result.stderr}")
    return result

def get_current_date():
    return datetime.now().strftime("%y-%m-%d")

def get_local_branches():
    result = run_git_command("git branch")
    branches = [branch.strip().replace("*", "").strip() for branch in result.stdout.splitlines()]
    return branches

def has_unstaged_changes():
    result = run_git_command("git status --porcelain", check=False)
    return bool(result.stdout.strip())

def commit_changes(branch, date):
    if has_unstaged_changes():
        print(f"[{branch}] Adding and committing changes...")
        run_git_command("git add .")
        run_git_command(f'git commit -m "{date}"')
    else:
        print(f"[{branch}] No changes to commit.")

def main():
    # Ensure we're in a git repository
    if not os.path.exists(".git"):
        print("Error: This directory is not a Git repository.")
        return

    # Get current date for commit messages
    date = get_current_date()
    print(f"Starting process on {date}...")

    # Get all local branches
    branches = get_local_branches()
    print(f"Found branches: {', '.join(branches)}")

    # Process each branch
    for branch in branches:
        print(f"\nProcessing branch: {branch}")
        
        # Checkout branch
        print(f"[{branch}] Switching to branch...")
        run_git_command(f"git checkout {branch}")

        # Initial commit of any changes
        commit_changes(branch, date)

        # Pull from remote
        print(f"[{branch}] Pulling from remote...")
        pull_result = run_git_command("git pull origin " + branch, check=False)

        if pull_result.returncode != 0:
            # Check for conflicts
            conflict_check = run_git_command("git diff --name-only --diff-filter=U", check=False)
            if conflict_check.stdout.strip():
                conflicting_files = conflict_check.stdout.strip().splitlines()
                print(f"[{branch}] Conflict detected in files: {', '.join(conflicting_files)}")
                print(f"[{branch}] Please resolve conflicts manually and rerun the script.")
                return
            else:
                print(f"[{branch}] Pull failed for another reason: {pull_result.stderr}")
                return

        # If pull succeeded, commit any new changes and push
        commit_changes(branch, date)
        print(f"[{branch}] Pushing to remote...")
        run_git_command("git push origin " + branch)
        print(f"[{branch}] Successfully updated and pushed.")

    print("\nAll branches processed successfully!")

if __name__ == "__main__":
    main()