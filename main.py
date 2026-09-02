import os
import random
import subprocess
import argparse
from datetime import datetime, timedelta

def get_positive_int(prompt, default=20):
    while True:
        try:
            user_input = input(f"{prompt} (default {default}): ")
            if not user_input.strip():
                return default
            value = int(user_input)
            if value > 0:
                return value
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_repo_path(prompt, default="."):
    while True:
        user_input = input(f"{prompt} (default current directory): ")
        if not user_input.strip():
            return default
        if os.path.isdir(user_input):
            return user_input
        else:
            print("Directory does not exist. Please enter a valid path.")

def get_filename(prompt, default="data.txt"):
    user_input = input(f"{prompt} (default {default}): ")
    if not user_input.strip():
        return default
    return user_input

def random_date_in_year(year):
    start_date = datetime(year, 1, 1)
    end_date = datetime.now() if year == datetime.now().year else datetime(year + 1, 1, 1)
    date_range = int((end_date - start_date).total_seconds())
    commit_date = start_date + timedelta(seconds=random.randint(0, date_range - 1))
    return commit_date

def make_commit(date, repo_path, filename, message="graph-greener!"):
    filepath = os.path.join(repo_path, filename)
    with open(filepath, "a") as f:
        f.write(f"Commit at {date.isoformat()}\n")
    subprocess.run(["git", "add", filename], cwd=repo_path)
    env = os.environ.copy()
    date_str = date.strftime("%Y-%m-%dT%H:%M:%S")
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    subprocess.run(["git", "commit", "-m", message], cwd=repo_path, env=env)

def main():
    print("="*60)
    print("Welcome to graph-greener - GitHub Contribution Graph Commit Generator")
    print("="*60)
    print("This tool will help you fill your GitHub contribution graph with custom commits.\n")

    parser = argparse.ArgumentParser(description="Graph Greener commit generator")
    parser.add_argument("--yes", "-y", action="store_true", help="Run non-interactively using defaults")
    parser.add_argument("--num", type=int, help="Number of commits to make (used with --yes)")
    parser.add_argument("--repo", type=str, help="Path to local git repository (used with --yes)")
    parser.add_argument("--file", type=str, help="Filename to modify for commits (used with --yes)")
    parser.add_argument("--year", type=int, help="Calendar year for commit dates (used with --yes)")
    args = parser.parse_args()

    if args.yes:
        num_commits = args.num if args.num and args.num > 0 else 20
        repo_path = args.repo if args.repo else "."
        filename = args.file if args.file else "data.txt"
        commit_year = args.year if args.year else datetime.now().year
    else:
        num_commits = get_positive_int("How many commits do you want to make", 20)
        repo_path = get_repo_path("Enter the path to your local git repository", ".")
        filename = get_filename("Enter the filename to modify for commits", "data.txt")
        commit_year = datetime.now().year

    print(f"\nMaking {num_commits} commits in repo: {repo_path}\nModifying file: {filename}\n")

    for i in range(num_commits):
        commit_date = random_date_in_year(commit_year)
        print(f"[{i+1}/{num_commits}] Committing at {commit_date.strftime('%Y-%m-%d %H:%M:%S')}")
        make_commit(commit_date, repo_path, filename)

    print("\nPushing commits to your remote repository...")
    subprocess.run(["git", "push"], cwd=repo_path)
    print("✔ All done! Check your GitHub contribution graph in a few minutes.\n")
    print("Tip: Use a dedicated repository for best results. Happy coding!")

if __name__ == "__main__":
    main()