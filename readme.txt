# home-server

Ensure ffmpeg/libav installed (edit views.py depending on which you use)
TEMP_DIR and FILES_DIR must both be accessible by webserver

DIY config
  - Create instance folder in project dir
  - "config.py"
    - CSRF_SESSION_KEY
    - SECRET_KEY
    - FILES_DIR (for media)
    - TEMP_DIR (for converted files and other misc)
    - MEDIA_URL (for airplay, use a simple webserver of FILES_DIR. DONT FORGET HTTP:// AT START OMG)
