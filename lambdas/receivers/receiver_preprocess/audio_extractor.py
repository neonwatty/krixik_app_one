from moviepy.editor import VideoFileClip  # type: ignore
from receivers import s3_client


def check_file_size(s3_bucket: str, s3_key: str) -> int:
    file_head = s3_client.head_object(Bucket=s3_bucket, Key=s3_key)
    file_size_mb = file_head["ContentLength"] / (1024**2)
    return file_size_mb


def extract_audio(video_file_path: str, audio_filepath: str) -> None:
    try:
        video = VideoFileClip(video_file_path)
        audio = video.audio
        if audio is not None:
            audio.write_audiofile(audio_filepath, verbose=False, logger=None, codec="libmp3lame")
            audio.close()
            video.close()
    except Exception as e:
        raise ValueError(f"FAILURE: error extracting audio from video {video_file_path}, exception: {e}")