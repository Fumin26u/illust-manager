import api.model.Tag

def select_all(isFetchTagWords = True):
    tags = api.model.Tag.select_all()
    if not isFetchTagWords:
        return tags
    
    for tag in tags:
        tag['words'] = api.model.Tag.selectTagWords(tag['id'])

    return tags

def select(tag_id: int, isFetchTagWords = True):
    tag = api.model.Tag.select(tag_id)
    if not isFetchTagWords:
        return tag
    
    tag['words'] = api.model.Tag.selectTagWords(tag['id'])
    return tag

def selectWithSearch(search: str, isFetchTagWords = True):
    tags = api.model.Tag.selectWithSearch(search)
    if not isFetchTagWords:
        return tags
    
    for tag in tags:
        tag['words'] = api.model.Tag.selectTagWords(tag['id'])
        print(tag['words'])
    return tags

def update(params):
    return api.model.Tag.update(params)