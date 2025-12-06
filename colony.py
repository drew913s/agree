#!/usr/bin/env python3
"""Colony Manager - Ant Colony Development Dashboard for Agree."""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PLAN_FILE = Path(__file__).parent / "plan.json"
BRICKS_DIR = Path(__file__).parent / "bricks"

# ANSI colors
C = {
    "reset": "\033[0m", "bold": "\033[1m", "dim": "\033[2m",
    "green": "\033[92m", "yellow": "\033[93m", "red": "\033[91m",
    "blue": "\033[94m", "cyan": "\033[96m", "magenta": "\033[95m",
}


def load_plan() -> dict:
    """Load the master plan.json file."""
    if not PLAN_FILE.exists():
        print(f"{C['red']}Error: plan.json not found{C['reset']}")
        sys.exit(1)
    with open(PLAN_FILE) as f:
        return json.load(f)


def save_plan(plan: dict) -> None:
    """Save the master plan.json file."""
    with open(PLAN_FILE, "w") as f:
        json.dump(plan, f, indent=2)


def count_lines(filepath: Path) -> int:
    """Count non-blank, non-comment lines in a Python file."""
    if not filepath.exists():
        return 0
    count = 0
    with open(filepath) as f:
        for line in f:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                count += 1
    return count


def validate_brick(brick_path: Path) -> dict:
    """Validate a brick file and return validation result."""
    result = {"exists": False, "lines": 0, "valid": False, "has_meta": False,
              "has_tests": False, "errors": []}

    if not brick_path.exists():
        return result

    result["exists"] = True
    result["lines"] = count_lines(brick_path)

    if result["lines"] > 50:
        result["errors"].append(f"Exceeds 50 lines ({result['lines']} lines)")

    # Check for meta.json
    meta_path = brick_path.with_suffix(".meta.json")
    result["has_meta"] = meta_path.exists()
    if not result["has_meta"]:
        result["errors"].append("Missing .meta.json file")

    # Check for test file
    test_path = brick_path.parent / f"test_{brick_path.name}"
    result["has_tests"] = test_path.exists()

    # Check return format
    with open(brick_path) as f:
        content = f.read()
        if "{'result':" not in content and '{"result":' not in content:
            if "return {" in content or "return{" in content:
                pass  # Might be using dict literal
            else:
                result["errors"].append("May not follow {'result': X, 'error': Y} format")

    result["valid"] = len(result["errors"]) == 0 and result["lines"] <= 50
    return result


def progress_bar(current: int, total: int, width: int = 20) -> str:
    """Generate a progress bar string."""
    if total == 0:
        return "[" + " " * width + "]"
    filled = int(width * current / total)
    return "[" + "=" * filled + " " * (width - filled) + "]"


def cmd_plan(args: argparse.Namespace, plan: dict) -> None:
    """Display the full project plan."""
    if args.json:
        print(json.dumps(plan, indent=2))
        return

    proj = plan["project"]
    summary = plan["summary"]

    print(f"\n{C['bold']}{'=' * 78}{C['reset']}")
    print(f"{C['bold']}{C['cyan']}{'AGREE - ENTERPRISE AGREEMENT SIGNING':^78}{C['reset']}")
    print(f"{C['bold']}{C['cyan']}{'Full Project Plan':^78}{C['reset']}")
    print(f"{C['bold']}{'=' * 78}{C['reset']}")
    print(f" Methodology: {proj['methodology']}")
    print(f" Total Bricks: {summary['total_bricks']} | Completed: {summary['completed']} | Progress: {summary['progress_percent']:.1f}%")
    print(f"{C['bold']}{'=' * 78}{C['reset']}\n")

    for wave in plan["waves"]:
        status_color = C['green'] if wave['status'] == 'completed' else (
            C['yellow'] if wave['status'] == 'pending' else C['dim'])
        print(f"{C['bold']}{status_color}WAVE {wave['id']}: {wave['name'].upper()}{C['reset']}")
        print("-" * 78)

        for princess in wave["princesses"]:
            completed = sum(1 for b in princess["bricks"] if b["status"] == "completed")
            total = len(princess["bricks"])
            pct = (completed / total * 100) if total > 0 else 0

            status_icon = {
                "unassigned": " ",
                "assigned": "->",
                "in_progress": ">>",
                "completed": "OK",
                "blocked": "XX"
            }.get(princess["status"], "??")

            bar = progress_bar(completed, total)
            assigned = princess.get("assigned_to") or "Unassigned"

            print(f"  {C['bold']}{princess['id']}{C['reset']} {princess['domain'].upper():12} {bar} {pct:5.1f}% [{status_icon}] {assigned}")

            for brick in princess["bricks"][:3]:  # Show first 3
                icon = {"pending": " ", "in_progress": ">", "completed": "x", "invalid": "!"}.get(brick["status"], "?")
                line_info = f"({brick['lines']} lines)" if brick.get("lines") else ""
                print(f"      [{icon}] {brick['name']}.py {line_info}")

            if len(princess["bricks"]) > 3:
                print(f"      ... ({len(princess['bricks']) - 3} more)")
        print()

    # Tech stack footer
    tech = plan["tech_stack"]
    print(f"{'=' * 78}")
    print(f"TECH: {tech['backend']} | {tech['frontend']} | {tech['database']} | {tech['cache']}")
    sec = plan["security"]
    print(f"SECURITY: {sec['encryption']} | {sec['passwords']} | {sec['tokens']} | {sec['audit']}")
    print(f"{'=' * 78}\n")


def cmd_status(args: argparse.Namespace, plan: dict) -> None:
    """Display current colony status dashboard."""
    if args.json:
        status = {"timestamp": datetime.now(timezone.utc).isoformat(), "waves": []}
        for wave in plan["waves"]:
            wave_data = {"id": wave["id"], "name": wave["name"], "status": wave["status"], "domains": []}
            for p in wave["princesses"]:
                completed = sum(1 for b in p["bricks"] if b["status"] == "completed")
                wave_data["domains"].append({
                    "id": p["id"], "domain": p["domain"], "status": p["status"],
                    "completed": completed, "total": len(p["bricks"]),
                    "progress_percent": (completed / len(p["bricks"]) * 100) if p["bricks"] else 0
                })
            status["waves"].append(wave_data)
        status["summary"] = plan["summary"]
        print(json.dumps(status, indent=2))
        return

    print(f"\n{C['bold']}{'=' * 62}{C['reset']}")
    print(f"{C['bold']}{C['cyan']}{'AGREE COLONY STATUS':^62}{C['reset']}")
    print(f"{C['bold']}{'=' * 62}{C['reset']}\n")

    for wave in plan["waves"]:
        status_color = C['green'] if wave['status'] == 'completed' else (
            C['yellow'] if wave['status'] in ('pending', 'in_progress') else C['dim'])
        print(f"{status_color}{C['bold']}Wave {wave['id']} - {wave['name']}{C['reset']}")
        print(f"{'Domain':<14} {'Status':<10} {'Bricks':<10} {'Progress':<24}")
        print("-" * 62)

        for p in wave["princesses"]:
            completed = sum(1 for b in p["bricks"] if b["status"] == "completed")
            total = len(p["bricks"])
            bar = progress_bar(completed, total)
            pct = (completed / total * 100) if total > 0 else 0

            status_icon = {"unassigned": " ", "assigned": "->", "in_progress": ">>",
                          "completed": "OK", "blocked": "XX"}.get(p["status"], "??")

            print(f"{p['id']} {p['domain']:<8} {status_icon:<10} {completed}/{total:<8} {bar} {pct:5.1f}%")
        print()

    summary = plan["summary"]
    print(f"{'=' * 62}")
    print(f"Total: {summary['completed']}/{summary['total_bricks']} bricks ({summary['progress_percent']:.1f}%)")
    print(f"{'=' * 62}\n")


def cmd_roles(args: argparse.Namespace, plan: dict) -> None:
    """List all Princess roles with their responsibilities."""
    if args.json:
        roles = []
        for wave in plan["waves"]:
            for p in wave["princesses"]:
                roles.append({
                    "id": p["id"], "domain": p["domain"], "description": p["description"],
                    "status": p["status"], "assigned_to": p.get("assigned_to"),
                    "brick_count": len(p["bricks"]), "wave": wave["id"]
                })
        print(json.dumps(roles, indent=2))
        return

    print(f"\n{C['bold']}Princess Roles{C['reset']}\n")
    print(f"{'ID':<8} {'Domain':<14} {'Status':<12} {'Bricks':<8} Description")
    print("-" * 78)

    for wave in plan["waves"]:
        for p in wave["princesses"]:
            status = p["status"]
            if p.get("assigned_to"):
                status = f"-> {p['assigned_to'][:15]}"
            print(f"{p['id']:<8} {p['domain']:<14} {status:<12} {len(p['bricks']):<8} {p['description']}")
    print()


def cmd_domain(args: argparse.Namespace, plan: dict) -> None:
    """Show details for a specific domain."""
    domain_id = args.domain_id.upper()

    target = None
    for wave in plan["waves"]:
        for p in wave["princesses"]:
            if p["id"] == domain_id or p["domain"].lower() == args.domain_id.lower():
                target = p
                break

    if not target:
        print(f"{C['red']}Error: Domain '{args.domain_id}' not found{C['reset']}")
        return

    if args.json:
        print(json.dumps(target, indent=2))
        return

    print(f"\n{C['bold']}{C['cyan']}{target['id']} - {target['domain'].upper()}{C['reset']}")
    print(f"Description: {target['description']}")
    print(f"Status: {target['status']}")
    if target.get("assigned_to"):
        print(f"Assigned to: {target['assigned_to']}")
    print(f"\n{'Brick':<24} {'Status':<12} {'Lines':<8} {'Valid'}")
    print("-" * 60)

    for brick in target["bricks"]:
        brick_path = BRICKS_DIR / target["domain"] / f"{brick['name']}.py"
        validation = validate_brick(brick_path)

        status = brick["status"]
        lines = validation["lines"] if validation["exists"] else "-"
        valid = "Yes" if validation["valid"] else ("No" if validation["exists"] else "-")

        print(f"{brick['name']:<24} {status:<12} {str(lines):<8} {valid}")
    print()


def cmd_session(args: argparse.Namespace, plan: dict) -> None:
    """Generate a session prompt for a Princess."""
    domain_id = args.domain_id.upper()

    target = None
    for wave in plan["waves"]:
        for p in wave["princesses"]:
            if p["id"] == domain_id or p["domain"].lower() == args.domain_id.lower():
                target = p
                break

    if not target:
        print(f"{C['red']}Error: Domain '{args.domain_id}' not found{C['reset']}")
        return

    prompt = f"""# Princess {target['id']}: {target['domain'].title()} Domain

You are Princess {target['id']}, responsible for building the {target['domain'].title()} domain bricks.

## Project Context
- **Project**: Agree - Enterprise Agreement Signing Platform
- **Your Domain**: {target['domain'].title()} ({target['description']})
- **Working Directory**: {Path(__file__).parent.absolute()}
- **Brick Location**: bricks/{target['domain']}/

## Brick Rules
1. Maximum 50 lines of code (excluding comments/blanks)
2. Return format: {{'result': X, 'error': str|None}}
3. Create {{name}}.py + {{name}}.meta.json + test_{{name}}.py for each brick
4. No banned patterns (eval, exec, shell=True, etc.)

## Your Assigned Bricks (in order)
"""

    for i, brick in enumerate(target["bricks"], 1):
        prompt += f"\n### {i}. {brick['name']}.py\n"
        prompt += f"**Purpose**: {brick['description']}\n"
        prompt += f"**File**: {brick['file']}\n"
        prompt += f"**Status**: {brick['status']}\n"

    prompt += f"""
## When Complete
After building each brick, run:
```
python colony.py complete {target['domain']}/{{brick_name}}
```

This updates the master plan and notifies the Queen.

## Start Now
Begin with: {target['bricks'][0]['name']}.py
"""

    if args.json:
        print(json.dumps({"princess_id": target["id"], "domain": target["domain"], "prompt": prompt}))
    else:
        print(prompt)


def cmd_validate(args: argparse.Namespace, plan: dict) -> None:
    """Validate all bricks in the project."""
    results = {"valid": 0, "invalid": 0, "missing": 0, "details": []}

    for wave in plan["waves"]:
        for princess in wave["princesses"]:
            for brick in princess["bricks"]:
                brick_path = BRICKS_DIR / princess["domain"] / f"{brick['name']}.py"
                validation = validate_brick(brick_path)

                detail = {
                    "domain": princess["domain"],
                    "brick": brick["name"],
                    "path": str(brick_path),
                    **validation
                }
                results["details"].append(detail)

                if not validation["exists"]:
                    results["missing"] += 1
                elif validation["valid"]:
                    results["valid"] += 1
                else:
                    results["invalid"] += 1

    if args.json:
        print(json.dumps(results, indent=2))
        return

    print(f"\n{C['bold']}Brick Validation Results{C['reset']}\n")
    print(f"Valid: {C['green']}{results['valid']}{C['reset']} | Invalid: {C['red']}{results['invalid']}{C['reset']} | Missing: {C['dim']}{results['missing']}{C['reset']}\n")

    # Show invalid bricks
    for detail in results["details"]:
        if detail["exists"] and not detail["valid"]:
            print(f"{C['red']}INVALID{C['reset']} {detail['domain']}/{detail['brick']}.py")
            for err in detail["errors"]:
                print(f"  - {err}")

    # Show valid bricks
    if args.verbose:
        print(f"\n{C['green']}Valid bricks:{C['reset']}")
        for detail in results["details"]:
            if detail["valid"]:
                print(f"  {detail['domain']}/{detail['brick']}.py ({detail['lines']} lines)")
    print()


def cmd_complete(args: argparse.Namespace, plan: dict) -> None:
    """Mark a brick as complete."""
    parts = args.brick_path.split("/")
    if len(parts) != 2:
        print(f"{C['red']}Error: Use format domain/brick_name{C['reset']}")
        return

    domain, brick_name = parts
    brick_name = brick_name.replace(".py", "")

    # Find and update the brick
    found = False
    for wave in plan["waves"]:
        for princess in wave["princesses"]:
            if princess["domain"] == domain:
                for brick in princess["bricks"]:
                    if brick["name"] == brick_name:
                        brick_path = BRICKS_DIR / domain / f"{brick_name}.py"
                        validation = validate_brick(brick_path)

                        if not validation["exists"]:
                            print(f"{C['red']}Error: Brick file not found at {brick_path}{C['reset']}")
                            return

                        if not validation["valid"]:
                            print(f"{C['yellow']}Warning: Brick has validation errors:{C['reset']}")
                            for err in validation["errors"]:
                                print(f"  - {err}")
                            print(f"\nMarking as complete anyway...")

                        brick["status"] = "completed"
                        brick["lines"] = validation["lines"]
                        found = True
                        break

    if not found:
        print(f"{C['red']}Error: Brick '{args.brick_path}' not found{C['reset']}")
        return

    # Update summary
    total_completed = sum(
        1 for w in plan["waves"] for p in w["princesses"] for b in p["bricks"]
        if b["status"] == "completed"
    )
    plan["summary"]["completed"] = total_completed
    plan["summary"]["progress_percent"] = round(total_completed / plan["summary"]["total_bricks"] * 100, 1)

    save_plan(plan)

    if args.json:
        print(json.dumps({"success": True, "brick": args.brick_path, "lines": validation["lines"]}))
    else:
        print(f"{C['green']}Marked {args.brick_path} as complete ({validation['lines']} lines){C['reset']}")
        print(f"Progress: {plan['summary']['completed']}/{plan['summary']['total_bricks']} ({plan['summary']['progress_percent']}%)")


def cmd_assign(args: argparse.Namespace, plan: dict) -> None:
    """Assign a Princess domain to a Claude window."""
    domain_id = args.domain_id.upper()

    for wave in plan["waves"]:
        for p in wave["princesses"]:
            if p["id"] == domain_id or p["domain"].lower() == args.domain_id.lower():
                p["assigned_to"] = args.window_name
                p["status"] = "assigned"
                save_plan(plan)

                if args.json:
                    print(json.dumps({"success": True, "domain": p["domain"], "assigned_to": args.window_name}))
                else:
                    print(f"{C['green']}Assigned {p['id']} ({p['domain']}) to {args.window_name}{C['reset']}")
                return

    print(f"{C['red']}Error: Domain '{args.domain_id}' not found{C['reset']}")


# ============== Autonomous Mode Commands ==============

AUTONOMOUS_DIR = Path(__file__).parent / "autonomous"
PID_DIR = AUTONOMOUS_DIR / "progress"

DOMAIN_MAP = {
    "Q-14": "security", "Q-10": "storage", "Q-08": "auth", "Q-07": "audit",
    "Q-01": "documents", "Q-02": "fields", "Q-03": "signing", "Q-04": "workflow",
    "Q-05": "parties", "Q-06": "notifications", "Q-09": "api",
    "Q-12": "templates", "Q-13": "automations"
}

WAVE_DOMAINS = {
    1: ["Q-14", "Q-10", "Q-08", "Q-07"],
    2: ["Q-01", "Q-02", "Q-05"],
    3: ["Q-03", "Q-04", "Q-06"],
    4: ["Q-09", "Q-12", "Q-13"]
}


def get_running_domains() -> list:
    """Get list of currently running domain loops."""
    running = []
    if not PID_DIR.exists():
        return running
    for pid_file in PID_DIR.glob("Q-*.pid"):
        domain_id = pid_file.stem
        try:
            pid = int(pid_file.read_text().strip())
            # Check if process is running
            os.kill(pid, 0)
            running.append({"domain_id": domain_id, "pid": pid})
        except (ProcessLookupError, ValueError):
            # Process not running, clean up stale PID file
            pid_file.unlink(missing_ok=True)
    return running


def cmd_start(args: argparse.Namespace, plan: dict) -> None:
    """Start autonomous build for a domain."""
    import subprocess

    domain_id = args.domain_id.upper()
    if domain_id not in DOMAIN_MAP:
        print(f"{C['red']}Error: Unknown domain '{domain_id}'{C['reset']}")
        return

    domain_name = DOMAIN_MAP[domain_id]
    spec_file = AUTONOMOUS_DIR / "specs" / f"{domain_id}-{domain_name.upper()}.md"

    if not spec_file.exists():
        print(f"{C['red']}Error: Spec file not found: {spec_file}{C['reset']}")
        print(f"Create it first: autonomous/specs/{domain_id}-{domain_name.upper()}.md")
        return

    # Check if already running
    running = get_running_domains()
    for r in running:
        if r["domain_id"] == domain_id:
            print(f"{C['yellow']}{domain_id} is already running (PID: {r['pid']}){C['reset']}")
            return

    # Start the domain loop
    loop_script = AUTONOMOUS_DIR / "domain-loop.sh"
    log_file = AUTONOMOUS_DIR / "progress" / f"{domain_id}.log"

    print(f"{C['cyan']}Starting autonomous build for {domain_id} ({domain_name})...{C['reset']}")

    # Run in background
    with open(log_file, "a") as log:
        proc = subprocess.Popen(
            [str(loop_script), domain_id],
            stdout=log,
            stderr=subprocess.STDOUT,
            cwd=str(Path(__file__).parent),
            start_new_session=True
        )

    # Update plan
    for wave in plan["waves"]:
        for p in wave["princesses"]:
            if p["id"] == domain_id:
                p["status"] = "in_progress"
                p["assigned_to"] = f"autonomous (PID: {proc.pid})"
                save_plan(plan)
                break

    if args.json:
        print(json.dumps({"success": True, "domain_id": domain_id, "pid": proc.pid}))
    else:
        print(f"{C['green']}Started {domain_id} (PID: {proc.pid}){C['reset']}")
        print(f"Logs: {log_file}")


def cmd_stop(args: argparse.Namespace, plan: dict) -> None:
    """Stop a running domain loop."""
    import signal

    domain_id = args.domain_id.upper()
    pid_file = PID_DIR / f"{domain_id}.pid"

    if not pid_file.exists():
        print(f"{C['yellow']}{domain_id} is not running{C['reset']}")
        return

    try:
        pid = int(pid_file.read_text().strip())
        os.kill(pid, signal.SIGTERM)
        pid_file.unlink(missing_ok=True)

        # Update plan
        for wave in plan["waves"]:
            for p in wave["princesses"]:
                if p["id"] == domain_id:
                    p["status"] = "stopped"
                    p["assigned_to"] = None
                    save_plan(plan)
                    break

        if args.json:
            print(json.dumps({"success": True, "domain_id": domain_id, "pid": pid}))
        else:
            print(f"{C['green']}Stopped {domain_id} (PID: {pid}){C['reset']}")

    except ProcessLookupError:
        pid_file.unlink(missing_ok=True)
        print(f"{C['yellow']}{domain_id} was not running (stale PID file removed){C['reset']}")
    except Exception as e:
        print(f"{C['red']}Error stopping {domain_id}: {e}{C['reset']}")


def cmd_start_wave(args: argparse.Namespace, plan: dict) -> None:
    """Start all domains in a wave."""
    wave_num = int(args.wave_num)

    if wave_num not in WAVE_DOMAINS:
        print(f"{C['red']}Error: Invalid wave number. Use 1-4{C['reset']}")
        return

    domains = WAVE_DOMAINS[wave_num]
    started = []
    skipped = []

    for domain_id in domains:
        spec_file = AUTONOMOUS_DIR / "specs" / f"{domain_id}-{DOMAIN_MAP[domain_id].upper()}.md"
        if not spec_file.exists():
            skipped.append(f"{domain_id} (no spec)")
            continue

        # Check if already running
        running = get_running_domains()
        if any(r["domain_id"] == domain_id for r in running):
            skipped.append(f"{domain_id} (already running)")
            continue

        # Create mock args and start
        class MockArgs:
            def __init__(self, did):
                self.domain_id = did
                self.json = args.json

        cmd_start(MockArgs(domain_id), plan)
        started.append(domain_id)

    if args.json:
        print(json.dumps({"wave": wave_num, "started": started, "skipped": skipped}))
    else:
        print(f"\n{C['bold']}Wave {wave_num} Summary:{C['reset']}")
        print(f"  Started: {', '.join(started) if started else 'none'}")
        if skipped:
            print(f"  Skipped: {', '.join(skipped)}")


def cmd_stop_all(args: argparse.Namespace, plan: dict) -> None:
    """Stop all running domain loops."""
    running = get_running_domains()

    if not running:
        print(f"{C['yellow']}No domains are currently running{C['reset']}")
        return

    stopped = []
    for r in running:
        class MockArgs:
            def __init__(self, did):
                self.domain_id = did
                self.json = False

        cmd_stop(MockArgs(r["domain_id"]), plan)
        stopped.append(r["domain_id"])

    if args.json:
        print(json.dumps({"stopped": stopped}))
    else:
        print(f"\n{C['green']}Stopped {len(stopped)} domain(s){C['reset']}")


def cmd_ps(args: argparse.Namespace, plan: dict) -> None:
    """Show running autonomous processes."""
    running = get_running_domains()

    if args.json:
        print(json.dumps({"running": running}))
        return

    if not running:
        print(f"{C['dim']}No autonomous processes running{C['reset']}")
        return

    print(f"\n{C['bold']}Running Autonomous Processes{C['reset']}\n")
    print(f"{'Domain':<10} {'PID':<10} {'Domain Name':<15}")
    print("-" * 40)

    for r in running:
        domain_name = DOMAIN_MAP.get(r["domain_id"], "unknown")
        print(f"{r['domain_id']:<10} {r['pid']:<10} {domain_name:<15}")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Colony Manager - Ant Colony Development Dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  plan                    Show full project plan
  status                  Show colony status dashboard
  roles                   List all Princess roles
  domain <ID>             Show specific domain details
  session <ID>            Generate session prompt for a Princess
  validate                Validate all bricks
  complete <domain/brick> Mark a brick as complete
  assign <ID> <window>    Assign domain to a Claude window

Autonomous Mode:
  start <ID>              Start autonomous build for a domain
  stop <ID>               Stop a running domain loop
  start-wave <N>          Start all domains in wave N (1-4)
  stop-all                Stop all running domain loops
  ps                      Show running autonomous processes

Examples:
  python colony.py plan
  python colony.py status --json
  python colony.py session Q-14
  python colony.py complete security/rate_limiter
  python colony.py start Q-14
  python colony.py start-wave 1
  python colony.py ps
"""
    )

    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("plan", help="Show full project plan")
    subparsers.add_parser("status", help="Show colony status dashboard")
    subparsers.add_parser("roles", help="List all Princess roles")

    domain_parser = subparsers.add_parser("domain", help="Show domain details")
    domain_parser.add_argument("domain_id", help="Domain ID (e.g., Q-14) or name (e.g., security)")

    session_parser = subparsers.add_parser("session", help="Generate session prompt")
    session_parser.add_argument("domain_id", help="Domain ID or name")

    subparsers.add_parser("validate", help="Validate all bricks")

    complete_parser = subparsers.add_parser("complete", help="Mark brick as complete")
    complete_parser.add_argument("brick_path", help="Brick path (e.g., security/rate_limiter)")

    assign_parser = subparsers.add_parser("assign", help="Assign domain to window")
    assign_parser.add_argument("domain_id", help="Domain ID or name")
    assign_parser.add_argument("window_name", help="Claude window identifier")

    # Autonomous mode commands
    start_parser = subparsers.add_parser("start", help="Start autonomous build for domain")
    start_parser.add_argument("domain_id", help="Domain ID (e.g., Q-14)")

    stop_parser = subparsers.add_parser("stop", help="Stop running domain loop")
    stop_parser.add_argument("domain_id", help="Domain ID (e.g., Q-14)")

    start_wave_parser = subparsers.add_parser("start-wave", help="Start all domains in wave")
    start_wave_parser.add_argument("wave_num", help="Wave number (1-4)")

    subparsers.add_parser("stop-all", help="Stop all running domain loops")
    subparsers.add_parser("ps", help="Show running autonomous processes")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    plan = load_plan()

    commands = {
        "plan": cmd_plan,
        "status": cmd_status,
        "roles": cmd_roles,
        "domain": cmd_domain,
        "session": cmd_session,
        "validate": cmd_validate,
        "complete": cmd_complete,
        "assign": cmd_assign,
        "start": cmd_start,
        "stop": cmd_stop,
        "start-wave": cmd_start_wave,
        "stop-all": cmd_stop_all,
        "ps": cmd_ps,
    }

    if args.command in commands:
        commands[args.command](args, plan)


if __name__ == "__main__":
    main()
