#!/usr/bin/env python3
"""
Complete Static Site Generator for Child Injury Claims
Single file containing all code - templates, content, and build logic
"""

import os
import shutil
import csv
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, Template
import markdown

# ============================================================================
# CONFIGURATION
# ============================================================================

SITE_CONFIG = {
    "site_name": "Child Injury Claims UK",
    "site_url": "https://childinjuryclaims.co.uk",
    "phone": "0800 123 4567",
    "email": "info@childinjuryclaims.co.uk",
    "build_date": datetime.now().strftime('%Y-%m-%d')
}

# ============================================================================
# LOCATION DATA (UK Counties and Towns)
# ============================================================================

LOCATIONS = [
    # County, Town, Postcode
    ("Greater London", "Woolwich", "SE18"),
    ("Greater London", "Greenwich", "SE10"),
    ("Greater London", "Lewisham", "SE13"),
    ("Greater London", "Croydon", "CR0"),
    ("Greater London", "Bromley", "BR1"),
    ("Greater London", "Richmond", "TW9"),
    ("Greater London", "Kingston", "KT1"),
    ("Greater London", "Sutton", "SM1"),
    ("Greater London", "Harrow", "HA1"),
    ("Greater London", "Ealing", "W5"),
    ("Greater Manchester", "Manchester City Centre", "M1"),
    ("Greater Manchester", "Salford", "M3"),
    ("Greater Manchester", "Bolton", "BL1"),
    ("Greater Manchester", "Wigan", "WN1"),
    ("Greater Manchester", "Rochdale", "OL11"),
    ("West Midlands", "Birmingham City Centre", "B1"),
    ("West Midlands", "Coventry", "CV1"),
    ("West Midlands", "Wolverhampton", "WV1"),
    ("West Midlands", "Dudley", "DY1"),
    ("West Midlands", "Walsall", "WS1"),
    ("West Yorkshire", "Leeds City Centre", "LS1"),
    ("West Yorkshire", "Bradford", "BD1"),
    ("West Yorkshire", "Wakefield", "WF1"),
    ("West Yorkshire", "Huddersfield", "HD1"),
    ("Merseyside", "Liverpool City Centre", "L1"),
    ("Merseyside", "Birkenhead", "CH41"),
    ("Merseyside", "Southport", "PR8"),
    ("Tyne and Wear", "Newcastle upon Tyne", "NE1"),
    ("Tyne and Wear", "Gateshead", "NE8"),
    ("Tyne and Wear", "Sunderland", "SR1"),
    ("South Yorkshire", "Sheffield City Centre", "S1"),
    ("South Yorkshire", "Rotherham", "S60"),
    ("South Yorkshire", "Doncaster", "DN1"),
    ("Kent", "Maidstone", "ME14"),
    ("Kent", "Canterbury", "CT1"),
    ("Kent", "Tunbridge Wells", "TN1"),
    ("Essex", "Chelmsford", "CM1"),
    ("Essex", "Colchester", "CO1"),
    ("Essex", "Southend-on-Sea", "SS1"),
    ("Surrey", "Guildford", "GU1"),
    ("Surrey", "Woking", "GU21"),
    ("Surrey", "Epsom", "KT17"),
    ("Hampshire", "Southampton", "SO14"),
    ("Hampshire", "Portsmouth", "PO1"),
    ("Hampshire", "Winchester", "SO23"),
    ("Sussex", "Brighton", "BN1"),
    ("Sussex", "Worthing", "BN11"),
    ("Sussex", "Eastbourne", "BN21"),
]

# ============================================================================
# HOMEPAGE CONTENT (Markdown)
# ============================================================================

HOMEPAGE_MD = """## Expert Child Injury Compensation Claims

When a child suffers an injury due to someone else's negligence, it can be a devastating experience for the whole family. Our specialist solicitors are here to help you get the compensation your child deserves, allowing you to focus on their recovery without financial worry.

### Why Choose Our Child Injury Solicitors?

- **Specialist Expertise**: We focus exclusively on child injury claims, understanding the unique challenges and legal considerations involved.
- **Nationwide Coverage**: With solicitors across the UK, we provide local expertise wherever you are.
- **No Win No Fee**: You don't pay unless your claim succeeds, giving you peace of mind.
- **Child-Centred Approach**: We prioritise your child's wellbeing throughout the claims process.

### Who Can Make A Child Injury Compensation Claim?

Parents or legal guardians can make a claim on behalf of a child who has suffered an injury due to someone else's negligence. This includes injuries occurring:

- At school or nursery
- In public places (playgrounds, parks, shops)
- Due to medical negligence during birth or treatment
- In road traffic accidents
- Due to defective products

### How Much Compensation Can I Claim For A Child Injury?

Compensation amounts vary depending on the severity and long-term impact of the injury:

- **Minor injuries** (cuts, bruises, short-term effects): £1,000 - £5,000
- **Moderate injuries** (fractures, emotional trauma): £5,000 - £20,000
- **Serious injuries** (permanent disability, brain injury): £20,000 - £100,000+
- **Severe, life-changing injuries**: £100,000 - several million pounds

Compensation covers both the pain and suffering caused and any financial losses, including medical expenses, care costs, and loss of future earnings if the injury affects the child's career prospects.

### What Are The Most Common Causes Of Child Injury Claims?

Our experience shows that child injury claims typically arise from:

1. **School Accidents**: Slips, trips, falls in playgrounds, inadequate supervision
2. **Medical Negligence**: Birth injuries, misdiagnosis, delayed treatment
3. **Road Traffic Accidents**: Child pedestrians or passengers injured
4. **Public Place Accidents**: Unsafe playground equipment, pavement trip hazards
5. **Product Defects**: Faulty toys, car seats, or other children's products

### How Do I Start A Child Injury Claim?

Starting a claim is straightforward:

1. **Contact us** for a free, no-obligation consultation
2. **We assess your case** and advise if you have a valid claim
3. **No Win No Fee agreement** – you're protected financially
4. **We gather evidence** (medical records, witness statements, expert opinions)
5. **We negotiate with insurers** to secure the best settlement
6. **Your child receives compensation** – we handle everything

### How Long Do I Have To Make A Child Injury Claim?

For children, special time limits apply:

- The standard 3-year time limit doesn't start until the child's 18th birthday
- A parent or guardian can claim on their behalf at any time before then
- After age 18, the young person has 3 years to claim themselves
- For serious injuries where the child lacks mental capacity, no time limit applies

However, it's always best to start the process as soon as possible while evidence is fresh.

### Evidence Required for a Child Injury Claim

To build a strong case, we'll help you gather:

- Medical records and reports
- Photographs of the injury and accident scene
- Witness statements
- Accident reports (school, nursery, workplace)
- Receipts for expenses incurred
- School or nursery records

### How Long Does A Claim Take To Settle?

Timelines vary depending on complexity:

- **Simple claims**: 4-9 months
- **Moderate claims requiring investigation**: 9-18 months
- **Complex claims (severe injuries)**: 18 months - 3 years

We keep you informed throughout and work to conclude your claim as efficiently as possible while ensuring the best outcome.

### Claims Involving Uninsured or Unknown Parties

If the responsible party is uninsured or can't be identified (like a hit-and-run driver), you may still be able to claim through the Motor Insurers' Bureau (MIB) or Criminal Injuries Compensation Authority. Our solicitors can advise on these specialist claims.
"""

# ============================================================================
# LOCATION PAGE TEMPLATE (Markdown)
# ============================================================================

LOCATION_TEMPLATE_MD = """## Child Injury Claims in [LOCATION]

If your child has suffered an injury in [LOCATION] due to someone else's negligence, our specialist solicitors can help you claim the compensation they deserve. We understand the unique challenges of child injury claims and provide a compassionate, expert service tailored to your family's needs.

### Who Can Make A Child Injury Compensation Claim in [LOCATION]?

Parents and legal guardians in [LOCATION] can make a claim on behalf of a child who has been injured through no fault of their own. This includes accidents at local schools, nurseries, playgrounds, or in public places throughout [LOCATION]. Our solicitors have extensive experience helping families in the [POSTCODE] area and across [COUNTY].

### How Much Compensation Can I Claim For A Child Injury in [LOCATION]?

Compensation for child injuries in [LOCATION] depends on the severity and long-term impact:

- **Minor injuries** (short-term effects): £1,000 - £5,000
- **Moderate injuries** (requiring ongoing treatment): £5,000 - £20,000
- **Serious injuries** (permanent disability): £20,000 - £100,000+
- **Severe, life-changing injuries**: £100,000 - several million

We'll help you claim for pain, suffering, medical expenses, care costs, and any impact on future earnings.

### Common Causes of Child Injuries in [LOCATION]

Families in [LOCATION] often approach us about injuries caused by:

- School accidents due to inadequate supervision
- Playground accidents on unsafe equipment
- Medical negligence at local hospitals or GP practices
- Road traffic accidents involving child pedestrians or passengers
- Slips and trips on poorly maintained pavements

### How Do I Start a Child Injury Claim in [LOCATION]?

Starting your claim in [LOCATION] is simple:

1. Contact us for a free, no-obligation consultation
2. We'll assess your case and explain your options
3. If you proceed, we'll handle everything on a No Win No Fee basis
4. We'll gather evidence from [LOCATION]-based medical experts if needed
5. We'll negotiate with insurers to secure your child's compensation

### Local Expertise in [LOCATION]

Our solicitors understand the local landscape in [COUNTY] and have experience dealing with cases involving:

- Local schools and educational facilities
- [COUNTY] council-maintained public areas
- NHS trusts and hospitals serving [LOCATION]
- Local businesses and service providers

### Free Claim Assessment in [LOCATION]

Don't wait to seek the compensation your child deserves. Contact our [LOCATION] team today for a free, confidential discussion about your child's injury. There's no obligation, and we'll advise you clearly on whether you have a valid claim.
"""

# ============================================================================
# HTML TEMPLATES (Jinja2)
# ============================================================================

BASE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ site_name }}{% endblock %}</title>
    <meta name="description" content="{% block description %}Expert child injury compensation claims solicitors. No Win No Fee. Free consultation.{% endblock %}">
    <style>
        {{ css_content|safe }}
    </style>
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "LegalService",
        "name": "{{ site_name }}",
        "url": "{{ site_url }}",
        "description": "Specialist solicitors for child injury compensation claims",
        "areaServed": "United Kingdom",
        "priceRange": "££",
        "openingHours": "Mo-Fr 09:00-18:00"
    }
    </script>
</head>
<body>
    <header class="site-header">
        <div class="container">
            <div class="header-content">
                <a href="/" class="logo">
                    <h1>{{ site_name }}</h1>
                </a>
                <nav class="main-nav">
                    <button class="mobile-menu-toggle" aria-label="Menu">☰</button>
                    <ul class="nav-menu">
                        <li><a href="/">Home</a></li>
                        <li><a href="/#areas-covered">Areas We Cover</a></li>
                        <li><a href="/#faq">FAQ</a></li>
                        <li><a href="/#contact" class="cta-button">Free Consultation</a></li>
                    </ul>
                </nav>
            </div>
        </div>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-about">
                    <h3>{{ site_name }}</h3>
                    <p>Specialist solicitors helping families get the compensation they deserve.</p>
                    <p class="trust-badge">✓ No Win No Fee</p>
                    <p class="trust-badge">✓ Free Initial Consultation</p>
                    <p class="trust-badge">✓ Specialist Child Injury Solicitors</p>
                </div>
                <div class="footer-links">
                    <h4>Quick Links</h4>
                    <ul>
                        <li><a href="/">Home</a></li>
                        <li><a href="/#areas-covered">Areas We Cover</a></li>
                        <li><a href="/#faq">Frequently Asked Questions</a></li>
                        <li><a href="/#contact">Contact Us</a></li>
                        <li><a href="/sitemap.xml">Sitemap</a></li>
                    </ul>
                </div>
                <div class="footer-contact">
                    <h4>Contact Us</h4>
                    <p>📞 Call us: <a href="tel:{{ phone }}">{{ phone }}</a></p>
                    <p>📧 Email: <a href="mailto:{{ email }}">{{ email }}</a></p>
                    <p>⏰ Mon-Fri: 9am - 6pm</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 {{ site_name }}. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        {{ js_content|safe }}
    </script>
    
    {% block faq_schema %}{% endblock %}
</body>
</html>
"""

INDEX_TEMPLATE = """{% extends "base.html" %}
{% block title %}{{ site_name }} | No Win No Fee Solicitors{% endblock %}
{% block content %}
<div class="hero">
    <div class="container">
        <h1>Expert Child Injury Compensation Claims</h1>
        <p class="hero-subtitle">Specialist solicitors helping families across the UK get the justice they deserve</p>
        <div class="hero-cta">
            <a href="/#contact" class="button button-large">Free Claim Assessment</a>
            <p class="small-text">No win no fee • Free consultation • 100% confidential</p>
        </div>
    </div>
</div>

<div class="container">
    <div class="content-section">
        {{ homepage_content|safe }}
    </div>

    <section id="areas-covered" class="areas-covered">
        <h2>Areas We Cover</h2>
        <p>We help families throughout England and Wales with child injury claims. Select your area below:</p>
        
        <div class="county-grid">
            {% for county, towns in locations_by_county.items() %}
            <div class="county-card">
                <h3><a href="/near-me/{{ county.lower().replace(' ', '-') }}/">{{ county }}</a></h3>
                <ul class="town-list">
                    {% for town in towns[:5] %}
                    <li><a href="/near-me/{{ county.lower().replace(' ', '-') }}-{{ town.town.lower().replace(' ', '-') }}/">{{ town.town }}</a></li>
                    {% endfor %}
                    {% if towns|length > 5 %}
                    <li><a href="/near-me/{{ county.lower().replace(' ', '-') }}/">View all {{ towns|length }} locations →</a></li>
                    {% endif %}
                </ul>
            </div>
            {% endfor %}
        </div>
    </section>

    <section id="faq" class="faq-section">
        <h2>Frequently Asked Questions</h2>
        <div class="faq-grid">
            <div class="faq-item">
                <h3>Who can make a child injury claim?</h3>
                <p>Parents or legal guardians can make a claim on behalf of a child who has suffered an injury due to someone else's negligence.</p>
            </div>
            <div class="faq-item">
                <h3>How much compensation can I claim?</h3>
                <p>Compensation amounts vary based on the severity of the injury. Minor injuries might attract £1,000-£5,000, while severe injuries can result in six-figure settlements.</p>
            </div>
            <div class="faq-item">
                <h3>How long do I have to make a claim?</h3>
                <p>For children, a claim can be made up to three years from the child's 18th birthday. It's best to start as soon as possible.</p>
            </div>
            <div class="faq-item">
                <h3>What does "No Win No Fee" mean?</h3>
                <p>You won't pay any legal fees if your claim is unsuccessful. If you win, fees are taken as a percentage of the compensation.</p>
            </div>
        </div>
    </section>

    <section id="contact" class="contact-section">
        <h2>Get Your Free Claim Assessment</h2>
        <div class="contact-grid">
            <div class="contact-form">
                <form name="claim-assessment" method="POST" data-netlify="true">
                    <input type="hidden" name="form-name" value="claim-assessment">
                    
                    <div class="form-group">
                        <label for="name">Your Name *</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="phone">Phone Number *</label>
                        <input type="tel" id="phone" name="phone" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="location">Your Location</label>
                        <input type="text" id="location" name="location" placeholder="e.g., Manchester">
                    </div>
                    
                    <div class="form-group">
                        <label for="message">Brief Details</label>
                        <textarea id="message" name="message" rows="3"></textarea>
                    </div>
                    
                    <button type="submit" class="button button-full">Request Free Callback</button>
                </form>
            </div>
            <div class="contact-info">
                <h3>Why choose us?</h3>
                <ul class="benefits-list">
                    <li>✓ Specialist child injury solicitors</li>
                    <li>✓ No win no fee guaranteed</li>
                    <li>✓ Free initial consultation</li>
                    <li>✓ Local solicitors nationwide</li>
                    <li>✓ 100% confidential advice</li>
                </ul>
            </div>
        </div>
    </section>
</div>
{% endblock %}

{% block faq_schema %}
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {
            "@type": "Question",
            "name": "Who can make a child injury claim?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Parents or legal guardians can make a claim on behalf of a child who has suffered an injury due to someone else's negligence."
            }
        },
        {
            "@type": "Question",
            "name": "How much compensation can I claim?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Compensation amounts vary based on the severity of the injury. Minor injuries might attract £1,000-£5,000, while severe injuries can result in six-figure settlements."
            }
        }
    ]
}
</script>
{% endblock %}
"""

LOCATION_TEMPLATE_HTML = """{% extends "base.html" %}
{% block title %}Child Injury Claims in {{ location_name }} | {{ county if location_type == 'town' else 'Local Solicitors' }}{% endblock %}
{% block description %}Expert child injury compensation claims in {{ location_name }}. No Win No Fee solicitors serving {{ location_name }} and surrounding areas. Free consultation.{% endblock %}
{% block content %}
<div class="hero hero-location">
    <div class="container">
        <h1>Child Injury Claims in {{ location_name }}</h1>
        <p class="hero-subtitle">Specialist solicitors helping families in {{ location_name }}{% if postcode %} ({{ postcode }}){% endif %} and the surrounding areas</p>
        <div class="hero-cta">
            <a href="/#contact" class="button button-large">Free Local Claim Assessment</a>
        </div>
    </div>
</div>

<div class="container">
    <nav class="breadcrumbs" aria-label="Breadcrumb">
        <ol>
            <li><a href="/">Home</a></li>
            <li><a href="/#areas-covered">Near Me</a></li>
            {% if location_type == 'town' %}
            <li><a href="/near-me/{{ county.lower().replace(' ', '-') }}/">{{ county }}</a></li>
            <li>{{ location_name }}</li>
            {% else %}
            <li>{{ location_name }}</li>
            {% endif %}
        </ol>
    </nav>

    <div class="content-section">
        {{ page_content|safe }}
    </div>

    {% if location_type == 'county' %}
    <section class="towns-list">
        <h2>Towns in {{ location_name }} We Cover</h2>
        <div class="town-grid">
            {% for town in towns %}
            <a href="/near-me/{{ county.lower().replace(' ', '-') }}-{{ town.town.lower().replace(' ', '-') }}/" class="town-card">
                <h3>{{ town.town }}</h3>
                <p>{{ town.postcode }}</p>
            </a>
            {% endfor %}
        </div>
    </section>
    {% else %}
    <section class="nearby-areas">
        <h2>Nearby Areas We Also Cover</h2>
        <ul class="nearby-list">
            {% for nearby in nearby_towns %}
            <li><a href="/near-me/{{ county.lower().replace(' ', '-') }}-{{ nearby.lower().replace(' ', '-') }}/">{{ nearby }}</a></li>
            {% endfor %}
            <li><a href="/near-me/{{ county.lower().replace(' ', '-') }}/">View all {{ county }} locations →</a></li>
        </ul>
    </section>
    {% endif %}

    <section id="contact" class="contact-section">
        <h2>Free Claim Assessment in {{ location_name }}</h2>
        <div class="contact-grid">
            <div class="contact-form">
                <form name="claim-assessment-{{ location_name.lower().replace(' ', '-') }}" method="POST" data-netlify="true">
                    <input type="hidden" name="form-name" value="claim-assessment-{{ location_name.lower().replace(' ', '-') }}">
                    
                    <div class="form-group">
                        <label for="name">Your Name *</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="phone">Phone Number *</label>
                        <input type="tel" id="phone" name="phone" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="message">Brief Details</label>
                        <textarea id="message" name="message" rows="3" placeholder="Tell us about your child's injury..."></textarea>
                    </div>
                    
                    <button type="submit" class="button button-full">Get Free Local Advice</button>
                </form>
            </div>
            <div class="contact-info">
                <h3>Local Service in {{ location_name }}</h3>
                <ul class="benefits-list">
                    <li>✓ Specialist child injury solicitors</li>
                    <li>✓ No win no fee guaranteed</li>
                    <li>✓ Free {{ location_name }} consultation</li>
                    <li>✓ Local knowledge and expertise</li>
                    <li>✓ 100% confidential advice</li>
                </ul>
                <p class="urgent-note">Don't wait - there are time limits for claims. Contact us today.</p>
            </div>
        </div>
    </section>
</div>
{% endblock %}

{% block faq_schema %}
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "LegalService",
    "name": "Child Injury Claims {{ location_name }}",
    "areaServed": {
        "@type": "City",
        "name": "{{ location_name }}"
    },
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "{{ location_name }}",
        "addressRegion": "{{ county if location_type == 'town' else location_name }}",
        "addressCountry": "UK"
    }
}
</script>
{% endblock %}
"""

SITEMAP_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{{ site_url }}/</loc>
        <lastmod>{{ build_date }}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>1.0</priority>
    </url>
    {% for county, towns in locations_by_county.items() %}
    <url>
        <loc>{{ site_url }}/near-me/{{ county.lower().replace(' ', '-') }}/</loc>
        <lastmod>{{ build_date }}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>
    {% for town in towns %}
    <url>
        <loc>{{ site_url }}/near-me/{{ county.lower().replace(' ', '-') }}-{{ town.town.lower().replace(' ', '-') }}/</loc>
        <lastmod>{{ build_date }}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    {% endfor %}
    {% endfor %}
</urlset>
"""

ROBOTS_TXT = """User-agent: *
Allow: /
Sitemap: {site_url}/sitemap.xml
"""

# ============================================================================
# CSS STYLES
# ============================================================================

CSS_STYLES = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary-color: #2c3e50;
    --secondary-color: #e74c3c;
    --accent-color: #3498db;
    --light-bg: #f8f9fa;
    --dark-text: #333;
    --light-text: #fff;
    --gray-text: #666;
    --border-color: #ddd;
    --success-color: #27ae60;
    --shadow: 0 2px 10px rgba(0,0,0,0.1);
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    line-height: 1.6;
    color: var(--dark-text);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

h1 { font-size: 2.5rem; margin-bottom: 1rem; color: var(--primary-color); }
h2 { font-size: 2rem; margin: 2rem 0 1rem; color: var(--primary-color); }
h3 { font-size: 1.5rem; margin: 1.5rem 0 1rem; color: var(--primary-color); }

.site-header {
    background: var(--light-text);
    box-shadow: var(--shadow);
    position: sticky;
    top: 0;
    z-index: 100;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
}

.logo h1 {
    font-size: 1.5rem;
    margin: 0;
    color: var(--primary-color);
}

.logo a { text-decoration: none; }

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
    align-items: center;
}

.nav-menu a {
    text-decoration: none;
    color: var(--dark-text);
    font-weight: 500;
}

.nav-menu a:hover { color: var(--secondary-color); }

.mobile-menu-toggle { display: none; }

.button {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    background: var(--secondary-color);
    color: var(--light-text);
    text-decoration: none;
    border-radius: 5px;
    font-weight: 600;
    transition: background-color 0.3s;
    border: none;
    cursor: pointer;
}

.button:hover { background: #c0392b; }
.button-large { padding: 1rem 2rem; font-size: 1.1rem; }
.button-full { width: 100%; }
.cta-button {
    background: var(--secondary-color);
    color: var(--light-text) !important;
    padding: 0.5rem 1rem;
    border-radius: 5px;
}

.hero {
    background: linear-gradient(135deg, var(--primary-color), #34495e);
    color: var(--light-text);
    padding: 4rem 0;
    text-align: center;
}

.hero h1 { color: var(--light-text); font-size: 3rem; }
.hero-subtitle { font-size: 1.2rem; margin: 1rem 0 2rem; opacity: 0.9; }
.hero-location { background: linear-gradient(135deg, #2980b9, var(--primary-color)); }

.content-section {
    background: var(--light-text);
    padding: 2rem;
    border-radius: 10px;
    box-shadow: var(--shadow);
    margin: 2rem 0;
}

.content-section h2 { margin-top: 0; }

.county-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.county-card {
    background: var(--light-bg);
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: var(--shadow);
}

.county-card h3 { margin: 0 0 1rem 0; font-size: 1.2rem; }
.county-card h3 a { text-decoration: none; color: var(--primary-color); }
.town-list { list-style: none; }
.town-list li { margin: 0.5rem 0; }
.town-list a { color: var(--gray-text); text-decoration: none; }
.town-list a:hover { color: var(--secondary-color); }

.faq-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.faq-item {
    background: var(--light-bg);
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: var(--shadow);
}

.faq-item h3 { margin: 0 0 1rem 0; color: var(--primary-color); }

.contact-section {
    background: var(--light-bg);
    padding: 3rem 0;
    margin: 3rem 0;
}

.contact-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin: 2rem 0;
}

.contact-form {
    background: var(--light-text);
    padding: 2rem;
    border-radius: 10px;
    box-shadow: var(--shadow);
}

.form-group { margin-bottom: 1rem; }
.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
}
.form-group input,
.form-group textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: 5px;
    font-family: inherit;
}

.benefits-list {
    list-style: none;
    margin: 1.5rem 0;
}
.benefits-list li { margin: 0.75rem 0; font-size: 1.1rem; }

.urgent-note {
    background: #fff3cd;
    border: 1px solid #ffeeba;
    color: #856404;
    padding: 1rem;
    border-radius: 5px;
    margin-top: 1rem;
}

.breadcrumbs {
    margin: 1rem 0;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--border-color);
}
.breadcrumbs ol {
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.breadcrumbs li:not(:last-child):after {
    content: '›';
    margin-left: 0.5rem;
    color: var(--gray-text);
}
.breadcrumbs a { color: var(--primary-color); text-decoration: none; }

.town-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}
.town-card {
    background: var(--light-bg);
    padding: 1rem;
    border-radius: 5px;
    text-decoration: none;
    color: var(--dark-text);
    transition: transform 0.3s;
    box-shadow: var(--shadow);
}
.town-card:hover { transform: translateY(-3px); }
.town-card h3 { margin: 0 0 0.5rem 0; font-size: 1.1rem; }

.nearby-list {
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin: 1rem 0;
}
.nearby-list li {
    background: var(--light-bg);
    padding: 0.5rem 1rem;
    border-radius: 20px;
}
.nearby-list a { text-decoration: none; color: var(--primary-color); }

.site-footer {
    background: var(--primary-color);
    color: var(--light-text);
    padding: 3rem 0 1rem;
    margin-top: 3rem;
}
.footer-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}
.footer-about .trust-badge { margin: 0.5rem 0; color: var(--accent-color); }
.footer-links ul { list-style: none; }
.footer-links a {
    color: var(--light-text);
    text-decoration: none;
    opacity: 0.8;
}
.footer-links a:hover { opacity: 1; }
.footer-contact a { color: var(--light-text); text-decoration: none; }
.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.1);
}
.small-text { font-size: 0.9rem; opacity: 0.8; margin-top: 1rem; }

@media (max-width: 768px) {
    h1 { font-size: 2rem; }
    h2 { font-size: 1.5rem; }
    .mobile-menu-toggle {
        display: block;
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
    }
    .nav-menu {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: var(--light-text);
        flex-direction: column;
        padding: 1rem;
        box-shadow: var(--shadow);
    }
    .nav-menu.active { display: flex; }
    .contact-grid { grid-template-columns: 1fr; }
    .hero h1 { font-size: 2rem; }
    .county-grid { grid-template-columns: 1fr; }
}
"""

# ============================================================================
# JAVASCRIPT
# ============================================================================

JS_SCRIPT = """
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
        });
    });
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = 'red';
                    isValid = false;
                } else {
                    field.style.borderColor = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });
});
"""

# ============================================================================
# NETLIFY CONFIGURATION
# ============================================================================

NETLIFY_TOML = """
[build]
  command = "python build.py"
  publish = "output"

[build.environment]
  PYTHON_VERSION = "3.9"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
"""

# ============================================================================
# MAIN BUILD CLASS
# ============================================================================

class SiteGenerator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(self.base_dir, 'output')
        self.config = SITE_CONFIG
        
        # Process locations into hierarchical structure
        self.locations_by_county = {}
        for county, town, postcode in LOCATIONS:
            if county not in self.locations_by_county:
                self.locations_by_county[county] = []
            self.locations_by_county[county].append({
                'town': town,
                'postcode': postcode,
                'county': county
            })
    
    def clean_output_dir(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)
        os.makedirs(os.path.join(self.output_dir, 'near-me'))
    
    def get_nearby_towns(self, county, current_town):
        towns = self.locations_by_county[county]
        town_names = [t['town'] for t in towns]
        if current_town in town_names:
            current_index = town_names.index(current_town)
            start = max(0, current_index - 3)
            end = min(len(town_names), current_index + 4)
            nearby = town_names[start:end]
            if current_town in nearby:
                nearby.remove(current_town)
            return nearby[:5]
        return []
    
    def generate_homepage(self):
        env = Environment()
        env.get_template = lambda name: Template(globals()[f"{name.upper().replace('.', '_')}_TEMPLATE"])
        
        template = env.get_template('base.html')
        
        # Render homepage
        homepage_html = Template(INDEX_TEMPLATE).render(
            site_name=self.config['site_name'],
            site_url=self.config['site_url'],
            phone=self.config['phone'],
            email=self.config['email'],
            css_content=CSS_STYLES,
            js_content=JS_SCRIPT,
            homepage_content=markdown.markdown(HOMEPAGE_MD),
            locations_by_county=self.locations_by_county
        )
        
        output_path = os.path.join(self.output_dir, 'index.html')
        with open(output_path, 'w') as f:
            f.write(homepage_html)
        print("✓ Generated homepage")
    
    def generate_location_pages(self):
        for county, towns in self.locations_by_county.items():
            county_slug = county.lower().replace(' ', '-')
            county_dir = os.path.join(self.output_dir, 'near-me', county_slug)
            os.makedirs(county_dir, exist_ok=True)
            
            # Generate county page
            county_content = LOCATION_TEMPLATE_MD.replace('[LOCATION]', county)
            county_content = county_content.replace('[COUNTY]', county)
            county_content = county_content.replace('[POSTCODE]', '')
            
            county_html = Template(LOCATION_TEMPLATE_HTML).render(
                site_name=self.config['site_name'],
                site_url=self.config['site_url'],
                phone=self.config['phone'],
                email=self.config['email'],
                css_content=CSS_STYLES,
                js_content=JS_SCRIPT,
                page_content=markdown.markdown(county_content),
                location_name=county,
                county=county,
                location_type='county',
                towns=towns,
                postcode=None
            )
            
            county_output = os.path.join(county_dir, 'index.html')
            with open(county_output, 'w') as f:
                f.write(county_html)
            print(f"  ✓ Generated county page: {county}")
            
            # Generate town pages
            for town_data in towns:
                town = town_data['town']
                postcode = town_data['postcode']
                town_slug = f"{county_slug}-{town.lower().replace(' ', '-')}"
                town_dir = os.path.join(self.output_dir, 'near-me', town_slug)
                os.makedirs(town_dir, exist_ok=True)
                
                town_content = LOCATION_TEMPLATE_MD.replace('[LOCATION]', town)
                town_content = town_content.replace('[COUNTY]', county)
                town_content = town_content.replace('[POSTCODE]', postcode)
                
                town_html = Template(LOCATION_TEMPLATE_HTML).render(
                    site_name=self.config['site_name'],
                    site_url=self.config['site_url'],
                    phone=self.config['phone'],
                    email=self.config['email'],
                    css_content=CSS_STYLES,
                    js_content=JS_SCRIPT,
                    page_content=markdown.markdown(town_content),
                    location_name=town,
                    county=county,
                    location_type='town',
                    postcode=postcode,
                    nearby_towns=self.get_nearby_towns(county, town)
                )
                
                town_output = os.path.join(town_dir, 'index.html')
                with open(town_output, 'w') as f:
                    f.write(town_html)
                print(f"    ✓ Generated town page: {town}, {county}")
    
    def generate_sitemap(self):
        sitemap_xml = Template(SITEMAP_TEMPLATE).render(
            site_url=self.config['site_url'],
            build_date=self.config['build_date'],
            locations_by_county=self.locations_by_county
        )
        
        output_path = os.path.join(self.output_dir, 'sitemap.xml')
        with open(output_path, 'w') as f:
            f.write(sitemap_xml)
        print("✓ Generated sitemap.xml")
    
    def generate_robots(self):
        robots = ROBOTS_TXT.format(site_url=self.config['site_url'])
        output_path = os.path.join(self.output_dir, 'robots.txt')
        with open(output_path, 'w') as f:
            f.write(robots)
        print("✓ Generated robots.txt")
    
    def generate_netlify_toml(self):
        output_path = os.path.join(self.base_dir, 'netlify.toml')
        with open(output_path, 'w') as f:
            f.write(NETLIFY_TOML)
        print("✓ Generated netlify.toml")
    
    def build(self):
        print("\n🚀 Building Child Injury Claims website...")
        print("=" * 50)
        
        self.clean_output_dir()
        self.generate_homepage()
        self.generate_location_pages()
        self.generate_sitemap()
        self.generate_robots()
        self.generate_netlify_toml()
        
        total_pages = sum(len(towns) for towns in self.locations_by_county.values()) + len(self.locations_by_county) + 1
        print("=" * 50)
        print(f"✅ Build complete! Generated {total_pages} pages")
        print(f"📁 Output directory: {self.output_dir}")
        print("\n📋 Next steps:")
        print("   1. Push to GitHub")
        print("   2. Connect to Netlify")
        print("   3. Add custom domain: childinjuryclaims.co.uk")
        print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    generator = SiteGenerator()
    generator.build()
