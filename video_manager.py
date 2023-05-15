from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, concatenate_videoclips


class VideoEditor:

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def create_video_with_audio(self, image_file, audio_file, duration):
        """
        Creates a video by combining an image clip with an audio clip.

        Args:
            image_file (str): Path to the image file.
            audio_file (str): Path to the audio file.
            duration (float): Duration of the video in seconds.

        Raises:
            FileNotFoundError: If the image or audio file is not found.
            ValueError: If the duration is invalid or negative.

        Returns:
            None

        """
        image_clip = ImageClip(image_file, duration=duration)
        audio_clip = AudioFileClip(audio_file)
        audio_clip = audio_clip.set_duration(image_clip.duration)
        video_clip = image_clip.set_audio(audio_clip)
        video_clip.write_videofile(self.output_file, fps=24)
        print("Video created successfully!")

    def convert_video_to_mp3(self):
        """
        Converts a video file to an MP3 audio file.

        Raises:
            FileNotFoundError: If the input video file is not found.
            ValueError: If the output file format is not supported.

        Returns:
            None

        """
        output_file = self.output_file.replace(".mp4", ".mp3")
        video = VideoFileClip(self.input_file)
        audio = video.audio
        audio.write_audiofile(output_file)
        video.close()
        audio.close()
        print("Video converted to MP3 successfully!")

    def trim_video(self, start_time=0, end_time=5):
        """
        Trims a video file to a specific time range.

        Args:
            start_time (int, optional): Start time of the trimmed video in seconds. Defaults to 0.
            end_time (int, optional): End time of the trimmed video in seconds. Defaults to 5.

        Raises:
            FileNotFoundError: If the input video file is not found.

        Returns:
            None

            """
        ffmpeg_extract_subclip(self.input_file, start_time, end_time, targetname=self.output_file)
        print("Video trimmed successfully!")

    def add_audio_to_video(self, audio_file):
        """
        Adds audio to a video file.

        Args:
            audio_file (str): Path to the audio file.

        Raises:
            FileNotFoundError: If the input video or audio file is not found.

        Returns:
            None

        """
        video_clip = VideoFileClip(self.input_file)
        audio_clip = AudioFileClip(audio_file)
        video_duration = video_clip.duration
        audio_duration = audio_clip.duration
        num_repeats = int(audio_duration / video_duration) + 1
        repeated_video_clips = [video_clip] * num_repeats
        repeated_video_clip = concatenate_videoclips(repeated_video_clips)
        repeated_video_clip = repeated_video_clip.subclip(0, audio_duration)
        repeated_video_clip = repeated_video_clip.set_audio(audio_clip)
        repeated_video_clip.write_videofile(self.output_file, codec="libx264", audio_codec="aac")

        print("Audio added to video successfully!")

    def reduce_video_size(self, target_bit_rate):
        """
        Reduces the size of a video file by resizing it to half its original resolution and reducing its bit rate.

        Args:
            target_bit_rate (str): The target bit rate for the output video, in kbps (kilobits per second).

        Returns:
            None

        Raises:
            None
        """
        video_clip = VideoFileClip(self.input_file)
        video_clip = video_clip.resize(width=video_clip.w // 2, height=video_clip.h // 2)
        video_clip.write_videofile(self.output_file, bitrate=target_bit_rate, codec="libx264", audio_codec="aac")
        print("Video compression complete!")


if __name__ == "__main__":
    editor = VideoEditor("input.mp4", "output.mp4")
    editor.create_video_with_audio("image.jpg", "audio.mp3", 10)
    editor.convert_video_to_mp3()
    editor.trim_video(start_time=0, end_time=20)
    editor.add_audio_to_video("audio.mp3")
    editor.reduce_video_size('1000k')
