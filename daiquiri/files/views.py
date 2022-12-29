import logging
from lunr import lunr
from django.contrib.admin.options import Paginator

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.utils.safestring import mark_safe

from .utils import (
        get_directory,
        get_file_path,
        render_with_layout,
        send_file,
        get_all_cms_content
)

logger = logging.getLogger(__name__)


class FileView(View):

    root = None

    def get(self, request, file_path, **kwargs):
        if self.root:
            logger.debug('root=%s', self.root)
            file_path = self.root.strip('/') + '/' + file_path

        file_path = get_file_path(file_path)
        if file_path is None:
            logger.debug('%s not found', file_path)
            raise Http404

        directory = get_directory(request.user, file_path)
        if directory is None:
            logger.debug('%s if forbidden', file_path)
            if request.user.is_authenticated:
                raise PermissionDenied
            else:
                return redirect_to_login(request.path_info)

        if file_path.endswith('.html') or file_path.endswith('.md') and directory.layout:
            return render_with_layout(request, file_path)
        else:
            return send_file(request, file_path)


class SearchView(View):

    root = None

    def get(self, request, **kwargs):

        docs = get_all_cms_content()
        idx = lunr(ref="url", fields=("body",), documents = docs)
        results = []
        search_string = request.GET.get("q")
        if search_string:
            file_ids = [f["ref"] for f in idx.search(search_string)]
            results = [d for d in docs if d["url"] in file_ids]

        paginator = Paginator(results, 5)
        page_number = request.GET.get('page')
        search_results = paginator.get_page(page_number)

        context = {
                "search_results": search_results,
                "search_string": search_string,
                "num_of_search_results": len(results)
                }

        return render(request, "files/search-results.html", context)

