# import ffmpeg

# def convert_480p(video_path):
#     output_path = video_path.replace('.mp4', '_480p.mp4')
#     ffmpeg.input(video_path).output(output_path, vf='scale=1280:720').run()
#     return output_path

# def convert_720p(video_path):
#     output_path = video_path.replace('.mp4', '_720p.mp4')
#     ffmpeg.input(video_path).output(output_path, vf='scale=1920:1080').run()
#     return output_path