import json

from rest_framework.renderers import JSONRenderer


class ZidshipJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    pagination_object_label = 'results'

    def render(self, data, media_type=None, renderer_context=None):
        if data.get('results', None) is not None:
            data[self.pagination_object_label] = data.pop('results')
            return json.dumps(data)

        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        elif data.get('errors', None) is not None:
            return super(ZidshipJSONRenderer, self).render(data)

        else:
            return json.dumps(data)
