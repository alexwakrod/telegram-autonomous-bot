def paginate(items, page, per_page=5):
    """Simple pagination helper"""
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end], len(items)