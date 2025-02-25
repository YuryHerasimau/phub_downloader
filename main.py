import youtube_dl
import json
import sys


def get_info(url):
    options = {
        'simulate': True, # Do not download the video files
        'quiet': True # Do not print messages to stdout
    }
    ydl = youtube_dl.YoutubeDL(options)
    
    try:
        info_dict = ydl.extract_info(url=url)
        # return info_dict
        # json_video_data = json.dumps(info_dict)
        # return json_video_data

        formats = info_dict.get('formats')
        p_formats = {}
        count = 1

        for format in formats:
            if format.get('protocol') == 'https':
                # p_formats.append(format.get('format_id'))
                p_formats[count] = format.get('format_id')
                count += 1
                
        video_data = {
            "title": info_dict.get('title'),
            "thumbnail": info_dict.get('thumbnail'),
            "formats": p_formats
        }

        return video_data
        
    except Exception as e:
        return f"Check the URL {url}. \nError: {e}"


def download_video(url, format):
    options = {
        "format": format
    }

    try:
        ydl = youtube_dl.YoutubeDL(options)
        ydl.extract_info(url=url)
        return f"[INFO] Video {format} downloaded successfully! Enjoy (.)(.)"
    except Exception as e:
        return f"Check the URL {url}. \nError: {e}"


def main():
    # print(get_info(url="https://www.pornhub.com/view_video.php?viewkey=ph60fd9d9a77c6f"))
    # print(get_info(url="https://rt.pornhub.com/view_video.php?viewkey=6746df53599a7"))
    # print(get_info(url="https://rt.pornhub.com/view_video.php?viewkey=67a0aa78275d5"))

    url = input("Введите URL: ")
    url = url.strip()

    video_data = get_info(url=url)
    title = video_data.get("title")
    available_formats = video_data.get("formats")

    print(f"[INFO] {title}\n{'-' * 50}")
    print("Выберите желаемое качество видео: ")

    for k, v in available_formats.items():
        print(f"{k}. {v}")

    format = int(input("Введите номер желаемого качества: "))

    if format not in available_formats:
        print("[ERROR] Выбран неверный формат!")
        sys.exit()

    print(download_video(url=url, format=available_formats[format]))

if __name__ == "__main__":
    main()