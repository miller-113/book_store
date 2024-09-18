from datetime import datetime

def site_copyright(_request):
    start_year = 2021
    current_year = datetime.now().year
    return {
        'start_year': start_year,
        'current_year': current_year,
    }