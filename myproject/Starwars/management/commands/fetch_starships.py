import requests
from django.core.management.base import BaseCommand
from Starwars.models import Starship  
import random

def calculate_values(input_string):
    # Simple hash function to generate values based on the input string
    hash_value = hash(input_string)
    
    # Ensure dodge is greater than attack and keep values between 1 and 25
    attack = (hash_value % 25) + 1
    dodge = ((hash_value + 100) % 25) + 6  # Making sure dodge is greater than attack (minimum 6)
    defend = 31 - (attack + dodge)  # The sum of all three values is 31
    
    # Adjust values if they go out of bounds
    if defend < 1:
        defend = 1
        dodge = 30 - (attack + defend)
    elif defend > 25:
        defend = 25
        dodge = 30 - (attack + defend)
    
    return attack, dodge, defend


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
                    attack, dodge, defend = calculate_values(name)
                    
                    
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
