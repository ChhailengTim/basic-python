import os
import math
from moviepy.editor import VideoFileClip, ColorClip, TextClip, CompositeVideoClip

def split_video(input_path,
                output_dir,
                clip_length_sec,
                to_portrait=True,
                overlay_text=None,
                text_position='top',   # 'top' or 'bottom'
                text_font_scale=1.0,
                text_color=(255, 255, 255),
                text_thickness=2,               # unused by moviepy TextClip, kept for API compatibility
                text_bg_color=(0, 0, 0),
                text_bg_alpha=0.6):

    os.makedirs(output_dir, exist_ok=True)

    clip = VideoFileClip(input_path)
    duration = clip.duration
    if duration <= 0 or clip_length_sec <= 0:
        clip.close()
        raise ValueError("Invalid video duration or clip_length_sec")

    fps = clip.fps or 30
    width, height = clip.size

    if to_portrait:
        out_w = width
        out_h = int(round(width * 16.0 / 9.0))
        if out_h < height:
            out_h = height
    else:
        out_w, out_h = width, height

    # make even
    if out_w % 2 == 1:
        out_w += 1
    if out_h % 2 == 1:
        out_h += 1

    num_clips = math.ceil(duration / clip_length_sec)
    print(f"Duration: {duration:.2f}s, fps: {fps}, clips: {num_clips}, out_size: ({out_w},{out_h})")

    for i in range(num_clips):
        start = i * clip_length_sec
        end = min(duration, (i + 1) * clip_length_sec)
        sub = clip.subclip(start, end)

        # background canvas for portrait (keeps original centered)
        if to_portrait:
            bg = ColorClip(size=(out_w, out_h), color=(0, 0, 0)).set_duration(sub.duration)
            sub_resized = sub.set_position(("center", "center"))
            layers = [bg, sub_resized]
        else:
            layers = [sub]

        # overlay text via TextClip + semi-transparent background
        if overlay_text:
            # fontsize scales roughly with width
            fontsize = max(12, int(30 * text_font_scale * (out_w / 720.0)))
            txt = TextClip(overlay_text, fontsize=fontsize, color='rgb({},{},{})'.format(*text_color),
                           method='label')  # method='label' uses Pillow
            txt = txt.set_duration(sub.duration)

            padding = 12
            txt_bg_w = txt.w + padding * 2
            txt_bg_h = txt.h + padding * 2
            txt_bg = ColorClip(size=(txt_bg_w, txt_bg_h), color=text_bg_color).set_duration(sub.duration).set_opacity(text_bg_alpha)

            # compute positions
            x_center = (out_w - txt_bg_w) // 2
            if text_position == 'top':
                y_pos = 10
            else:
                y_pos = out_h - txt_bg_h - 10

            txt_bg = txt_bg.set_position((x_center, y_pos))
            txt = txt.set_position((x_center + padding, y_pos + padding))

            layers.append(txt_bg)
            layers.append(txt)

        final = CompositeVideoClip(layers, size=(out_w, out_h))

        out_path = os.path.join(output_dir, f"clip_{i+1}.mp4")
        # write with audio preserved, using the source fps to avoid speed changes
        final.write_videofile(out_path, codec='libx264', audio_codec='aac', fps=fps, threads=4, verbose=False, logger=None)
        final.close()
        sub.close()
        print("Saved:", out_path)

    clip.close()

# Example usage when run as script
if __name__ == "__main__":
    split_video(
        "long_video.MP4",
        "clips",
        10,
        to_portrait=True,
        overlay_text="Sample caption here",
        text_position='bottom',
        text_font_scale=1.2,
        text_color=(255, 255, 255),
        text_bg_color=(0, 0, 0),
        text_bg_alpha=0.6
    )
