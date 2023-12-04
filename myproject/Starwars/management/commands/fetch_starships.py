import requests
from django.core.management.base import BaseCommand
from Starwars.models import Starship  
import random


class Command(BaseCommand):
    help = 'Fetch starship data from SWAPI and initialize the database'

    def handle(self, *args, **kwargs):
        url_template = 'https://swapi.dev/api/starships/?page={}'
        
        # Loop through pages 1 to 4
        for page_num in range(1, 5):
            url = url_template.format(page_num)  # URL to fetch starship data
            
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                starships_data = data.get('results', [])
                
                for starship in starships_data:
                    # Extract relevant data
                    name = starship.get('name', '')
                    dodge = random.randint(1,25)
                    attack = random.randint(1,dodge)
                    defend = random.randint(1,25)
                    
                    
                    # Create or update your Starship model with the retrieved data
                    Starship.objects.update_or_create(
                        name=name,
                        attack = attack,
                        defend = defend,
                        dodge = dodge
                        
                    )
                
                self.stdout.write(self.style.SUCCESS(f'Successfully initialized the database with starship data from page {page_num}'))
            else:
                self.stderr.write(self.style.ERROR(f'Failed to fetch starship data from page {page_num}'))
