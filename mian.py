import os
import subprocess


def convert_audio_files(input_dir, output_dir, target_format):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_dir):
        # 获取文件的完整路径
        file_path = os.path.join(input_dir, filename)

        # 检查文件是否是音频文件（这里简单通过文件扩展名判断）
        if filename.lower().endswith(('.wav', '.flac', '.aac', '.m4a', '.ogg')):
            # 构造输出文件的路径和名称
            # 这里我们保留原文件名，只改变扩展名
            output_file_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.' + target_format)

            # 调用FFmpeg进行转换
            # 注意：这里使用了-q:a参数来控制输出音频的质量（对于MP3等编码有效）
            # -q:a 2表示高质量，数值越大质量越低，文件越小
            # 如果你不需要控制质量，可以省略这个参数
            command = [
                'ffmpeg',
                '-i', file_path,  # 输入文件
                # '-q:a', '2',  # 音频质量（可选）
                '-progress progress.txt', #进度文件
                '-acodec', 'libmp3lame' if target_format == 'mp3' else 'copy',  # 音频编码器，如果目标格式与源格式相同则使用copy
                output_file_path  # 输出文件
            ]

            # 如果目标格式不是MP3，可能需要调整编码器参数
            # 例如，对于AAC可以使用'-acodec aac -strict experimental'
            # 注意：这里的'copy'编码器仅当源和目标格式兼容时才有效

            # 执行FFmpeg命令
            subprocess.run(command, check=True)
            print(f"Converted {file_path} to {output_file_path}")


# 使用示例
input_directory = 'i'
output_directory = 'o'
target_format = 'mp3'

convert_audio_files(input_directory, output_directory, target_format)