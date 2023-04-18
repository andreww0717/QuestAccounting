# add user context to html files
def add_user_context(request):
    return {'user': request.user} 

