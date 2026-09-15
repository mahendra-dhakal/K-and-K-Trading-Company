from datetime import date

from django.core.management.base import BaseCommand

from core.models import (
    CompanyProfile,
    CoreValue,
    FAQ,
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


class Command(BaseCommand):
    help = (
        "Populates the database with clearly-marked PLACEHOLDER demo content so the "
        "site looks complete right after setup. Replace everything from Django Admin "
        "before going live — none of these figures are real."
    )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            "Seeding PLACEHOLDER demo data. Replace all of this in Django Admin before launch."
        ))

        company, _ = CompanyProfile.objects.get_or_create(pk=1)
        company.company_name = "K&K Trading Company"
        company.tagline = "Reliable Trade. Trusted Partnerships."
        company.short_description = (
            "[Placeholder] K&K Trading Company is committed to delivering reliable products, "
            "professional service, and long-term business relationships."
        )
        company.about_description = (
            "[Placeholder] K&K Trading Company was founded with a simple goal: to be a dependable "
            "partner for businesses that need consistent quality, honest communication, and "
            "on-time delivery. Replace this paragraph with your company's real story."
        )
        company.mission = "[Placeholder] To deliver reliable products and services that help our partners grow."
        company.vision = "[Placeholder] To be a trusted regional leader in trading and distribution."
        company.phone = "+977 1-000-0000"
        company.email = "info@example.com"
        company.address = "[Placeholder Address], Kathmandu, Nepal"
        company.business_hours = "Sun – Fri: 9:00 AM – 6:00 PM"
        company.hero_headline = "Building Reliable Business Connections."
        company.hero_subtext = (
            "K&K Trading Company is committed to delivering reliable products, professional "
            "service, and long-term business relationships."
        )
        company.cta_headline = "Let's Build Something Valuable Together."
        company.cta_subtext = "Have a business enquiry or looking for a reliable partner? Get in touch with our team."
        company.save()

        # Core values
        values = [
            ("Reliability", "We do what we say, every time.", "bi-shield-check"),
            ("Quality", "We hold our products and partners to a high standard.", "bi-gem"),
            ("Professionalism", "Every interaction reflects our commitment to excellence.", "bi-briefcase"),
            ("Long-Term Partnerships", "We invest in relationships, not just transactions.", "bi-people"),
        ]
        for i, (title, desc, icon) in enumerate(values):
            CoreValue.objects.get_or_create(
                title=title, defaults={"description": desc, "icon": icon, "display_order": i}
            )

        # Timeline
        timeline = [
            ("2020", "Company Founded", "[Placeholder] K&K Trading Company began operations."),
            ("2022", "Business Expansion", "[Placeholder] Expanded into new business sectors."),
            ("2024", "New Market", "[Placeholder] Entered new regional markets."),
            ("2026", "Continued Growth", "[Placeholder] Continuing to grow our partner network."),
        ]
        for i, (year, title, desc) in enumerate(timeline):
            TimelineEvent.objects.get_or_create(
                year=year, title=title, defaults={"description": desc, "display_order": i}
            )

        # Statistics — placeholders, not real figures
        stats = [
            ("10+", "Years of Experience", "bi-calendar3"),
            ("100+", "Clients Served", "bi-people-fill"),
            ("50+", "Projects Completed", "bi-kanban"),
            ("20+", "Business Partners", "bi-briefcase-fill"),
        ]
        for i, (number, label, icon) in enumerate(stats):
            Statistic.objects.get_or_create(
                label=label, defaults={"number": number, "icon": icon, "display_order": i}
            )

        # Services
        services = [
            ("Trading", "bi-arrow-left-right", "General trading of quality goods across sectors."),
            ("Construction Supply", "bi-building", "Supplying materials and equipment for construction projects."),
            ("Distribution", "bi-truck", "Reliable distribution and logistics for partner businesses."),
            ("Consultancy", "bi-lightbulb", "Business and sourcing consultancy for local partners."),
            ("Import & Export", "bi-globe2", "Cross-border trade facilitation and documentation support."),
        ]
        for i, (name, icon, desc) in enumerate(services):
            Service.objects.get_or_create(
                name=name,
                defaults={
                    "short_description": desc,
                    "full_description": f"[Placeholder] {desc} Replace with real service details in Django Admin.",
                    "key_features": "Reliable sourcing\nCompetitive pricing\nDedicated support\nTimely delivery",
                    "icon": icon,
                    "is_featured": i < 4,
                    "display_order": i,
                },
            )

        # Product categories & products
        cat_general, _ = ProductCategory.objects.get_or_create(name="General Goods", defaults={"display_order": 0})
        cat_industrial, _ = ProductCategory.objects.get_or_create(name="Industrial Supplies", defaults={"display_order": 1})

        products = [
            ("Sample Product A", cat_general, "A short placeholder description of Sample Product A."),
            ("Sample Product B", cat_general, "A short placeholder description of Sample Product B."),
            ("Sample Product C", cat_industrial, "A short placeholder description of Sample Product C."),
            ("Sample Product D", cat_industrial, "A short placeholder description of Sample Product D."),
        ]
        for i, (name, category, desc) in enumerate(products):
            Product.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
                    "short_description": desc,
                    "detailed_description": f"[Placeholder] {desc} Replace with real specifications.",
                    "specifications": "Origin: [Placeholder]\nPackaging: [Placeholder]\nMOQ: [Placeholder]",
                    "is_featured": i < 3,
                    "display_order": i,
                },
            )

        # Project categories & projects
        cat_infra, _ = ProjectCategory.objects.get_or_create(name="Infrastructure", defaults={"display_order": 0})
        cat_supply, _ = ProjectCategory.objects.get_or_create(name="Supply Contracts", defaults={"display_order": 1})

        projects = [
            ("Placeholder Project One", cat_infra, "Kathmandu, Nepal", date(2023, 6, 1)),
            ("Placeholder Project Two", cat_supply, "Pokhara, Nepal", date(2024, 3, 15)),
            ("Placeholder Project Three", cat_infra, "Biratnagar, Nepal", date(2025, 1, 10)),
        ]
        for i, (title, category, location, completed) in enumerate(projects):
            Project.objects.get_or_create(
                title=title,
                defaults={
                    "category": category,
                    "location": location,
                    "completion_date": completed,
                    "description": "[Placeholder] Replace with a real project description in Django Admin.",
                    "is_featured": True,
                    "display_order": i,
                },
            )

        # Team members
        team = [
            ("K. Sharma", "Managing Director"),
            ("K. Thapa", "Operations Director"),
            ("A. Gurung", "Business Development Manager"),
        ]
        for i, (name, position) in enumerate(team):
            TeamMember.objects.get_or_create(
                name=name,
                defaults={
                    "position": position,
                    "bio": "[Placeholder bio] Replace with a real profile in Django Admin.",
                    "display_order": i,
                },
            )

        # Testimonials
        testimonials = [
            ("Placeholder Client A", "Sample Company Ltd.", "Purchasing Manager"),
            ("Placeholder Client B", "Sample Enterprises", "Director"),
        ]
        for i, (name, company_name, position) in enumerate(testimonials):
            Testimonial.objects.get_or_create(
                client_name=name,
                defaults={
                    "client_company": company_name,
                    "client_position": position,
                    "testimonial": "[Placeholder testimonial] Replace with a real client quote in Django Admin.",
                    "rating": 5,
                    "display_order": i,
                },
            )

        # FAQ
        faqs = [
            ("What does K&K Trading Company do?", "[Placeholder] Replace with a real answer in Django Admin."),
            ("How can I request a quote?", "[Placeholder] Use the contact form to send us your enquiry."),
        ]
        for i, (q, a) in enumerate(faqs):
            FAQ.objects.get_or_create(question=q, defaults={"answer": a, "display_order": i})

        self.stdout.write(self.style.SUCCESS("Placeholder demo data seeded successfully."))
