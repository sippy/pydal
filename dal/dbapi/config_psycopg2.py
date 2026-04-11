from psycopg2.extras import DictCursor

# special quote/escape chracters (if any)
escape_chars = ['\\']
cursor_params_dict = {'cursor_factory':DictCursor}

def convert_desc(desc):
    ret = []
    for col in desc:
        ret.append(col.name)
    return ret
