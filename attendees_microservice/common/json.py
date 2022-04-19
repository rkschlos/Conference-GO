from json import JSONEncoder
from datetime import datetime
from django.db.models import QuerySet


class QuerySetEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, QuerySet):
            return list(o)
        else:
            return super().default(o)


class DateEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        else:
            return super().default(o)


class ModelEncoder(DateEncoder, QuerySetEncoder, JSONEncoder):
    encoders = {}

    def default(self, o):
        if isinstance(o, self.model):

            #   if the object to decode is the same class as what's in the
            #   model property, then
            d = {}
            if hasattr(o, "get_api_url"):
                d["href"] = o.get_api_url()
            #     * create an empty dictionary that will hold the property names
            #       as keys and the property values as values
            for property in self.properties:
                value = getattr(o, property)
                if property in self.encoders:
                    encoder = self.encoders[property]
                    value = encoder.default(value)
                d[property] = value
            #     * for each name in the properties list
            #         * get the value of that property from the model instance
            #           given just the property name
            #         * put it into the dictionary with that property name as
            #           the key
            d.update(self.get_extra_data(o))
            return d
        #     * return the dictionary
        #   otherwise,
        #       return super().default(o)  # From the documentation
        else:
            return super().default(o)

    def get_extra_data(self, o):
        return {}
