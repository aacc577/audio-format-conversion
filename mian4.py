import os
import subprocess
import tempfile
import mutagen.id3  # 对于 MP3 文件
import mutagen.flac  # 对于 FLAC 文件
import mutagen.easyid3  # 一个更简单的接口，但可能不支持所有标签
# 注意：对于 AAC 文件，你可能需要使用其他库，因为 mutagen.easyid3 不直接支持 AAC。
# 但对于此示例，我们将主要关注 MP3 和 FLAC，并假设 AAC 文件的处理类似。

def convert_audio_files(input_dir, output_dir, target_format, temp_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.wav', '.flac', '.aac', '.m4a', '.ogg')):
            file_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.' + target_format)
            temp_progress_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt', prefix=f"{os.path.splitext(filename)[0]}_progress_", dir=temp_dir)
            progress_file_path = temp_progress_file.name
            temp_progress_file.close()

            # 读取元数据
            metadata = None
            if filename.lower().endswith('.flac'):
                audio = mutagen.flac.Flac(file_path)
                metadata = {
                    'TITLE': audio['TITLE'][0] if 'TITLE' in audio else '',
                    'ARTIST': audio['ARTIST'][0] if 'ARTIST' in audio else '',
                    'ALBUM': audio['ALBUM'][0] if 'ALBUM' in audio else '',
                    # ... 可以添加更多字段
                }
            elif filename.lower().endswith('.mp3'):
                audio = mutagen.id3.ID3(file_path)
                # 注意：mutagen.id3.ID3 返回的是一个标签集合，你可能需要遍历或检查特定的帧
                metadata = {
                    'TITLE': audio.get('TIT2', [b''])[0].decode('utf-8') if 'TIT2' in audio else '',
                    'ARTIST': audio.get('TPE1', [b''])[0].decode('utf-8') if 'TPE1' in audio else '',
                    'ALBUM': audio.get('TALB', [b''])[0].decode('utf-8') if 'TALB' in audio else '',
                    # ... 可以添加更多字段，注意解码和默认值
                }
            # 对于其他格式，你可以添加类似的逻辑

            # 构建 FFmpeg 命令，包含元数据
            metadata_args = []
            if metadata:
                for key, value in metadata.items():
                    metadata_args.append(f'-metadata {key.lower()}="{value}"')

            command = [
                'D:\\ffmpeg\\bin\\ffmpeg.exe',
                '-i', file_path,
                '-progress', progress_file_path,
                '-acodec', 'libmp3lame' if target_format == 'mp3' else 'aac' if target_format == 'aac' else 'copy',
                *metadata_args,  # 添加元数据参数
                output_file_path
            ]

            try:
                subprocess.run(command, check=True)
                print(f"Converted {file_path} to {output_file_path} with metadata")
            except subprocess.CalledProcessError as e:
                print(f"Failed to convert {file_path}: {e}")

# 使用示例（与之前相同）
input_directory = 'i'
output_directory = 'o'
target_format = 'mp3'
temp_directory = 'temp_progress_files'

convert_audio_files(input_directory, output_directory, target_format, temp_directory)