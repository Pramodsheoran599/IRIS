import av
import os
from tqdm import tqdm


def extract_frames(video_path):
    frames = []
    video = av.open(video_path)
    for frame in video.decode(0):
        yield frame.to_image()


def anomaly_videos_extraction(part_number):
    path = 'content/Anomaly_Dataset/Anomaly_Videos/' + part_number
    destination = 'content/Dataset/Abnormal'

    folders = os.listdir(path)
    for directory in tqdm( folders , desc = part_number):
        p1 = os.path.join(path, directory)
        d1 = os.path.join(destination, directory)

        if os.path.exists(d1):
            continue
        os.makedirs(d1, exist_ok=True)

        videos = os.listdir(p1)
        for video in tqdm( videos , desc = directory , position = 0):
            vid_path = os.path.join(p1, video)
            r2 = os.path.join(d1, video[:-4])
            os.makedirs(r2, exist_ok=True)

            for index, frame in enumerate((extract_frames(vid_path))):
                frame.save(os.path.join(r2, f"{index}.jpg"))


def normal_videos_extraction():
    path = 'content/Anomaly_Dataset/Anomaly_Videos/Normal-Videos-Part-1'
    destination = 'content/Dataset/Normal'

    videos = (os.listdir(path))
    for video in tqdm(videos):
        p1 = os.path.join(path, video)
        r1 = os.path.join(destination, video[:-4])

        if os.path.exists(r1):
            continue
        os.makedirs(r1, exist_ok=True)

        for k, frame in enumerate((extract_frames(p1))):
            frame.save(os.path.join(r1, f"{k}.jpg"))


anomaly_videos_extraction('Anomaly-Videos-Part-1')
anomaly_videos_extraction('Anomaly-Videos-Part-2')
normal_videos_extraction()
