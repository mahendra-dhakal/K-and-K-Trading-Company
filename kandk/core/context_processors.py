from .models import CompanyProfile


def site_settings(request):
    """Makes the CompanyProfile singleton available to every template as `site`."""
    return {"site": CompanyProfile.load()}
