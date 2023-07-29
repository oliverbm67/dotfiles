"""detect_git.py print the status of the current git repository."""
import subprocess
import sys
import os

GIT_PS1_HIDE_IF_PWD_IGNORED = False
GIT_PS1_COMPRESSSPARSESTATE = False
GIT_PS1_OMITSPARSESTATE = False
GIT_PS1_SHOWCONFLICTSTATE = True
GIT_PS1_SHOWDIRTYSTATE = True
GIT_PS1_SHOWSTASHSTATE = True

def read_first_line(file):
    """Return the first line of the file"""
    with open(file, "r") as filehandler:
        lines = filehandler.readlines()
        first_line = lines[0][:-1]
        return first_line

def check_ignore_directory():
    """Return True if the current directory should be ignored by GIT"""
    if not GIT_PS1_HIDE_IF_PWD_IGNORED:
        return False
    git_config_cmd = "git config --bool bash.hideIfPwdIgnored"
    git_config = subprocess.run(git_config_cmd.split(), capture_output=True, check=True)
    if git_config.stdout == "false":
        return False
    git_ignore_cmd = "git check-ignore -q ."
    git_ignore = subprocess.run(git_ignore_cmd.split(), capture_output=True, check=True)
    if git_ignore.stdout != "":
        return False
    return True

def check_sparse():
    """Check if sparse checkout is applicable"""
    if not GIT_PS1_COMPRESSSPARSESTATE or GIT_PS1_OMITSPARSESTATE:
        return False
    git_sparse_cmd = "git config --bool core.sparseCheckout"
    git_sparse = subprocess.run(git_sparse_cmd.split(), capture_output=True,check=True)
    if git_sparse == "false":
        return False
    return True

def check_rebase(dot_git):
    """Check if the git repository is in a rebase-merge operation.
    Return (state,branch,step,total) values, empty strings if not in rebase"""
    rebase_merge_dir = os.path.join(dot_git, "rebase-merge")
    rebase_apply_dir = os.path.join(dot_git, "rebase-apply")
    rebase_rebasing_file = os.path.join(dot_git, "rebase-apply","rebasing")
    rebase_applying_file = os.path.join(dot_git, "rebase-apply","applying")
    branch = ""
    step = ""
    total = ""
    state = ""
    if os.path.isdir(rebase_merge_dir):
        branch = read_first_line(os.path.join(rebase_merge_dir, "head-name"))
        step = read_first_line(os.path.join(rebase_merge_dir, "msgnum"))
        total = read_first_line(os.path.join(rebase_merge_dir, "end"))
        state = "REBASE"
    elif os.path.isdir(rebase_apply_dir):
        step = read_first_line(os.path.join(rebase_apply_dir, "next"))
        total = read_first_line(os.path.join(rebase_apply_dir, "last"))
        if os.path.exists(rebase_rebasing_file):
            branch = read_first_line(os.path.join(rebase_apply_dir, "rebasing"))
            state = "REBASE"
        elif os.path.exists(rebase_applying_file):
            state = "AM"
        else:
            state = "AM/REBASE"
    elif os.path.exists(os.path.join(dot_git, "MERGE_HEAD")):
        state = "MERGING"
    ## TODO: Missing __git_sequencer_status
    elif os.path.exists(os.path.join(dot_git, "BISECT_LOG")):
        state = "BISECTING"
    return (state,branch,step,total)

def check_branch(dot_git):
    """Retrieve the branch name or commit hash"""
    head_file = os.path.join(dot_git, "HEAD")
    ## Check for symlink
    if os.path.islink(head_file):
        git_symref_cmd = "git symbolic-ref HEAD"
        git_symref = subprocess.run(git_symref_cmd.split(), capture_output=True, check=True)
        branch = git_symref.stdout
    elif os.path.exists(head_file):
        head = read_first_line(head_file)
        branch = head.replace("ref: ","")
        if head == branch: ## detached head
            ## TODO support formatting options of GIT_PS1_DESCRIBE_STYLE)
            git_describe_cmd = "git describe --tags --exact-match HEAD"
            git_describe = subprocess.run(git_describe_cmd.split(), capture_output=True, check=False)
            if git_describe.exitcode == 0:
                branch = git_describe.stdout
            else:
                branch = ""
    else: ## No HEAD file, something went wrong
        sys.exit()  # TODO : find appropriate error code
    return branch

def check_conflict():
    """Check for conflicts"""
    if GIT_PS1_SHOWCONFLICTSTATE:
        git_conflict_cmd = "git ls-files --unmerged"
        git_conflict = subprocess.run(git_conflict_cmd.split(), capture_output=True, check=True)
        if git_conflict.stdout != b'':
            return True
    return False

def check_dirty_state(git_short_sha):
    """Return a visual indicator for dirty state if enabled"""
    unstaged = False
    staged = False
    unknown = False
    if GIT_PS1_SHOWDIRTYSTATE:
        cmd = "git config --bool bash.showDirtyState"
        git_dirty = subprocess.run(cmd.split(), capture_output=True, check=False)
        if git_dirty.stdout != "false":
            cmd = "git diff --no-ext-diff --quiet"
            git_unstaged = subprocess.run(cmd.split(), capture_output=False, check=False)
            unstaged = bool(git_unstaged.returncode != 0)
            cmd = "git diff --no-ext-diff --cached --quiet"
            git_staged = subprocess.run(cmd.split(), capture_output=False, check=False)
            staged = bool(git_staged.returncode != 0)
            unknown = bool(git_short_sha == "" and not staged)
    return (unstaged, staged, unknown)

def check_stash_state():
    """Return a boolean value depending if there is something stashed or not"""
    if GIT_PS1_SHOWSTASHSTATE:
        git_stash_cmd = "git rev-parse --verify --quiet refs/stash"
        git_stash = subprocess.run(git_stash_cmd.split(), capture_output=True, check=False)
        if git_stash.stdout != b'':
            return True
    return False

git_rev_parse_cmd = "git rev-parse --git-dir --is-inside-git-dir \
		--is-bare-repository --is-inside-work-tree \
		--short HEAD"

## Explicit check to false because exit code is non zero outside of a git repository
rev_parse = subprocess.run(git_rev_parse_cmd.split(), capture_output=True, check=False)
## Check we are in a git repository
if rev_parse.returncode != 0:
    sys.exit()
rev_parse_str = rev_parse.stdout.decode("utf-8").split("\n")
## Extract informations
inside_gitdir = bool(rev_parse_str[1] == "true")
bare_repo = bool(rev_parse_str[2] == "true")
inside_worktree = bool(rev_parse_str[3] == "true")
short_sha = rev_parse_str[4]

if inside_worktree and check_ignore_directory():
    sys.exit()
dotgit = os.path.join(os.getcwd(), ".git")
(repo_state,branch_name,rebase_step,total_step) = check_rebase(dotgit)
if branch_name == "" :
    branch_name = check_branch(dotgit)
## check_branch may still returns empty
if branch_name == "":
    branch_name = f"{short_sha}..."
sparse = check_sparse()
conflict = check_conflict()
if inside_gitdir and not bare_repo:
    branch_name = "GIT_DIR!"
elif inside_worktree:
    (repo_unstaged, repo_staged, repo_unknown) = check_dirty_state(short_sha)
repo_stash = check_stash_state()
clean_branch_name = branch_name.replace("refs/heads/","")

status = clean_branch_name
if repo_unstaged:
    status +="*"
if repo_staged:
    status +="+"
if repo_unknown:
    status +="#"
if repo_stash:
    status +="$"
if sparse:
    status +="|SPARSE"
if conflict:
    status +="|CONFLICT"
print(status, end="")
