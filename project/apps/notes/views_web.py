from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# from .helpers import tree_to_list


@login_required
def index(request):
    # root_folders = request.user.folders \
    #                            .filter(parent_id=None) \
    #                            .order_by('title')
    #
    # # Folders and notepads
    # items = []
    # for folder in root_folders:
    #     items += tree_to_list(folder)
    #
    # context = {'items': items}
    # return render(request, 'notes/index_bb.html', context)
    return render(request, 'notes/index_bb.html')
