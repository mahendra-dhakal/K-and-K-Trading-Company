from django.contrib import admin
from django.utils.html import format_html

from .models import (
    CompanyProfile,
    CoreValue,
    Enquiry,
    FAQ,
    Product,
    ProductCategory,
    ProductImage,
    Project,
    ProjectCategory,
    ProjectImage,
    Service,
    Statistic,
    TeamMember,
    Testimonial,
    TimelineEvent,
)

admin.site.site_header = "K&K Trading Company — Content Manager"
admin.site.site_title = "K&K Admin"
admin.site.index_title = "Website Content Management"


def image_preview(obj, field_name="image", height=60):
    image = getattr(obj, field_name, None)
    if image:
        return format_html('<img src="{}" style="height:{}px;border-radius:6px;" />', image.url, height)
    return "—"


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identity", {"fields": ("company_name", "tagline", "logo", "favicon")}),
        ("Descriptions", {"fields": ("short_description", "about_description", "mission", "vision")}),
        ("Homepage Hero", {"fields": ("hero_headline", "hero_subtext", "hero_image")}),
        ("Call To Action", {"fields": ("cta_headline", "cta_subtext")}),
        (
            "Contact Information",
            {"fields": ("phone", "secondary_phone", "email", "address", "business_hours", "google_maps_embed_url")},
        ),
        ("Social Links", {"fields": ("facebook_url", "instagram_url", "linkedin_url", "twitter_url")}),
    )

    def has_add_permission(self, request):
        return not CompanyProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ("year", "title", "display_order", "is_active")
    list_filter = ("is_active",)
    list_editable = ("display_order", "is_active")
    search_fields = ("year", "title")
    ordering = ("display_order", "year")


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "display_order", "is_active")
    list_filter = ("is_active",)
    list_editable = ("display_order", "is_active")
    search_fields = ("title",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "thumbnail", "is_featured", "is_active", "display_order", "updated_at")
    list_filter = ("is_active", "is_featured")
    list_editable = ("is_featured", "is_active", "display_order")
    search_fields = ("name", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at", "preview")
    fieldsets = (
        (None, {"fields": ("name", "slug", "icon", "image", "preview")}),
        ("Content", {"fields": ("short_description", "full_description", "key_features")}),
        ("Visibility", {"fields": ("is_active", "is_featured", "display_order")}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.display(description="Image")
    def thumbnail(self, obj):
        return image_preview(obj, "image")

    @admin.display(description="Preview")
    def preview(self, obj):
        return image_preview(obj, "image", height=160)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "caption", "display_order", "preview")
    readonly_fields = ("preview",)

    @admin.display(description="Preview")
    def preview(self, obj):
        return image_preview(obj, "image")


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "thumbnail", "category", "is_featured", "is_active", "display_order")
    list_filter = ("is_active", "is_featured", "category")
    list_editable = ("is_featured", "is_active", "display_order")
    search_fields = ("name", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at", "preview")
    inlines = [ProductImageInline]
    fieldsets = (
        (None, {"fields": ("name", "slug", "category", "main_image", "preview")}),
        ("Content", {"fields": ("short_description", "detailed_description", "specifications")}),
        ("Visibility", {"fields": ("is_active", "is_featured", "display_order")}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.display(description="Image")
    def thumbnail(self, obj):
        return image_preview(obj, "main_image")

    @admin.display(description="Preview")
    def preview(self, obj):
        return image_preview(obj, "main_image", height=160)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("image", "caption", "display_order", "preview")
    readonly_fields = ("preview",)

    @admin.display(description="Preview")
    def preview(self, obj):
        return image_preview(obj, "image")


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "thumbnail",
        "category",
        "location",
        "completion_date",
        "is_featured",
        "is_published",
        "display_order",
    )
    list_filter = ("is_published", "is_featured", "category")
    list_editable = ("is_featured", "is_published", "display_order")
    search_fields = ("title", "location", "description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at", "preview")
    inlines = [ProjectImageInline]
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "main_image", "preview")}),
        ("Details", {"fields": ("location", "completion_date", "description")}),
        ("Visibility", {"fields": ("is_published", "is_featured", "display_order")}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.display(description="Image")
    def thumbnail(self, obj):
        return image_preview(obj, "main_image")

    @admin.display(description="Preview")
    def preview(self, obj):
        return image_preview(obj, "main_image", height=160)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "thumbnail", "position", "display_order", "is_active")
    list_filter = ("is_active",)
    list_editable = ("display_order", "is_active")
    search_fields = ("name", "position")

    @admin.display(description="Photo")
    def thumbnail(self, obj):
        return image_preview(obj, "photo")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("client_name", "client_company", "rating", "is_published", "display_order")
    list_filter = ("is_published", "rating")
    list_editable = ("is_published", "display_order")
    search_fields = ("client_name", "client_company", "testimonial")


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ("number", "label", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    search_fields = ("label",)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "is_published", "display_order")
    list_editable = ("is_published", "display_order")
    search_fields = ("question", "answer")


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "subject", "status", "submitted_at")
    list_filter = ("status", "submitted_at")
    list_editable = ("status",)
    search_fields = ("full_name", "email", "subject", "company")
    date_hierarchy = "submitted_at"
    ordering = ("-submitted_at",)
    readonly_fields = ("full_name", "email", "phone_number", "company", "subject", "message", "submitted_at")
    fieldsets = (
        ("Contact", {"fields": ("full_name", "email", "phone_number", "company")}),
        ("Enquiry", {"fields": ("subject", "message", "submitted_at")}),
        ("Follow-up", {"fields": ("status",)}),
    )

    def has_add_permission(self, request):
        return False
