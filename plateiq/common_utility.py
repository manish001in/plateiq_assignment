from __future__ import absolute_import, unicode_literals

def custom_serializer_object(obj):
    # this function basically gets you the dictionary of any object you pass to it, if a model has
    # foreign keys then it gets the unicode value of that foreign key.
    
    obj_data = {}

    if obj:
        for field in obj._meta.fields:
            if len(field.choices) > 0:
                try:
                    obj_data[field.name] = str(dict(field.choices)[getattr(obj, field.name)])
                except Exception as e:
                    obj_data[field.name] = str(getattr(obj, field.name))
            else:
                try:
                    obj_data[field.name] = str(getattr(obj, field.name))
                except UnicodeEncodeError as e:
                    if type(getattr(obj, field.name))==unicode:
                        obj_data[field.name] = getattr(obj, field.name)
                    else:
                        obj_data[field.name] = unicode(getattr(obj, field.name), 'utf-8')    

    return obj_data
