import os
from pathlib import Path
from roboflow import Roboflow

DEST = Path(__file__).resolve().parent.parent / "data" / "datasets" / "my-first-project"

def main():
    DEST.mkdir(parents=True, exist_ok=True)
    rf = Roboflow(api_key=os.getenv("ROBOFLOW_API_KEY", "COLE_SEU_TOKEN"))
    project  = rf.workspace("challenge-vimrr").project("my-first-project-uyrs1")
    version  = project.version(1)
    version.download("yolov8", location=str(DEST))
    print(f"Dataset salvo em {DEST}")

if __name__ == "__main__":
    main()
