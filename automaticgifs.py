import whisper
import re
import subprocess
def transcribe_video(video_path):
    model = whisper.load_model("base")
    result = model.transcribe(video_path)
    print("Transcription completed.")
    return result['text']
def segment_transcription(transcription, max_length=10):
    sentences = re.split(r'(?<=[.!?]) +', transcription)
    segments = []
    current_segment = ""
    for sentence in sentences:
        if len(current_segment.split()) + len(sentence.split()) <= max_length:
            current_segment += " " + sentence
        else:
            segments.append(current_segment.strip())
            current_segment = sentence
    if current_segment:
        segments.append(current_segment.strip())
    print("Segmentation completed.")
    return segments
def create_gif(input_video, start_time, duration, output_gif):
    command = [
        'ffmpeg',
        '-ss', str(start_time),
        '-t', str(duration),
        '-i', input_video,
        '-vf', "fps=10,scale=320:-1:flags=lanczos",
        '-gifflags', '+transdiff',
        '-y', output_gif
    ]
    subprocess.run(command, check=True)
    print(f"GIF created: {output_gif}")
def generate_gifs(video_path, segments, segment_durations):
    gifs = []
    for i, (segment, duration) in enumerate(zip(segments, segment_durations)):
        start_time = i * duration  # assuming each segment starts right after the previous one
        output_gif = f"output_{i}.gif"
        create_gif(video_path, start_time, duration, output_gif)
        gifs.append(output_gif)
    return gifs
def add_caption_to_gif(gif_path, caption, output_gif):
    command = [
        'ffmpeg',
        '-i', gif_path,
        '-vf', f"drawtext=text='{caption}':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=h-line_h-10",
        '-y', output_gif
    ]
    subprocess.run(command, check=True)
    print(f"Caption added to GIF: {output_gif}")
def create_gifs_from_video(video_path, max_length, duration_per_segment):
    transcription = transcribe_video(video_path)
    print("Transcription:", transcription)
    segments = segment_transcription(transcription, max_length)
    print("Segments:", segments)
    gifs = generate_gifs(video_path, segments, [duration_per_segment] * len(segments))
    for i, (gif, caption) in enumerate(zip(gifs, segments)):
        output_gif = f"captioned_{i}.gif"
        add_caption_to_gif(gif, caption, output_gif)
video_path = 'CAGV.mp4'
create_gifs_from_video(video_path, max_length=10, duration_per_segment=5)