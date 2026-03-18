#!/usr/bin/env python3
"""
Static Site Generator for Child Injury Claims
Builds a complete hyperlocal website with 100+ location pages
"""

import os
import shutil
import csv
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import markdown
import pandas as pd

class SiteGenerator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.content_dir = os.path.join(self.base_dir, 'content')
        self.template_dir = os.path.join(self.base_dir, 'templates')
        self.static_dir = os.path.join(self.base_dir, 'static')
        self.output_dir = os.path.join(self.base_dir, 'output')
        
        # Setup Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=True
        )
        
        # Load locations data
        self.locations = self.load_locations()
        
        # Build date for sitemap
        self.build_date = datetime.now().strftime('%Y-%m-%d')
        
    def load_locations(self):
        """Load locations from CSV file"""
        csv_path = os.path.join(self.content_dir, 'data', 'locations.csv')
        df = pd.read_csv(csv_path)
        
        # Group by county for hierarchical structure
        locations_by_county = {}
        for _, row in df.iterrows():
            county = row['county']
            if county not in locations_by_county:
                locations_by_county[county] = []
            
            locations_by_county[county].append({
                'town': row['town'],
                'county': county,
                'postcode': row['postcode'],
                'slug': f"{county.lower().replace(' ', '-')}-{row['town'].lower().replace(' ', '-')}",
                'county_slug': county.lower().replace(' ', '-')
            })
        
        return locations_by_county
    
    def clean_output_dir(self):
        """Remove and recreate output directory"""
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)
        
        # Create necessary subdirectories
        os.makedirs(os.path.join(self.output_dir, 'css'))
        os.makedirs(os.path.join(self.output_dir, 'js'))
        os.makedirs(os.path.join(self.output_dir, 'images'))
        os.makedirs(os.path.join(self.output_dir, 'near-me'))
    
    def copy_static_files(self):
        """Copy static assets to output directory"""
        # Copy CSS
        shutil.copy(
            os.path.join(self.static_dir, 'css', 'style.css'),
            os.path.join(self.output_dir, 'css', 'style.css')
        )
        
        # Copy JS
        shutil.copy(
            os.path.join(self.static_dir, 'js', 'main.js'),
            os.path.join(self.output_dir, 'js', 'main.js')
        )
        
        # Copy images (if any)
        if os.path.exists(os.path.join(self.static_dir, 'images')):
            for img in os.listdir(os.path.join(self.static_dir, 'images')):
                shutil.copy(
                    os.path.join(self.static_dir, 'images', img),
                    os.path.join(self.output_dir, 'images', img)
                )
    
    def generate_homepage(self):
        """Generate the homepage"""
        template = self.env.get_template('index.html')
        
        # Load homepage content from markdown
        with open(os.path.join(self.content_dir, 'homepage.md'), 'r') as f:
            content = f.read()
        
        # Convert markdown to HTML
        html_content = markdown.markdown(content)
        
        # Prepare data for template
        data = {
            'content': html_content,
            'locations_by_county': self.locations,
            'build_date': self.build_date,
            'total_locations': sum(len(towns) for towns in self.locations.values())
        }
        
        # Render and save
        html = template.render(**data)
        output_path = os.path.join(self.output_dir, 'index.html')
        with open(output_path, 'w') as f:
            f.write(html)
        
        print(f"✓ Generated homepage")
    
    def generate_location_pages(self):
        """Generate all county and town pages"""
        template = self.env.get_template('location.html')
        
        # Load location page template content
        with open(os.path.join(self.content_dir, 'location_template.md'), 'r') as f:
            base_content = f.read()
        
        # Generate county pages and town pages
        for county, towns in self.locations.items():
            # Generate county page
            county_slug = county.lower().replace(' ', '-')
            county_dir = os.path.join(self.output_dir, 'near-me', county_slug)
            os.makedirs(county_dir, exist_ok=True)
            
            # County page content
            county_content = base_content.replace('[LOCATION]', county)
            county_content = county_content.replace('[COUNTY]', county)
            county_content = county_content.replace('[IS_COUNTY]', 'true')
            
            html_content = markdown.markdown(county_content)
            
            county_data = {
                'content': html_content,
                'location_name': county,
                'location_type': 'county',
                'towns': towns,
                'nearby_counties': self.get_nearby_counties(county),
                'build_date': self.build_date
            }
            
            html = template.render(**county_data)
            county_output = os.path.join(county_dir, 'index.html')
            with open(county_output, 'w') as f:
                f.write(html)
            
            print(f"  ✓ Generated county page: {county}")
            
            # Generate town pages for this county
            for town_data in towns:
                town = town_data['town']
                town_slug = town_data['slug']
                town_dir = os.path.join(self.output_dir, 'near-me', town_slug)
                os.makedirs(town_dir, exist_ok=True)
                
                # Town page content with location injection
                town_content = base_content.replace('[LOCATION]', town)
                town_content = town_content.replace('[COUNTY]', county)
                town_content = town_content.replace('[POSTCODE]', town_data['postcode'])
                town_content = town_content.replace('[IS_COUNTY]', 'false')
                
                html_content = markdown.markdown(town_content)
                
                town_data_dict = {
                    'content': html_content,
                    'location_name': town,
                    'county': county,
                    'postcode': town_data['postcode'],
                    'location_type': 'town',
                    'nearby_towns': self.get_nearby_towns(county, town),
                    'build_date': self.build_date
                }
                
                html = template.render(**town_data_dict)
                town_output = os.path.join(town_dir, 'index.html')
                with open(town_output, 'w') as f:
                    f.write(html)
                
                print(f"    ✓ Generated town page: {town}, {county}")
    
    def get_nearby_counties(self, current_county):
        """Get list of nearby counties (for internal linking)"""
        all_counties = list(self.locations.keys())
        current_index = all_counties.index(current_county)
        
        # Get 3 counties before and after (wrap around if needed)
        nearby = []
        for i in range(max(0, current_index - 3), min(len(all_counties), current_index + 4)):
            if all_counties[i] != current_county:
                nearby.append(all_counties[i])
        
        return nearby[:5]  # Limit to 5
    
    def get_nearby_towns(self, county, current_town):
        """Get list of nearby towns in same county"""
        towns = self.locations[county]
        town_names = [t['town'] for t in towns]
        
        if current_town in town_names:
            current_index = town_names.index(current_town)
            start = max(0, current_index - 3)
            end = min(len(town_names), current_index + 4)
            
            nearby = town_names[start:end]
            nearby.remove(current_town) if current_town in nearby else None
            
            return nearby[:5]
        
        return []
    
    def generate_sitemap(self):
        """Generate XML sitemap"""
        template = self.env.get_template('sitemap.xml')
        
        urls = []
        
        # Add homepage
        urls.append({
            'loc': 'https://childinjuryclaims.co.uk/',
            'lastmod': self.build_date,
            'priority': '1.0'
        })
        
        # Add all location pages
        for county, towns in self.locations.items():
            county_slug = county.lower().replace(' ', '-')
            urls.append({
                'loc': f'https://childinjuryclaims.co.uk/near-me/{county_slug}/',
                'lastmod': self.build_date,
                'priority': '0.9'
            })
            
            for town_data in towns:
                urls.append({
                    'loc': f'https://childinjuryclaims.co.uk/near-me/{town_data["slug"]}/',
                    'lastmod': self.build_date,
                    'priority': '0.8'
                })
        
        html = template.render(urls=urls)
        output_path = os.path.join(self.output_dir, 'sitemap.xml')
        with open(output_path, 'w') as f:
            f.write(html)
        
        print(f"✓ Generated sitemap.xml")
    
    def generate_robots_txt(self):
        """Generate robots.txt"""
        robots_content = """User-agent: *
Allow: /
Sitemap: https://childinjuryclaims.co.uk/sitemap.xml
"""
        output_path = os.path.join(self.output_dir, 'robots.txt')
        with open(output_path, 'w') as f:
            f.write(robots_content)
        
        print(f"✓ Generated robots.txt")
    
    def build(self):
        """Main build process"""
        print("🚀 Building Child Injury Claims website...")
        print("=" * 50)
        
        self.clean_output_dir()
        self.copy_static_files()
        self.generate_homepage()
        self.generate_location_pages()
        self.generate_sitemap()
        self.generate_robots_txt()
        
        print("=" * 50)
        print(f"✅ Build complete! {sum(len(towns) for towns in self.locations.values())} location pages generated")
        print(f"📁 Output directory: {self.output_dir}")

if __name__ == '__main__':
    generator = SiteGenerator()
    generator.build()
