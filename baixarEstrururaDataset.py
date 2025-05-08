from roboflow import Roboflow

rf = Roboflow(api_key="ws5mqV3HBfhJI1xGOR9Q")
project = rf.workspace("challenge-vimrr").project("my-first-project-uyrs1")
version = project.version(1)
dataset = version.download("yolov8")
                
#yolo task=detect mode=train model=yolov8n.pt data=My-First-Project-1/data.yaml epochs=40 imgsz=640 device=0
#yolo task=segment mode=train model=yolov8n.pt data="C:/Users/vinig/AREA_DE_TRABALHO/merda_master/cuPreto/My-First-Project-1/data.yaml" epochs=40 imgsz=640 device=0
