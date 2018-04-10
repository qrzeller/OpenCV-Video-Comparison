from datetime import datetime
from matcher import face
import scene

def main():

    project_user_path = "C:\\Users\\Admin\\PycharmProjects\\cpw_project\\"
    scenes_path = project_user_path + "datas\\scenes\\"
    faces_path = project_user_path + "datas\\faces\\"
    frames_path = project_user_path + "datas\\frames\\"
    videos_path = project_user_path + "datas\\videos\\"
    ffmpeg_path = project_user_path + "ffmpeg\\bin\\ffmpeg.exe"
    faces_cascade_path = project_user_path + "datas\\detect\\haarcascade_frontalface_alt.xml"
    faces_trainer_path = project_user_path + "datas\\detect\\trainer.yml"
    indexer_path = project_user_path + "datas\\index.pickle"
    result_json_path = project_user_path + "datas\\result.json"
    db_result_js_path = project_user_path + "datas\\database.js"


    # Time start
    t0 = datetime.now()

    # Struct => {'video_name': ['scene_image;method']}
    dico_match = {}

    ### Scenes extraction
    print("[%s] extract_scenes: start" % str(datetime.now().strftime("%d-%m-%Y %H:%M")))
    scene.extract_scenes(videos_path, scenes_path, ffmpeg_path)

    ### Faces recognition
    # Best value found for face detection
    confidence_threshold = 50
    scale_factor = 1.2
    min_neighbors = 5
    print("[%s] faces_recognition: start" % str(datetime.now().strftime("%d-%m-%Y %H:%M")))
    dico_match = face.faces_recognition(scenes_path, faces_path, faces_cascade_path, faces_trainer_path, confidence_threshold, scale_factor, min_neighbors)


    # Get time and compare
    t1 = datetime.now()
    print("Duration: %s" % (t1 - t0))


if __name__ == "__main__":
    main()