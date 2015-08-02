"""ObjectRocket Python client constants."""
import os

# TODO(TheDodd): move this to config when we have more items to put there.
#: The URL of the ObjectRocket APIv2.
OR_DEFAULT_API_URL = os.getenv('OR_DEFAULT_API_URL', 'https://sjc-api.objectrocket.com/v2/')

#: A time format for use throughout this client.
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
