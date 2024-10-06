import api.model.Category

def select_all():
    return api.model.Category.select_all()

def select(category_id: int):
    return api.model.Category.select(category_id)