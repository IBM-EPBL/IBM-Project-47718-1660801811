from json import dump, load

def select():
    with open("db.json", "r") as openfile:
        return load(openfile)
    
def modify(data):
    with open("db.json", "w") as outfile:
        dump(data, outfile, indent=4)

def insert(data):
    db = select()
    db.update(data)
    modify(db)

def verify(data):
    db_keys = select().keys()
    if data in db_keys:
        return True
    return False

def check(data):
    key, pwd = data
    db_val = select()[key]
    if pwd == db_val[-1]:
        return True
    return False
