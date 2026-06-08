import subprocess
import os
from pathlib import Path

import ffmpeg


def convert_mkv_to_mp4(input_file, output_file):
    try:
        # Загружаем входной файл
        input_stream = ffmpeg.input(input_file)

        # Конвертируем в MP4
        output_stream = ffmpeg.output(
            input_stream,
            output_file,
            map='0:v',
            vcodec='libx264',  # Кодек видео (H.264)
            acodec='aac',  # Кодек аудио (AAC)
            strict='experimental',
            movflags='faststart'  # Для стриминга (постепенная загрузка)
        )

        # Запускаем конвертацию
        ffmpeg.run(output_stream)
        print(f"Конвертация завершена: {output_file}")

    except ffmpeg.Error as e:
        print(f"Ошибка при конвертации: {e}")


def extract_subtitles(input_file, output_srt, stream_index=0):
    """
    Извлекает субтитры из видеофайла

    :param input_file: Входной видеофайл (MKV, MP4 и др.)
    :param output_srt: Выходной файл субтитров (например 'subtitles.srt')
    :param stream_index: Индекс потока субтитров (по умолчанию 0)
    """
    try:
        (
            ffmpeg
            .input(input_file)
            .output(output_srt, map=f'0:s:{stream_index}', format='srt')
            .run(overwrite_output=True)
        )
        print(f"Субтитры сохранены в {output_srt}")
    except ffmpeg.Error as e:
        print(f"Ошибка: {e}")


def extract_specific_audio(input_file, output_audio, audio_stream_index=0):
    """Извлекает конкретную аудиодорожку по индексу"""
    (
        ffmpeg
        .input(input_file)
        .output(output_audio, map=f'0:a:{audio_stream_index}')
        .run(overwrite_output=True)
    )


def replace_audio_in_mp4(input_mp4, input_audio, output_mp4, audio_codec='aac'):
    """
    Заменяет аудиодорожку в MP4-файле

    :param input_mp4: Исходный видеофайл
    :param input_audio: Новая аудиодорожка (AAC)
    :param output_mp4: Выходной файл
    :param audio_codec: Кодек аудио (по умолчанию 'aac')
    """
    #
    # from ffmpeg import FFmpeg, Progress
    #
    # ffmpeg = (
    #     FFmpeg()
    #     .option("y")
    #     .input(input_mp4)
    #     .input(input_audio)
    #     .output(
    #         output_mp4,
    #         codec="copy",
    #     )
    # )

    video_stream = ffmpeg.input(input_mp4).video
    audio_stream = ffmpeg.input(input_audio).audio
    ffmpeg.concat(video_stream, audio_stream, v=1, a=1).output(output_mp4, acodec='aac', strict='experimental').run(overwrite_output=True)


if __name__ == "__main__":
    base = Path("D:\\kolec\\TOTARO\\re-zero\\")
    # name = "Dekiru Neko wa Kyou mo Yuuutsu.S01E10.1080p.HEVC.H265.10bit.Rus.AniDUB"
    assert base.exists(), "Нету базы"
    for name in [
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 14 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 15 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 16 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 17 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 18 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 19 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 20 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 21 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 22 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 23 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 24 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 25 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 26 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 27 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 28 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 29 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 30 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 31 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 32 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 33 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 34 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 35 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 36 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 37 [BDRip 1080p x265 FLAC]",
        "[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 38 [BDRip 1080p x265 FLAC]",
    ]:
        input_mkv = base.joinpath(f"{name}.mkv")
        output_mp4 = base.joinpath(f"{name}.mp4")

        output_jp_mp4 = base.joinpath(f"res_{name}.mp4")
        # output_srt = base.joinpath("s1.srt")
        output_audio = base.joinpath(f"{name}.mp3")

        extract_specific_audio(str(input_mkv), str(output_audio), 5)
        convert_mkv_to_mp4(str(input_mkv), str(output_mp4))
        replace_audio_in_mp4(str(output_mp4), str(output_audio), str(output_jp_mp4))



    # extract_subtitles(str(input_mkv), str(output_srt), 1)


## Извлечь дорожку. 7:20, смещение: -467.00
# ffmpeg -i "D:\kolec\TOTARO\Tonari no Totoro (1988).mkv" -map 0:a:5 -c:a libmp3lame -q:a 2 "D:\kolec\TOTARO\Tonari no Totoro (1988)_audio.mp3"
# ffmpeg -i "D:\kolec\TOTARO\Tonari no Totoro (1988).mp4" -i "D:\kolec\TOTARO\Tonari no Totoro (1988).mp3" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest "D:\kolec\TOTARO\Tonari.mp4"