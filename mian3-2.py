import os
import subprocess
import tempfile

def convert_audio_files(input_dir, output_dir, target_format, temp_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # 确保临时目录存在
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.wav', '.flac', '.aac', '.m4a', '.ogg')):
            file_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.' + target_format)
            # 使用指定的临时目录
            temp_progress_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt', prefix=f"{os.path.splitext(filename)[0]}_progress_", dir=temp_dir)
            progress_file_path = temp_progress_file.name
            temp_progress_file.close()  # 关闭文件，以便FFmpeg可以写入它

            command = [
                'D:\\ffmpeg\\bin\\ffmpeg.exe',
                '-i', file_path,
                '-progress', progress_file_path,
                '-map_metadata:g:0',
                '-id3v2_version 3',
                '-acodec', 'libmp3lame' if target_format == 'mp3' else 'aac' if target_format == 'aac' else 'copy',
                output_file_path
            ]

            try:
                subprocess.run(command, check=True)
                print(f"Converted {file_path} to {output_file_path}")
                # 可以选择删除进度文件
                # os.remove(progress_file_path)
            except subprocess.CalledProcessError as e:
                print(f"Failed to convert {file_path}: {e}")
                # 可以选择保留进度文件以供调试
                # 注意：不删除可能会导致大量临时文件积累

# 使用示例
input_directory = 'i'
output_directory = 'o'
target_format = 'mp3'
temp_directory = 'temp_progress_files'  # 指定临时文件保存的位置

convert_audio_files(input_directory, output_directory, target_format, temp_directory)