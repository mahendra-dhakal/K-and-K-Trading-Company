from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class SingletonModel(models.Model):
    """Base class for models that should only ever have one row."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class CompanyProfile(SingletonModel):
    """Global company information, editable from the admin as a singleton."""

    company_name = models.CharField(max_length=150, default="K&K Trading Company")
    tagline = models.CharField(max_length=200, blank=True, help_text="Short slogan shown near the logo/hero.")
    logo = models.ImageField(upload_to="company/", blank=True, null=True)
    favicon = models.ImageField(upload_to="company/", blank=True, null=True)

    short_description = models.TextField(
        blank=True, help_text="1-2 sentences used in hero/footer/meta description."
    )
    about_description = models.TextField(
        blank=True, help_text="Longer company overview used on the About page."
    )

    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)

    phone = models.CharField(max_length=50, blank=True)
    secondary_phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    business_hours = models.CharField(max_length=255, blank=True, default="Sun - Fri: 9:00 AM - 6:00 PM")

    google_maps_embed_url = models.URLField(blank=True, help_text="Google Maps embed URL for the contact page.")

    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    hero_headline = models.CharField(max_length=200, blank=True, default="Building Reliable Business Connections.")
    hero_subtext = models.TextField(
        blank=True,
        default="K&K Trading Company is committed to delivering reliable products, "
        "professional service, and long-term business relationships.",
    )
    hero_image = models.ImageField(upload_to="company/", blank=True, null=True)

    cta_headline = models.CharField(max_length=200, blank=True, default="Let's Build Something Valuable Together.")
    cta_subtext = models.TextField(
        blank=True,
        default="Have a business enquiry or looking for a reliable partner? Get in touch with our team.",
    )

    class Meta:
        verbose_name = "Company Profile"
        verbose_name_plural = "Company Profile"

    def __str__(self):
        return self.company_name


class TimelineEvent(models.Model):
    """Company history / milestones shown on the About page timeline."""

    year = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "year"]

    def __str__(self):
        return f"{self.year} — {self.title}"


class CoreValue(models.Model):
    """Company values displayed with icons on the About/Home pages."""

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(
        max_length=50, blank=True, help_text="Bootstrap Icon class name, e.g. 'bi-shield-check'."
    )
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.title


class Service(models.Model):
    """A business area / service offered by the company."""

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    short_description = models.CharField(max_length=300, blank=True)
    full_description = models.TextField(blank=True)
    key_features = models.TextField(
        blank=True, help_text="One feature per line. Displayed as a bullet list on the detail page."
    )
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Bootstrap Icon class name, e.g. 'bi-truck'.")

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]
        indexes = [models.Index(fields=["is_active", "is_featured"])]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:service_detail", args=[self.slug])

    def features_list(self):
        return [line.strip() for line in self.key_features.splitlines() if line.strip()]


class ProductCategory(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Catalogue-only product entry. No cart / checkout / payments."""

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="products"
    )
    short_description = models.CharField(max_length=300, blank=True)
    detailed_description = models.TextField(blank=True)
    specifications = models.TextField(
        blank=True, help_text="One 'Key: Value' pair per line, e.g. 'Material: Stainless Steel'."
    )
    main_image = models.ImageField(upload_to="products/", blank=True, null=True)

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]
        indexes = [models.Index(fields=["is_active", "is_featured"])]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:product_detail", args=[self.slug])

    def spec_list(self):
        pairs = []
        for line in self.specifications.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                pairs.append((key.strip(), value.strip()))
            elif line.strip():
                pairs.append((line.strip(), ""))
        return pairs


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="products/gallery/")
    caption = models.CharField(max_length=150, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.product.name} image {self.pk}"


class ProjectCategory(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name_plural = "Project Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(
        ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects"
    )
    location = models.CharField(max_length=150, blank=True)
    completion_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    main_image = models.ImageField(upload_to="projects/", blank=True, null=True)

    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-completion_date"]
        indexes = [models.Index(fields=["is_published", "is_featured"])]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:project_detail", args=[self.slug])


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=150, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.project.title} image {self.pk}"


class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    position = models.CharField(max_length=120, blank=True)
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    client_name = models.CharField(max_length=120)
    client_company = models.CharField(max_length=150, blank=True)
    client_position = models.CharField(max_length=120, blank=True)
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    testimonial = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    is_published = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "-id"]

    def __str__(self):
        return f"{self.client_name} — {self.client_company}"


class Statistic(models.Model):
    number = models.CharField(max_length=20, help_text="e.g. '10+', '100+'")
    label = models.CharField(max_length=100, help_text="e.g. 'Years of Experience'")
    description = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Bootstrap Icon class name.")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.number} {self.label}"


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_published = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ["display_order"]

    def __str__(self):
        return self.question


class Enquiry(models.Model):
    STATUS_NEW = "new"
    STATUS_CONTACTED = "contacted"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_RESOLVED = "resolved"
    STATUS_CHOICES = [
        (STATUS_NEW, "New"),
        (STATUS_CONTACTED, "Contacted"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_RESOLVED, "Resolved"),
    ]

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=150, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Enquiries"
        ordering = ["-submitted_at"]
        indexes = [models.Index(fields=["status", "-submitted_at"])]

    def __str__(self):
        return f"{self.full_name} — {self.subject}"
