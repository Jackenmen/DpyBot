import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

import yarl


_current_folder = Path(__file__).absolute().parent
REPOS_FOLDER = _current_folder / "repos"
EXT_COGS_FOLDER = _current_folder.parent / "dpybot" / "ext_cogs"
INSTALLED_COGS_JSON = _current_folder / "installed_cogs.json"


def rmtree(path: Path) -> None:
    # https://docs.python.org/3.8/library/shutil.html#rmtree-example
    def remove_readonly(func: Any, path: Any, _: Any) -> None:
        "Clear the readonly bit and reattempt the removal"
        os.chmod(path, stat.S_IWRITE)
        func(path)

    shutil.rmtree(str(path), onerror=remove_readonly)


def get_installed_cogs() -> Dict[str, str]:
    # cog_name: repo_name
    if not INSTALLED_COGS_JSON.exists():
        return {}

    with INSTALLED_COGS_JSON.open(encoding="utf-8") as fp:
        return json.load(fp)


def write_installed_cogs(installed_cogs: Dict[str, str]) -> None:
    with INSTALLED_COGS_JSON.open("w", encoding="utf-8") as fp:
        return json.dump(installed_cogs, fp)


def is_valid_repo_name(name: str) -> bool:
    return (
        not name.startswith(".")
        and not name.endswith(".")
        and re.fullmatch(r"[a-zA-Z0-9_\-\.]+", name) is not None
    )


def get_installed_cog_path(name: str) -> Path:
    return EXT_COGS_FOLDER / name


def get_repo_path(name: str) -> Path:
    return REPOS_FOLDER / name


def get_cog_path(repo_name: str, cog_name: str) -> Path:
    return REPOS_FOLDER / repo_name / cog_name


def _update_repo(repo_path: Path) -> bool:
    try:
        subprocess.check_call(("git", "fetch"), cwd=str(repo_path))
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git fetch returned exit code {exc.returncode}")
        return False

    try:
        subprocess.check_call(
            ("git", "reset", "--hard", "@{upstream}"), cwd=str(repo_path)
        )
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git reset returned exit code {exc.returncode}")
        return False

    return True


def _install_cog(cog_path: Path, target_path: Path) -> None:
    if cog_path.is_dir():
        shutil.copytree(src=str(cog_path), dst=str(target_path), dirs_exist_ok=True)
    else:
        shutil.copy2(src=str(cog_path), dst=str(target_path))


def install_cog() -> None:
    print("Enter repository name:")
    repo_name = input("> ").strip()
    if not get_repo_path(repo_name).exists():
        print("ERROR: Repository with this name does not exist!")
        return
    print("Enter cog name:")
    cog_name = input("> ").strip()
    cog_path = get_cog_path(repo_name, cog_name)
    if not cog_path.exists():
        print("ERROR: Cog with this name does not exist!")
        return

    target_path = get_installed_cog_path(cog_name)
    if target_path.exists():
        print("ERROR: Cog with this name is already installed!")
        return

    installed_cogs = get_installed_cogs()
    installed_cogs[cog_name] = repo_name
    _install_cog(cog_path, target_path)
    write_installed_cogs(installed_cogs)


def uninstall_cog() -> None:
    print("Enter cog name:")
    cog_name = input("> ").strip()
    cog_path = get_installed_cog_path(cog_name)
    if cog_path.exists():
        installed_cogs = get_installed_cogs()
        installed_cogs.pop(cog_name, None)
        rmtree(cog_path)
        write_installed_cogs(installed_cogs)
    else:
        print("ERROR: Cog with this name does not exist!")


def update_cogs() -> None:
    updated_repos = set()
    failed_repos = set()
    for cog_name, repo_name in get_installed_cogs().items():
        if repo_name not in updated_repos and repo_name not in failed_repos:
            if _update_repo(get_repo_path(repo_name)):
                updated_repos.add(repo_name)
            else:
                failed_repos.add(repo_name)
                continue
        _install_cog(
            get_cog_path(repo_name, cog_name), get_installed_cog_path(cog_name)
        )
    if failed_repos:
        print(
            "Some repositories (and cogs installed from them) failed to update: "
            + ", ".join(failed_repos)
        )


def list_cogs_in_repo() -> None:
    print("Enter repository name:")
    repo_name = input("> ").strip()
    repo_path = get_repo_path(repo_name)
    for path in repo_path.iterdir():
        print(f"- {path.stem}")


def list_repositories() -> None:
    for path in REPOS_FOLDER.iterdir():
        if not path.is_dir():
            continue
        print(f"- {path.stem}")


def update_repositories() -> None:
    for repo_path in REPOS_FOLDER.iterdir():
        if not repo_path.is_dir():
            continue
        _update_repo(repo_path)


def add_repository() -> None:
    print("Enter repository address:")
    url = input("> ").strip()
    repo_name: str = ""
    for part in reversed(yarl.URL(url).parts):
        if not part or part == "/":
            continue
        if not is_valid_repo_name(part):
            break
        if get_repo_path(part).exists():
            break
        repo_name = part
        break

    if not repo_name:
        print("Couldn't automatically determine repository name.")
        while True:
            print("Enter repository name:")
            repo_name = input("> ").strip()
            if not is_valid_repo_name(repo_name):
                print(
                    "ERROR: Repo names can only contain characters A-z, numbers,"
                    " underscores, hyphens, and dots."
                )
            if get_repo_path(repo_name).exists():
                print("ERROR: This name is already taken!")
            break
    try:
        subprocess.check_call(("git", "clone", url, str(get_repo_path(repo_name))))
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git clone returned exit code {exc.returncode}")


def remove_repository() -> None:
    print("Enter repository name:")
    repo_name = input("> ").strip()
    repo_path = get_repo_path(repo_name)
    if repo_path.exists():
        rmtree(repo_path)
    else:
        print("ERROR: Repository with this name does not exist!")


ACTIONS = [
    sys.exit,
    install_cog,  # 1.
    uninstall_cog,
    update_cogs,
    list_cogs_in_repo,
    list_repositories,
    update_repositories,
    add_repository,
    remove_repository,
]


def main_menu() -> None:
    while True:
        print(
            "Choose action:\n"
            "1. Install a cog.\n"
            "2. Uninstall a cog.\n"
            "3. Update cogs.\n"
            "4. List cogs in a repository.\n"
            "5. List repositories.\n"
            "6. Update repositories.\n"
            "7. Add a repository.\n"
            "8. Remove a repository.\n"
            "0. Exit."
        )
        choice = input("> ").strip()
        try:
            func = ACTIONS[int(choice)]
        except (KeyError, ValueError):
            print("Invalid choice!\n")
        func()


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("Ctrl+C received, exiting...")
