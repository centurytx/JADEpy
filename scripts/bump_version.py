#!/usr/bin/env python3

import argparse
import re
import subprocess
import sys
from pathlib import Path


def get_current_version():
    """Extract current version from src/jadepy/__init__.py"""
    init_file = Path("src/jadepy/__init__.py")
    if not init_file.exists():
        raise FileNotFoundError("src/jadepy/__init__.py not found")

    content = init_file.read_text()
    match = re.search(r'__version__ = "([^"]+)"', content)
    if not match:
        raise ValueError("Version not found in src/jadepy/__init__.py")

    return match.group(1)


def parse_version(version_str):
    """Parse semantic version string into major, minor, patch components"""
    parts = version_str.split('.')
    if len(parts) != 3:
        raise ValueError(f"Invalid semantic version: {version_str}")
    
    try:
        return [int(part) for part in parts]
    except ValueError:
        raise ValueError(f"Invalid semantic version: {version_str}")


def bump_version(version_parts, bump_type):
    """Bump version based on type (major, minor, patch)"""
    major, minor, patch = version_parts
    
    if bump_type == "major":
        return [major + 1, 0, 0]
    elif bump_type == "minor":
        return [major, minor + 1, 0]
    elif bump_type == "patch":
        return [major, minor, patch + 1]
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def update_init_file(new_version):
    """Update version in src/jadepy/__init__.py"""
    init_file = Path("src/jadepy/__init__.py")
    content = init_file.read_text()
    
    updated_content = re.sub(
        r'__version__ = "[^"]+"',
        f'__version__ = "{new_version}"',
        content
    )
    
    init_file.write_text(updated_content)


def update_pyproject_file(new_version):
    """Update version in pyproject.toml"""
    pyproject_file = Path("pyproject.toml")
    if not pyproject_file.exists():
        raise FileNotFoundError("pyproject.toml not found")
    
    content = pyproject_file.read_text()
    
    updated_content = re.sub(
        r'version = "[^"]+"',
        f'version = "{new_version}"',
        content
    )
    
    pyproject_file.write_text(updated_content)


def check_git_origin():
    """Check if git origin is the expected repository"""
    try:
        result = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True,
            text=True,
            check=True
        )
        
        expected_origin = "git@github.com:centurytx/JADEpy.git"
        
        for line in result.stdout.split('\n'):
            if line.startswith("origin") and "(fetch)" in line:
                origin_url = line.split()[1]
                if origin_url == expected_origin:
                    return True
        
        return False
        
    except subprocess.CalledProcessError:
        return False


def create_git_tag(version):
    """Create and push git tag for the version"""
    tag_name = f"v{version}"
    tag_message = f"Release version v{version}"
    
    try:
        # Create annotated tag
        subprocess.run(
            ["git", "tag", "-a", tag_name, "-m", tag_message],
            check=True
        )
        
        # Push tag to origin
        subprocess.run(
            ["git", "push", "origin", tag_name],
            check=True
        )
        
        print(f"Created and pushed tag {tag_name}")
        
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to create or push git tag: {e}")


def main():
    parser = argparse.ArgumentParser(description="Bump semantic version")
    parser.add_argument(
        "action",
        choices=["major", "minor", "patch", "show", "tag"],
        help="Version bump type, 'show' to display current version, or 'tag' to create git tag"
    )
    
    args = parser.parse_args()
    
    try:
        current_version = get_current_version()
        
        if args.action == "show":
            print(current_version)
            return
        
        if args.action == "tag":
            if not check_git_origin():
                print("Error: Git origin is not git@github.com:centurytx/JADE-backend.git", file=sys.stderr)
                print("Tagging is only allowed on the main repository to prevent tags on forks.", file=sys.stderr)
                sys.exit(1)
            
            create_git_tag(current_version)
            return
        
        version_parts = parse_version(current_version)
        new_version_parts = bump_version(version_parts, args.action)
        new_version = ".".join(map(str, new_version_parts))
        
        update_init_file(new_version)
        update_pyproject_file(new_version)
        
        print(f"Version bumped from {current_version} to {new_version}")
        
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()