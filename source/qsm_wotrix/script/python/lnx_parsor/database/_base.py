# coding:utf-8


def generate_entity_type_models(model_class, database_):
    class Meta:
        database = database_

    attrs = {
        '__module__': model_class.__module__,
        'Meta': Meta,
    }

    return type(model_class.__name__, (model_class,), attrs)


def build_entity_types(models, database_):
    for i_model in models:
        # fixme: create table method sort models?
        database_.create_tables([i_model])


class Status(object):
    pass
