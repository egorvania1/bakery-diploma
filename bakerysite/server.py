# Source - https://stackoverflow.com/a/38943785
# Posted by aboutaaron, modified by community. See post 'Timeline' for change history
# Retrieved 2026-05-31, License - CC BY-SA 4.0

from waitress import serve
    
from website.wsgi import application
    
if __name__ == '__main__':
    serve(application, port='8000')
