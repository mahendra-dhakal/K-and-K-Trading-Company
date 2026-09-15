import time

from django.core.cache import cache
from django.shortcuts import render

ENQUIRY_PATH = "/enquiry/"
RATE_LIMIT_SECONDS = 30
RATE_LIMIT_MAX_ATTEMPTS = 5
RATE_LIMIT_WINDOW = 600  # 10 minutes


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


class EnquiryRateLimitMiddleware:
    """Lightweight, dependency-free rate limiting for the enquiry endpoint.

    Prevents a single client from flooding the enquiry form: at most
    RATE_LIMIT_MAX_ATTEMPTS submissions per RATE_LIMIT_WINDOW seconds, with a
    short cooldown between consecutive submissions.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and request.path.rstrip("/") + "/" == ENQUIRY_PATH:
            ip = _client_ip(request)
            cooldown_key = f"enquiry_cooldown_{ip}"
            count_key = f"enquiry_count_{ip}"

            if cache.get(cooldown_key):
                return render(
                    request,
                    "core/enquiry_throttled.html",
                    {"message": "Please wait a moment before submitting another enquiry."},
                    status=429,
                )

            attempts = cache.get(count_key, 0)
            if attempts >= RATE_LIMIT_MAX_ATTEMPTS:
                return render(
                    request,
                    "core/enquiry_throttled.html",
                    {"message": "Too many enquiries submitted recently. Please try again later."},
                    status=429,
                )

            cache.set(cooldown_key, True, RATE_LIMIT_SECONDS)
            cache.set(count_key, attempts + 1, RATE_LIMIT_WINDOW)

        return self.get_response(request)
