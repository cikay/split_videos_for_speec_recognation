import os
from moviepy import VideoFileClip
from pydub import AudioSegment
from pydub.silence import split_on_silence


def video_to_audio_segments(
    video_path, output_dir, file_prefix, min_silence_len=420, silence_thresh=-40
):
    """
    Extracts audio from an MP4 video, splits it into segments based on silence,
    and saves the segments as WAV files.

    Args:
        video_path (str): Path to the input MP4 video file.
        output_dir (str): Path to the output directory for audio segments.
        min_silence_len (int): Minimum length of silence in milliseconds.
        silence_thresh (int): Silence threshold in dBFS.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio_path = os.path.join(output_dir, "extracted_audio.wav")
        audio.write_audiofile(audio_path)
        video.close()
        audio.close()

        sound = AudioSegment.from_wav(audio_path)
        chunks = split_on_silence(
            sound,
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh,
            keep_silence=250,
        )

        for i, chunk in enumerate(chunks):
            chunk_name = os.path.join(output_dir, f"{file_prefix}_{i}.wav")
            chunk.export(chunk_name, format="wav")
            print(f"Exported {chunk_name}")

    except Exception as e:
        print(f"Error processing {video_path}: {e}")


# Example Usage:
input_audio = "./videos/Zulkuf_Ergun_Soane_u_Niviskariya_Kurdi.mp4"
output_directory = "audio_segments"
file_prefix = "zulkuf_ergun__soane_u_niviskariya_kurdi"
video_to_audio_segments(input_audio, output_directory, file_prefix)
