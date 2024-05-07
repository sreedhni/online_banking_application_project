from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    """
    Custom renderer for User related views.

    This renderer provides customized JSON rendering behavior for User related views.
    It checks if the response contains an 'ErrorDetail' and formats the response accordingly.
    """

    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render method to customize JSON response.

        Args:
            data (dict): The data to be rendered.
            accepted_media_type (str): The accepted media type.
            renderer_context (dict): The context for rendering.

        Returns:
            str: JSON formatted response.
        """
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps(data)
        return response
