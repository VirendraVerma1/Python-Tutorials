import ffmpeg

input_file = "D:\\Wallpaper\\PICS\\Elephanta caves\\New folder\\VID_20221120_160925.mp4"
output_file = "output.mp4"

input_video = ffmpeg.input(input_file)
output_video = input_video.video.filter('scale', '-2:480').output(output_file)
print(output_video)
#output_video.run()


import os
import ffmpeg

def compress_video(video_full_path, size_upper_bound, two_pass=True, filename_suffix='cps_'):
    """
    Compress video file to target size.
    :param video_full_path: full path of the video file
    :param size_upper_bound: upper bound of the compressed video file size in bytes
    :param two_pass: whether to use two-pass encoding
    :param filename_suffix: suffix of the compressed video file name
    :return: full path of the compressed video file
    """
    # Get the original video file name and extension
    video_file_name = os.path.basename(video_full_path)
    video_file_ext = os.path.splitext(video_file_name)[1]

    # Set the compressed video file name and full path
    compressed_video_file_name = filename_suffix + video_file_name
    compressed_video_full_path = os.path.join(os.path.dirname(video_full_path), compressed_video_file_name)

    # Set the ffmpeg command line arguments for compression
    if two_pass:
        ffmpeg_args = [
            '-y',
            '-i', video_full_path,
            '-c:v', 'libx264',
            '-b:v', '1000k',
            '-pass', '1',
            '-f', 'mp4',
            '/dev/null'
        ]
        ffmpeg_args += [
            '-y',
            '-i', video_full_path,
            '-c:v', 'libx264',
            '-b:v', '1000k',
            '-pass', '2',
            '-c:a', 'copy',
            compressed_video_full_path
        ]
    else:
        ffmpeg_args = [
            '-y',
            '-i', video_full_path,
            '-c:v', 'libx264',
            '-b:v', '1000k',
            '-c:a', 'copy',
            compressed_video_full_path
        ]

    # Compress the video file using ffmpeg
    process = ffmpeg.run(ffmpeg_args)

    # Check if the compressed video file size is within the upper bound
    compressed_video_file_size = os.path.getsize(compressed_video_full_path)
    #if compressed_video_file_size > size_upper_bound:
    #    raise ValueError(f'Compressed video file size {compressed_video_file_size} bytes exceeds upper bound {size_upper_bound} bytes.')

    return compressed_video_full_path


compress_video("D:\\Wallpaper\\PICS\\Elephanta caves\\New folder\\VID_20221120_160925.mp4","16:9")