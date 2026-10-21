"""
SupplyCompare - Enterprise Quotation Comparison & Purchasing Platform
Main Entry Point
"""
import os
import sys
import subprocess

def main():
    print("================================================================")
    print("SupplyCompare Enterprise Supply Chain Platform")
    print("================================================================")
    print("Usage: python main.py [runserver|test|migrate|seed|help]")

    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")

    if cmd == "runserver":
        port = sys.argv[2] if len(sys.argv) > 2 else "8000"
        print(f"Starting Django backend on port {port}...")
        subprocess.run([sys.executable, "manage.py", "runserver", port], cwd=backend_dir)
    elif cmd == "test":
        print("Running comprehensive test suite...")
        subprocess.run([sys.executable, "manage.py", "test", "tests"], cwd=backend_dir)
    elif cmd == "migrate":
        print("Executing database schema migrations...")
        subprocess.run([sys.executable, "manage.py", "migrate"], cwd=backend_dir)
    elif cmd == "seed":
        print("Seeding kirana dataset...")
        subprocess.run([sys.executable, os.path.join("scripts", "seed_data.py")], cwd=backend_dir)
    else:
        print("Platform is ready. Run 'python main.py runserver' to start backend.")

if __name__ == "__main__":
    main()
