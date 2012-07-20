import local_settings

ENV= getattr(local_settings, 'ENV', 'develop')
PORT = getattr(local_settings, 'PORT', 8080)
