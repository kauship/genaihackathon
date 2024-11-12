import os
import subprocess

def clone_or_pull_repo(repo_url, repo_dir):
    """Clone or update the repository."""
    if not os.path.exists(repo_dir):
        subprocess.run(["git", "clone", repo_url, repo_dir], check=True)
    else:
        subprocess.run(["git", "-C", repo_dir, "pull"], check=True)

def get_top_merge_commits(repo_dir, top_n=3):
    """Get the top N most recent merge commits."""
    cmd = ["git", "-C", repo_dir, "log", "--merges", "--pretty=format:%H", f"-n{top_n}"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.splitlines()

def get_diff_for_merge_commit(repo_dir, merge_commit):
    """Get the diff for the changes introduced by the pull request."""
    cmd = ["git", "-C", repo_dir, "diff", f"{merge_commit}^1", f"{merge_commit}^2"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout

def save_diffs_to_file(diffs, output_file):
    """Save the diffs to a file."""
    with open(output_file, "w") as f:
        for pr_num, diff in diffs.items():
            f.write(f"### Pull Request {pr_num} ###\n")
            f.write(diff)
            f.write("\n\n")

def main(repo_url, output_file):
    repo_dir = "temp_repo"
    # Clone or update the repository
    clone_or_pull_repo(repo_url, repo_dir)
    
    # Get the top 3 merge commits (PRs)
    merge_commits = get_top_merge_commits(repo_dir, top_n=3)
    
    # Collect diffs for each merge commit
    diffs = {}
    for i, merge_commit in enumerate(merge_commits, 1):
        diff = get_diff_for_merge_commit(repo_dir, merge_commit)
        diffs[f"PR #{i}"] = diff

    # Save diffs to output file
    save_diffs_to_file(diffs, output_file)
    print(f"Differences saved to {output_file}")

# Example usage
repo_url = "https://github.com/owner/repo.git"  # Replace with your repo URL
output_file = "pr_diffs.txt"
main(repo_url, output_file)
