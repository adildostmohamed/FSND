from app import Artist
from flask_seeder import Seeder
import sys
import os
sys.path.append(os.path.abspath("app"))


class ArtistSeeder(Seeder):
    def run(self):
        seed_artists = [{
            "name": "Guns N Petals",
            "genres": "Rock n Roll",
            "city": "San Francisco",
            "state": "CA",
            "phone": "326-123-5000",
            "website": "https://www.gunsnpetalsband.com",
            "facebook_link": "https://www.facebook.com/GunsNPetals",
            "seeking_venue": True,
            "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
            "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        },
            {
            "name": "Matt Quevedo",
            "genres": "Jazz",
            "city": "New York",
            "state": "NY",
            "phone": "300-400-5000",
            "facebook_link": "https://www.facebook.com/mattquevedo923251523",
            "seeking_venue": True,
            "seeking_description": "I am awesome! Book me now for all your slots",
            "website": "https://www.mattyQ.com",
            "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        },
            {
            "name": "The Wild Sax Band",
            "genres": "Jazz,Classical",
            "city": "San Francisco",
            "state": "CA",
            "phone": "432-325-5432",
            "seeking_venue": True,
            "seeking_description": "Everyone loves sax, let us prove it to you",
            "website": "https://www.wildsax.com",
            "facebook_link": "https://www.facebook.com/wildsaxpeople",
            "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        }]

        for artist_data in seed_artists:
            artist = Artist(name=artist_data['name'], genres=artist_data['genres'],
                            city=artist_data['city'], state=artist_data['state'], phone=artist_data['phone'], website=artist_data['website'], facebook_link=artist_data['facebook_link'], seeking_venue=artist_data['seeking_venue'], seeking_description=artist_data['seeking_description'], image_link=artist_data['image_link'])
            print("Adding artist: %s" % artist)
            self.db.session.add(artist)
