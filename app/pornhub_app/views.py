from django.http import FileResponse
from django.shortcuts import render
from .forms import PornhubForm
import youtube_dl


def get_info(request):
    if request.method == "GET":
        form = PornhubForm()

        context = {
            "form": form
        }

        return render(request=request, template_name="pornhub_app/index.html", context=context)

    if request.method == "POST":
        form = PornhubForm(request.POST)
        url = request.POST.get("title")

        if url:
            try:
                options = {
                    'simulate': True,
                    'quiet': True
                }
                ydl = youtube_dl.YoutubeDL(options)
                info_dict = ydl.extract_info(url=url)

                p_formats = []
                formats = info_dict.get('formats')

                for format in formats:
                    if format.get('protocol') == 'https':
                        p_formats.append(format.get('format_id'))
                        
                video_data = {
                    "url": url,
                    "title": info_dict.get('title'),
                    "thumbnail": info_dict.get('thumbnail'),
                    "formats": p_formats
                }

                context = {
                    "form": form,
                    "video_data": video_data
                }

                return render(request=request, template_name="pornhub_app/index.html", context=context)

            except Exception as _ex:
                context = {
                    "form": form,
                    "error_message": f"Check the URL {url}"
                }

                return render(request=request, template_name="pornhub_app/index.html", context=context)

def download_video(request):
    if request.method == "POST":
        url = request.POST.get("url")
        select_res = request.POST.get("select_res")

        options = {
            "format": select_res
        }
        
        ydl = youtube_dl.YoutubeDL(options)
        video = ydl.extract_info(url=url)
        file_name = ydl.prepare_filename(video)

        return FileResponse(open(file_name, 'rb'), as_attachment=True, filename=file_name)