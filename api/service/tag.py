import api.model.Tag

def select_all():
    return api.model.Tag.select_all()

def select(tag_id: int):
    return api.model.Tag.select(tag_id)

def selectWithSearch(search: str):
    return api.model.Tag.selectWithSearch(search)

def update(params):
    return api.model.Tag.update(params)