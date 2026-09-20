from django.contrib import messages
from django.core.mail import mail_admins, send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import EnquiryForm
from .models import (
    CompanyProfile,
    CoreValue,
    FAQ,
    HomeIntroductionSection,
    Product,
    ProductCategory,
    Project,
    ProjectCategory,
    Service,
    Statistic,
    TeamMember,
    Testimonial,
    TimelineEvent,
)


def home(request):
    company = CompanyProfile.load()
    context = {
        "company": company,
        "services": Service.objects.filter(is_active=True, is_featured=True)[:6],
        "products": Product.objects.filter(is_active=True, is_featured=True).select_related("category")[:6],
        "projects": Project.objects.filter(is_published=True, is_featured=True).select_related("category")[:6],
        "values": CoreValue.objects.filter(is_active=True)[:4],
        "statistics": Statistic.objects.filter(is_active=True),
        "introduction_sections": HomeIntroductionSection.objects.filter(is_active=True),
        "testimonials": Testimonial.objects.filter(is_published=True)[:6],
        "meta_description": company.short_description
        or "K&K Trading Company — reliable products, professional service, long-term partnerships.",
    }
    return render(request, "core/home.html", context)


def about(request):
    company = CompanyProfile.load()
    context = {
        "company": company,
        "timeline": TimelineEvent.objects.filter(is_active=True),
        "values": CoreValue.objects.filter(is_active=True),
        "team": TeamMember.objects.filter(is_active=True),
        "statistics": Statistic.objects.filter(is_active=True),
        "meta_description": f"Learn about {company.company_name} — our story, mission, and the team behind it.",
    }
    return render(request, "core/about.html", context)


def service_list(request):
    services = Service.objects.filter(is_active=True)
    context = {
        "services": services,
        "meta_description": "Explore the business areas and services offered by K&K Trading Company.",
    }
    return render(request, "core/service_list.html", context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    related = Service.objects.filter(is_active=True).exclude(pk=service.pk)[:3]
    context = {
        "service": service,
        "related_services": related,
        "meta_description": service.short_description or service.full_description[:160],
    }
    return render(request, "core/service_detail.html", context)


def product_list(request):
    products = Product.objects.filter(is_active=True).select_related("category")
    categories = ProductCategory.objects.filter(is_active=True)

    category_slug = request.GET.get("category")
    active_category = None
    if category_slug:
        active_category = get_object_or_404(ProductCategory, slug=category_slug, is_active=True)
        products = products.filter(category=active_category)

    context = {
        "products": products,
        "categories": categories,
        "active_category": active_category,
        "meta_description": "Browse the product catalogue of K&K Trading Company.",
    }
    return render(request, "core/product_list.html", context)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category").prefetch_related("gallery_images"),
        slug=slug,
        is_active=True,
    )
    related = (
        Product.objects.filter(is_active=True, category=product.category)
        .exclude(pk=product.pk)[:4]
    )
    context = {
        "product": product,
        "related_products": related,
        "meta_description": product.short_description or product.detailed_description[:160],
    }
    return render(request, "core/product_detail.html", context)


def project_list(request):
    projects = Project.objects.filter(is_published=True).select_related("category")
    categories = ProjectCategory.objects.filter(is_active=True)

    category_slug = request.GET.get("category")
    active_category = None
    if category_slug:
        active_category = get_object_or_404(ProjectCategory, slug=category_slug, is_active=True)
        projects = projects.filter(category=active_category)

    context = {
        "projects": projects,
        "categories": categories,
        "active_category": active_category,
        "meta_description": "See selected projects and business activities delivered by K&K Trading Company.",
    }
    return render(request, "core/project_list.html", context)


def project_detail(request, slug):
    project = get_object_or_404(
        Project.objects.select_related("category").prefetch_related("gallery_images"),
        slug=slug,
        is_published=True,
    )
    context = {
        "project": project,
        "meta_description": project.description[:160] if project.description else "",
    }
    return render(request, "core/project_detail.html", context)


def contact(request):
    company = CompanyProfile.load()
    context = {
        "company": company,
        "form": EnquiryForm(),
        "faqs": FAQ.objects.filter(is_published=True),
        "meta_description": f"Get in touch with {company.company_name}. Send us a business enquiry.",
    }
    return render(request, "core/contact.html", context)


@require_http_methods(["POST"])
def submit_enquiry(request):
    company = CompanyProfile.load()
    form = EnquiryForm(request.POST)

    if form.is_valid():
        enquiry = form.save()

        subject = f"New Business Enquiry: {enquiry.subject}"
        body = (
            f"A new enquiry was submitted on the website.\n\n"
            f"Name: {enquiry.full_name}\n"
            f"Email: {enquiry.email}\n"
            f"Phone: {enquiry.phone_number or '-'}\n"
            f"Company: {enquiry.company or '-'}\n"
            f"Subject: {enquiry.subject}\n\n"
            f"Message:\n{enquiry.message}\n"
        )
        recipient = getattr(settings, "COMPANY_EMAIL", None)
        try:
            if recipient:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient],
                    fail_silently=False,
                )
        except Exception:
            # The enquiry is already safely stored in the database and visible
            # in Django Admin even if the notification email fails to send.
            pass

        messages.success(
            request,
            "Thank you for contacting %s. Your enquiry has been received and our team "
            "will get back to you shortly." % company.company_name,
        )
        return redirect(reverse("core:contact") + "?sent=1")

    context = {
        "company": company,
        "form": form,
        "faqs": FAQ.objects.filter(is_published=True),
        "meta_description": f"Get in touch with {company.company_name}.",
    }
    messages.error(request, "Please correct the errors below and try again.")
    return render(request, "core/contact.html", context)


def custom_404(request, exception=None):
    return render(request, "404.html", status=404)


def custom_500(request):
    return render(request, "500.html", status=500)
