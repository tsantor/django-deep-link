from urllib.parse import parse_qs


def get_querystring_as_dict(request):
    query_str = request.META.get("QUERY_STRING", None)
    if query_str:
        return parse_qs(query_str)
    return {}
