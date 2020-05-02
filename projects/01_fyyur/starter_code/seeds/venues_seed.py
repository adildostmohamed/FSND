from app import Venue
from flask_seeder import Seeder
import sys
import os
sys.path.append(os.path.abspath("app"))


class VenuesSeeder(Seeder):
    def run(self):
        seed_venues = [{
            "name": "The Musical Hop",
            "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
            "address": "1015 Folsom Street",
            "city": "San Francisco",
            "state": "CA",
            "phone": "123-123-1234",
            "website": "https://www.themusicalhop.com",
            "facebook_link": "https://www.facebook.com/TheMusicalHop",
            "seeking_talent": True,
            "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
            "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
        },
            {
                "name": "The Dueling Pianos Bar",
                "genres": ["Classical", "R&B", "Hip-Hop"],
                "address": "335 Delancey Street",
                "city": "New York",
                "state": "NY",
                "phone": "914-003-1132",
                "website": "https://www.theduelingpianos.com",
                "facebook_link": "https://www.facebook.com/theduelingpianos",
                "seeking_talent": True,
                "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
                "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
        },
            {
                "name": "Park Square Live Music & Coffee",
                "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
                "address": "34 Whiskey Moore Ave",
                "city": "San Francisco",
                "state": "CA",
                "phone": "415-000-1234",
                "website": "https://www.parksquarelivemusicandcoffee.com",
                "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
                "seeking_talent": True,
                "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
                "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        }]
        for venue_data in seed_venues:
            venue = Venue(name=venue_data['name'], genres=venue_data['genres'], address=venue_data['address'],
                          city=venue_data['city'], state=venue_data['state'], phone=venue_data['phone'], website=venue_data['website'], facebook_link=venue_data['facebook_link'], seeking_talent=venue_data['seeking_talent'], seeking_description=venue_data['seeking_description'], image_link=venue_data['image_link'])
            print("Adding venue: %s" % venue)
            self.db.session.add(venue)
