#!/usr/bin/env python3
"""
project_detector.py - Multi-Stack Project & Environment Detector
Used by Antigravity IDE global workflows to detect tech stack, frameworks, tools, and configs.
"""

import sys
import os
import json
from typing import Dict, Any, List


def detect_project(root_dir: str = ".") -> Dict[str, Any]:
    root_dir = os.path.abspath(root_dir)
    res: Dict[str, Any] = {
        "root_dir": root_dir,
        "stacks": [],
        "primary_stack": "Unknown",
        "package_manager": None,
        "frameworks": [],
        "entry_points": [],
        "test_frameworks": [],
        "linters": [],
        "manifests": [],
        "doc_files": [],
        "has_git": os.path.isdir(os.path.join(root_dir, ".git")),
    }

    # Check Documentation
    for doc in ["README.md", "README", "AGENTS.md", "GEMINI.md", "DESIGN.md", "ARCHITECTURE.md", "CONTRIBUTING.md"]:
        if os.path.isfile(os.path.join(root_dir, doc)):
            res["doc_files"].append(doc)

    # 1. Flutter / Dart
    pubspec = os.path.join(root_dir, "pubspec.yaml")
    if os.path.isfile(pubspec):
        res["stacks"].append("Dart")
        res["manifests"].append("pubspec.yaml")
        try:
            with open(pubspec, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if "flutter:" in content or "sdk: flutter" in content:
                    res["stacks"].append("Flutter")
                    res["frameworks"].append("Flutter")
                    res["primary_stack"] = "Flutter"
                else:
                    res["primary_stack"] = "Dart"
        except Exception:
            pass
        res["package_manager"] = "flutter/pub"
        res["test_frameworks"].append("flutter_test" if "Flutter" in res["stacks"] else "test")
        res["linters"].append("dart analyze")
        if os.path.isfile(os.path.join(root_dir, "lib", "main.dart")):
            res["entry_points"].append("lib/main.dart")

    # 2. Node.js / TypeScript / JavaScript (React, Next.js, Vue, Angular, Nest, Express)
    pkg_json = os.path.join(root_dir, "package.json")
    if os.path.isfile(pkg_json):
        res["stacks"].append("JavaScript/Node.js")
        res["manifests"].append("package.json")
        if os.path.isfile(os.path.join(root_dir, "tsconfig.json")):
            res["stacks"].append("TypeScript")

        # Package manager detection
        if os.path.isfile(os.path.join(root_dir, "pnpm-lock.yaml")):
            res["package_manager"] = "pnpm"
        elif os.path.isfile(os.path.join(root_dir, "yarn.lock")):
            res["package_manager"] = "yarn"
        elif os.path.isfile(os.path.join(root_dir, "bun.lockb")) or os.path.isfile(os.path.join(root_dir, "bun.lock")):
            res["package_manager"] = "bun"
        else:
            res["package_manager"] = "npm"

        try:
            with open(pkg_json, "r", encoding="utf-8", errors="ignore") as f:
                data = json.load(f)
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                scripts = data.get("scripts", {})

                if "next" in deps:
                    res["frameworks"].append("Next.js")
                    if res["primary_stack"] == "Unknown":
                        res["primary_stack"] = "Next.js"
                elif "react" in deps:
                    res["frameworks"].append("React")
                    if res["primary_stack"] == "Unknown":
                        res["primary_stack"] = "React"
                if "vue" in deps:
                    res["frameworks"].append("Vue")
                if "@angular/core" in deps:
                    res["frameworks"].append("Angular")
                if "express" in deps:
                    res["frameworks"].append("Express")
                if "@nestjs/core" in deps:
                    res["frameworks"].append("NestJS")

                if "jest" in deps or "jest" in scripts.get("test", ""):
                    res["test_frameworks"].append("Jest")
                if "vitest" in deps:
                    res["test_frameworks"].append("Vitest")
                if "playwright" in deps or "@playwright/test" in deps:
                    res["test_frameworks"].append("Playwright")
                if "cypress" in deps:
                    res["test_frameworks"].append("Cypress")

                if "eslint" in deps:
                    res["linters"].append("ESLint")
                if "prettier" in deps:
                    res["linters"].append("Prettier")
                if "biome" in deps or "@biomejs/biome" in deps:
                    res["linters"].append("Biome")

                for ep in ["src/index.ts", "src/index.js", "src/main.tsx", "src/main.ts", "pages/_app.tsx", "app/layout.tsx", "server.js", "index.js"]:
                    if os.path.isfile(os.path.join(root_dir, ep)):
                        res["entry_points"].append(ep)
        except Exception:
            pass

    # 3. PHP / Laravel
    composer = os.path.join(root_dir, "composer.json")
    if os.path.isfile(composer):
        res["stacks"].append("PHP")
        res["manifests"].append("composer.json")
        res["package_manager"] = res["package_manager"] or "composer"
        try:
            with open(composer, "r", encoding="utf-8", errors="ignore") as f:
                cdata = json.load(f)
                cdeps = {**cdata.get("require", {}), **cdata.get("require-dev", {})}
                if "laravel/framework" in cdeps:
                    res["frameworks"].append("Laravel")
                    res["primary_stack"] = "Laravel"
                if "phpunit/phpunit" in cdeps:
                    res["test_frameworks"].append("PHPUnit")
                if "pestphp/pest" in cdeps:
                    res["test_frameworks"].append("Pest")
                if "phpstan/phpstan" in cdeps:
                    res["linters"].append("PHPStan")
                if "laravel/pint" in cdeps:
                    res["linters"].append("Laravel Pint")
        except Exception:
            pass
        if os.path.isfile(os.path.join(root_dir, "artisan")):
            res["entry_points"].append("artisan")

    # 4. Python (Django, FastAPI, Flask)
    for py_manifest in ["pyproject.toml", "requirements.txt", "Pipfile", "setup.py"]:
        if os.path.isfile(os.path.join(root_dir, py_manifest)):
            res["stacks"].append("Python")
            res["manifests"].append(py_manifest)
            if res["primary_stack"] == "Unknown":
                res["primary_stack"] = "Python"
            break

    # 5. Rust
    if os.path.isfile(os.path.join(root_dir, "Cargo.toml")):
        res["stacks"].append("Rust")
        res["manifests"].append("Cargo.toml")
        if res["primary_stack"] == "Unknown":
            res["primary_stack"] = "Rust"

    # 6. Go
    if os.path.isfile(os.path.join(root_dir, "go.mod")):
        res["stacks"].append("Go")
        res["manifests"].append("go.mod")
        if res["primary_stack"] == "Unknown":
            res["primary_stack"] = "Go"

    return res


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    data = detect_project(target)
    if "--json" in sys.argv:
        print(json.dumps(data, indent=2))
        return

    print("### Project Tech Stack Summary")
    print(f"- **Root**: `{data['root_dir']}`")
    print(f"- **Primary Stack**: **{data['primary_stack']}**")
    print(f"- **Detected Stacks**: {', '.join(data['stacks']) if data['stacks'] else 'Generic'}")
    print(f"- **Frameworks**: {', '.join(data['frameworks']) if data['frameworks'] else 'None detected'}")
    print(f"- **Package Manager**: {data['package_manager'] or 'N/A'}")
    print(f"- **Test Frameworks**: {', '.join(data['test_frameworks']) if data['test_frameworks'] else 'None'}")
    print(f"- **Linters/Analyzers**: {', '.join(data['linters']) if data['linters'] else 'None'}")
    print(f"- **Manifests**: {', '.join(data['manifests']) if data['manifests'] else 'None'}")
    print(f"- **Documentation Files**: {', '.join(data['doc_files']) if data['doc_files'] else 'None'}")


if __name__ == "__main__":
    main()
