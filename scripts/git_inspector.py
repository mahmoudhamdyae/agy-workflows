#!/usr/bin/env python3
"""
git_inspector.py - Intelligent Git Repository & State Inspector
Designed for Antigravity IDE global Git workflows (Commit & Commit-Push).
"""

import sys
import os
import re
import json
import subprocess
from typing import Dict, List, Any, Optional, Tuple

SENSITIVE_PATTERNS = [
    # Environment & secret files
    r"(^|/)\.env(\.[a-zA-Z0-9_\-]+)?$",
    r"(^|/)[a-zA-Z0-9_\-]*\.env$",
    # Private keys & certificates
    r"\.pem$",
    r"\.key$",
    r"\.pkcs12$",
    r"\.pfx$",
    r"\.p12$",
    r"\.keystore$",
    r"\.jks$",
    r"(^|/)id_(rsa|dsa|ecdsa|ed25519)(|\.pub)$",
    # Credentials & cloud keys
    r"(^|/)credentials\.json$",
    r"(^|/)service[-_]account.*\.json$",
    r"(^|/)client[-_]secret.*\.json$",
    r"(^|/)secrets?\.(json|yaml|yml|properties|xml)$",
    r"(^|/)\.secrets?$",
    # Tokens & auth
    r"(^|/)token\.json$",
    r"(^|/)auth\.json$",
    r"(^|/)oauth.*\.json$",
    r"\.token$",
    # Local files often holding keys
    r"(^|/)local\.properties$",
    r"(^|/)\.npmrc$",
    r"(^|/)\.pypirc$",
]

COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in SENSITIVE_PATTERNS]


def run_cmd(cmd: List[str], cwd: Optional[str] = None) -> Tuple[int, str, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except Exception as e:
        return -1, "", str(e)


def is_sensitive(filepath: str) -> bool:
    norm_path = filepath.replace("\\", "/")
    filename = os.path.basename(norm_path)
    for pattern in COMPILED_PATTERNS:
        if pattern.search(norm_path) or pattern.search(filename):
            return True
    return False


def inspect_git(target_dir: str = ".") -> Dict[str, Any]:
    target_dir = os.path.abspath(target_dir)

    result: Dict[str, Any] = {
        "target_dir": target_dir,
        "is_git_repo": False,
        "repo_root": None,
        "git_dir": None,
        "current_branch": None,
        "is_detached": False,
        "has_commits": False,
        "commit_count": 0,
        "recent_commits": [],
        "in_progress_op": None,
        "remotes": {},
        "upstream": None,
        "ahead": 0,
        "behind": 0,
        "is_clean": True,
        "staged": [],
        "unstaged": [],
        "untracked": [],
        "sensitive_files": [],
        "safe_to_stage": [],
    }

    # Check git installation
    code, out, _ = run_cmd(["git", "--version"])
    if code != 0:
        result["error"] = "Git is not installed or not in PATH."
        return result

    # Check inside work tree
    code, out, _ = run_cmd(["git", "rev-parse", "--is-inside-work-tree"], cwd=target_dir)
    if code != 0 or out != "true":
        result["is_git_repo"] = False
        return result

    result["is_git_repo"] = True

    # Repo root
    code, root, _ = run_cmd(["git", "rev-parse", "--show-toplevel"], cwd=target_dir)
    if code == 0:
        result["repo_root"] = root
    else:
        result["repo_root"] = target_dir

    # Git dir
    code, gdir, _ = run_cmd(["git", "rev-parse", "--git-dir"], cwd=target_dir)
    if code == 0:
        result["git_dir"] = os.path.abspath(os.path.join(target_dir, gdir)) if not os.path.isabs(gdir) else gdir

    # Branch name
    code, branch, _ = run_cmd(["git", "branch", "--show-current"], cwd=target_dir)
    if code == 0 and branch:
        result["current_branch"] = branch
        result["is_detached"] = False
    else:
        # Check if detached HEAD
        code, head_ref, _ = run_cmd(["git", "rev-parse", "--short", "HEAD"], cwd=target_dir)
        if code == 0 and head_ref:
            result["current_branch"] = f"HEAD (detached at {head_ref})"
            result["is_detached"] = True
        else:
            result["current_branch"] = "main (no commits yet)"

    # Commits check
    code, rev_count, _ = run_cmd(["git", "rev-list", "--count", "HEAD"], cwd=target_dir)
    if code == 0:
        result["has_commits"] = True
        result["commit_count"] = int(rev_count) if rev_count.isdigit() else 0

        # Recent 5 commits for style context
        code, log_out, _ = run_cmd(["git", "log", "-n", "5", "--oneline"], cwd=target_dir)
        if code == 0 and log_out:
            result["recent_commits"] = log_out.splitlines()
    else:
        result["has_commits"] = False
        result["commit_count"] = 0

    # In-progress Git operations
    if result["git_dir"] and os.path.exists(result["git_dir"]):
        gpath = result["git_dir"]
        if os.path.exists(os.path.join(gpath, "MERGE_HEAD")):
            result["in_progress_op"] = "merge"
        elif os.path.exists(os.path.join(gpath, "rebase-merge")) or os.path.exists(os.path.join(gpath, "rebase-apply")):
            result["in_progress_op"] = "rebase"
        elif os.path.exists(os.path.join(gpath, "CHERRY_PICK_HEAD")):
            result["in_progress_op"] = "cherry-pick"
        elif os.path.exists(os.path.join(gpath, "REVERT_HEAD")):
            result["in_progress_op"] = "revert"
        elif os.path.exists(os.path.join(gpath, "BISECT_LOG")):
            result["in_progress_op"] = "bisect"

    # Remotes
    code, remotes_out, _ = run_cmd(["git", "remote", "-v"], cwd=target_dir)
    if code == 0 and remotes_out:
        remotes_dict: Dict[str, Dict[str, str]] = {}
        for line in remotes_out.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                rname, rurl = parts[0], parts[1]
                rtype = parts[2].strip("()") if len(parts) >= 3 else "fetch"
                if rname not in remotes_dict:
                    remotes_dict[rname] = {}
                remotes_dict[rname][rtype] = rurl
        result["remotes"] = remotes_dict

    # Upstream branch
    code, upstream, _ = run_cmd(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], cwd=target_dir)
    if code == 0 and upstream:
        result["upstream"] = upstream
        # Ahead / behind counts
        code, counts, _ = run_cmd(["git", "rev-list", "--left-right", "--count", f"HEAD...{upstream}"], cwd=target_dir)
        if code == 0 and counts:
            parts = counts.split()
            if len(parts) == 2:
                result["ahead"] = int(parts[0])
                result["behind"] = int(parts[1])

    # Status porcelain v2
    code, status_out, _ = run_cmd(["git", "status", "--porcelain=v2", "-uall"], cwd=target_dir)
    if code == 0:
        staged_list = []
        unstaged_list = []
        untracked_list = []

        for line in status_out.splitlines():
            if not line:
                continue
            line_type = line[0]
            parts = line.split(" ")

            if line_type == "1":
                # Ordinary changed entry: 1 <XY> <sub> <mH> <mI> <mW> <hH> <hI> <path>
                xy = parts[1]
                path = " ".join(parts[8:])
                staging_state = xy[0]
                worktree_state = xy[1]

                if staging_state != ".":
                    staged_list.append({"path": path, "status": staging_state})
                if worktree_state != ".":
                    unstaged_list.append({"path": path, "status": worktree_state})

            elif line_type == "2":
                # Renamed/copied entry: 2 <XY> <sub> <mH> <mI> <mW> <hH> <hI> <X><score> <path><sep><origPath>
                xy = parts[1]
                paths = " ".join(parts[9:]).split("\t")
                path = paths[0]
                orig_path = paths[1] if len(paths) > 1 else ""
                staging_state = xy[0]
                worktree_state = xy[1]

                if staging_state != ".":
                    staged_list.append({"path": path, "orig_path": orig_path, "status": staging_state})
                if worktree_state != ".":
                    unstaged_list.append({"path": path, "orig_path": orig_path, "status": worktree_state})

            elif line_type == "u":
                # Unmerged entry
                path = " ".join(parts[10:])
                unstaged_list.append({"path": path, "status": "unmerged"})

            elif line_type == "?":
                # Untracked entry: ? <path>
                path = line[2:]
                untracked_list.append(path)

        result["staged"] = staged_list
        result["unstaged"] = unstaged_list
        result["untracked"] = untracked_list

        all_candidates = set()
        for item in staged_list:
            all_candidates.add(item["path"])
        for item in unstaged_list:
            all_candidates.add(item["path"])
        for item in untracked_list:
            all_candidates.add(item)

        sensitive_found = []
        safe_files = []

        for f in sorted(all_candidates):
            if is_sensitive(f):
                sensitive_found.append(f)
            else:
                safe_files.append(f)

        result["sensitive_files"] = sensitive_found
        result["safe_to_stage"] = safe_files
        result["is_clean"] = (len(staged_list) == 0 and len(unstaged_list) == 0 and len(untracked_list) == 0)

    return result


def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    res = inspect_git(target_dir)

    if "--json" in sys.argv:
        print(json.dumps(res, indent=2))
        return

    # Formatted Markdown Summary
    if not res["is_git_repo"]:
        print("### Git Status: NOT_A_GIT_REPOSITORY")
        print(f"Directory: `{res['target_dir']}` is not inside an initialized Git repository.")
        return

    print("### Git State Summary")
    print(f"- **Repository Root**: `{res['repo_root']}`")
    print(f"- **Current Branch**: `{res['current_branch']}`" + (" ⚠️ **(DETACHED HEAD)**" if res["is_detached"] else ""))
    print(f"- **Total Commits**: {res['commit_count']}")

    if res["in_progress_op"]:
        print(f"- ⚠️ **Operation In Progress**: `{res['in_progress_op'].upper()}`")

    if res["remotes"]:
        remote_strs = [f"`{k}` ({v.get('fetch', v.get('push', ''))})" for k, v in res["remotes"].items()]
        print(f"- **Configured Remotes**: {', '.join(remote_strs)}")
    else:
        print("- **Configured Remotes**: None (local-only repository)")

    if res["upstream"]:
        print(f"- **Upstream Tracking**: `{res['upstream']}` (Ahead: {res['ahead']}, Behind: {res['behind']})")
    else:
        print("- **Upstream Tracking**: None (branch not tracked)")

    print(f"- **Working Tree Clean**: {'Yes' if res['is_clean'] else 'No'}")

    if not res["is_clean"]:
        print("\n#### Changes Breakdown:")
        print(f"- Staged files: {len(res['staged'])}")
        print(f"- Unstaged modified/deleted: {len(res['unstaged'])}")
        print(f"- Untracked files: {len(res['untracked'])}")

        if res["sensitive_files"]:
            print("\n🚨 **SENSITIVE FILES DETECTED (MUST NOT BE STAGED)**:")
            for s in res["sensitive_files"]:
                print(f"  - `{s}`")

        print(f"\n✅ **Safe Files Eligible for Staging**: {len(res['safe_to_stage'])} file(s)")


if __name__ == "__main__":
    main()
