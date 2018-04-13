from datetime import datetime
from matcher import matching
from matcher import face
from matcher import ihcolor
import scene
import utils
import argparse
import gui


def main():

    # Time start
    t0 = datetime.now()

    # Parse user input
    # Matching type => "orb", "ssim", "face" or "histo"
    parser = argparse.ArgumentParser(description='CPW video classifier')
    parser.add_argument("-m", "--matcher", dest='matching_type', type=str, required=True, help='set matching')
    args = parser.parse_args()

    # Check matching type set
    m = ["face", "orb", "ssim", "histo"]
    if not [s for s in m if args.matching_type in s]:
        print("Error: matching type must be: %s" % ('|'.join(m)))
        return

    # Check if whitespace in the user path => error ffmpeg
    project_user_path = "C:\\Users\\Etienne\\Documents\\GitHub\\opencv_video-comparison\\src\\cpw_project\\"
    if utils.check_space_in_string(project_user_path):
        print("Error: whitespace in the user project path.")
        return

    # Paths directories
    scenes_path = project_user_path + "datas\\scenes\\"
    faces_path = project_user_path + "datas\\faces\\"
    videos_path = project_user_path + "datas\\videos\\"

    # Paths files
    ffmpeg_path = project_user_path + "ffmpeg\\bin\\ffmpeg.exe"
    faces_cascade_path = project_user_path + "datas\\detect\\haarcascade_frontalface_alt.xml"
    faces_trainer_path = project_user_path + "datas\\trainer.yml"
    indexer_path = project_user_path + "datas\\index.pickle"
    result_json_match_path = project_user_path + "datas\\result_" + args.matching_type + ".json"
    result_txt_match_path = project_user_path + "datas\\result_" + args.matching_type + ".txt"

    # Scenes extraction
    scene_threshold = 0.4
    # print("[%s] extract_scenes: start" % str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
    scene.extract_scenes(videos_path, scenes_path, ffmpeg_path, scene_threshold)

    # Images matching
    if (args.matching_type == "orb") or (args.matching_type == "ssim"):
        print("[%s] matching %s: start" % (str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")), args.matching_type))
        matching.matching(scenes_path, args.matching_type, result_json_match_path, result_txt_match_path)

    # Faces recognition matching
    if args.matching_type == "face":
        confidence_threshold = 50
        scale_factor = 1.2
        min_neighbors = 5
        print("[%s] faces_recognition: start" % str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
        face.faces_recognition(scenes_path, faces_path, faces_cascade_path, faces_trainer_path, result_json_match_path, result_txt_match_path, confidence_threshold, scale_factor, min_neighbors)

    # Color histogram image matcher
    if args.matching_type == "histo":
        print("[%s] histo_color_matching: start" % str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
        threshold = 0.2
        ihcolor.histo_matcher(scenes_path, indexer_path, result_json_match_path, result_txt_match_path,  threshold)

    # Get time and compare
    t1 = datetime.now()
    print("Duration: %s" % (t1 - t0))


if __name__ == "__main__":
    main()