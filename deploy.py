import requests
import json
import base64
import os
import sys

# GitHub credentials
GITHUB_TOKEN = sys.argv[1] if len(sys.argv) > 1 else ""
USERNAME = "LastPlatform"  # verified from API
REPO_NAME = "caleb-space"
REPO_DESC = "Caleb's Space - 生物制药细胞培养工程师的个人博客"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# ── Step 1: Get username from API ──────────────────────────────────────────
def get_username():
    resp = requests.get("https://api.github.com/user", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()["login"]

# ── Step 2: Create repository ───────────────────────────────────────────────
def create_repo(username):
    url = "https://api.github.com/user/repos"
    payload = {
        "name": REPO_NAME,
        "description": REPO_DESC,
        "homepage": f"https://{username}.github.io/{REPO_NAME}",
        "private": False,
        "has_issues": True,
        "has_wiki": False,
        "auto_init": False
    }
    resp = requests.post(url, headers=HEADERS, json=payload)
    if resp.status_code == 201:
        print("[OK] Repository created.")
        return True
    elif resp.status_code == 422:
        print("[--] Repository already exists, skipping.")
        return True
    else:
        print(f"[FAIL] Repository creation failed: {resp.status_code} {resp.text}")
        return False

# ── Step 3: Upload files ─────────────────────────────────────────────────────
def upload_file(username, filepath, content_bytes):
    url = f"https://api.github.com/repos/{username}/{REPO_NAME}/contents/{filepath}"
    content_b64 = base64.b64encode(content_bytes).decode("utf-8")
    # Check if file exists (update) or new (create)
    existing = requests.get(url, headers=HEADERS)
    payload = {
        "message": f"Add {filepath}",
        "content": content_b64
    }
    if existing.status_code == 200:
        payload["sha"] = existing.json()["sha"]
    resp = requests.put(url, headers=HEADERS, json=payload)
    if resp.status_code in (200, 201):
        print(f"  [OK] {filepath}")
    else:
        print(f"  [FAIL] {filepath}: {resp.status_code}")

def upload_directory(username, local_dir):
    for root, dirs, files in os.walk(local_dir):
        # Skip .workbuddy
        if ".workbuddy" in root:
            continue
        for filename in files:
            filepath = os.path.join(root, filename)
            # Compute relative path
            rel_path = os.path.relpath(filepath, local_dir).replace("\\", "/")
            with open(filepath, "rb") as f:
                content = f.read()
            upload_file(username, rel_path, content)

# ── Step 4: Enable GitHub Pages ──────────────────────────────────────────────
def enable_pages(username):
    # First, set the Pages source via the repos API
    pages_url = f"https://api.github.com/repos/{username}/{REPO_NAME}/pages"
    # Use legacy build_type (no workflow needed)
    payload = {
        "build_type": "legacy",
        "source": {
            "branch": "main",
            "path": "/"
        }
    }
    # First try to get current pages status
    resp = requests.get(pages_url, headers=HEADERS)
    if resp.status_code == 200:
        existing = resp.json()
        print(f"[INFO] Pages already exists, branch={existing.get('source', {}).get('branch')}")
        if existing.get("source", {}).get("branch") == "main":
            return
        # Need to update
        resp = requests.post(url, headers=HEADERS, json=payload)
    elif resp.status_code == 404:
        resp = requests.post(url, headers=HEADERS, json=payload)
    else:
        print(f"[WARN] Pages status check failed: {resp.status_code}")

    if resp.status_code in (200, 201):
        print("[OK] GitHub Pages enabled.")
    else:
        print(f"[WARN] Pages enable failed: {resp.status_code} — first push may be needed first")

# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=> Deploying to GitHub...")
    username = get_username()
    print(f"=> GitHub username: {username}\n")

    if not create_repo(username):
        print("Repo creation failed, aborting.")
    else:
        print("\n=> Uploading files...")
        local_dir = r"c:\Users\Caleb\WorkBuddy\20260411205106"
        upload_directory(username, local_dir)

        print("\n=> Enabling GitHub Pages...")
        enable_pages(username)

        print(f"\n=> Done!")
        print(f"   Repo: https://github.com/{username}/{REPO_NAME}")
        print(f"   Site: https://{username}.github.io/{REPO_NAME}")
        print(f"   (GitHub Pages takes ~2-5 min to build, refresh after a moment)")
