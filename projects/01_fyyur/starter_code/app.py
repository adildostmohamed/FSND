#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

Migrate(app, db)

# ADDED: init seeder to generate data
seeder = FlaskSeeder()
seeder.init_app(app, db)

# ADDED: helper methods to get past and upcoming shows


def get_genres(genres):
    formatted_genres = genres.split(',')
    return formatted_genres


def get_past_shows(shows):
    past_shows = list(filter(lambda x: x.start_time <
                             datetime.today(), shows))
    formatted_past_shows = list(map(lambda x: x.format(), past_shows))
    return formatted_past_shows


def get_upcoming_shows(shows):
    upcoming_shows = list(filter(lambda x: x.start_time >=
                                 datetime.today(), shows))
    formatted_upcoming_shows = list(map(lambda x: x.format(), upcoming_shows))
    return formatted_upcoming_shows

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    name = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120))
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500), nullable=False)
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venue')

    def format(self):
        upcoming_shows = get_upcoming_shows(self.shows)
        upcoming_shows_count = len(upcoming_shows)
        past_shows = get_past_shows(self.shows)
        past_shows_count = len(past_shows)
        genres = get_genres(self.genres)
        """ Returns a formatted dictionary for venue """
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'genres': genres,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'shows': self.shows,
            'past_shows': past_shows,
            'past_shows_count': past_shows_count,
            'upcoming_shows': upcoming_shows,
            'upcoming_shows_count': upcoming_shows_count,
        }


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    name = db.Column(db.String, unique=True, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist')

    def format(self):
        upcoming_shows = get_upcoming_shows(self.shows)
        upcoming_shows_count = len(upcoming_shows)
        past_shows = get_past_shows(self.shows)
        past_shows_count = len(past_shows)
        genres = get_genres(self.genres)
        """ Returns a formatted dictionary for artist """
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'genres': genres,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'shows': self.shows,
            'past_shows': past_shows,
            'past_shows_count': past_shows_count,
            'upcoming_shows': upcoming_shows,
            'upcoming_shows_count': upcoming_shows_count,
        }


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    start_time = db.Column(db.DateTime, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)

    def format(self):
        """ Returns a formatted dict for show """
        return {
            'id': self.id,
            'artist_id': self.artist_id,
            'artist_name': self.artist.name,
            'artist_image_link': self.artist.image_link,
            'venue_id': self.venue_id,
            'venue_name': self.venue.name,
            'venue_image_link': self.venue.image_link,
            'start_time': str(self.start_time)
        }


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    lastest_artists = Artist.query.order_by(
        desc(Artist.created_at)).limit(10).all()
    latest_venues = Venue.query.order_by(
        desc(Venue.created_at)).limit(10).all()
    latest_shows = Show.query.order_by(desc(Show.created_at)).limit(10).all()
    return render_template('pages/home.html', artists=lastest_artists, venues=latest_venues, shows=latest_shows)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venues_data = []
    # GET DISTINCT LIST OF CITIES AND STATES
    cities = db.session.query(Venue.city, Venue.state).distinct(
        Venue.city, Venue.state)
    # GET AVAILABLE VENUES ID AND NAME FOR EACH CITY AND STATE
    for city in cities:
        venues_in_city = db.session.query(Venue.id, Venue.name).filter(
            Venue.city == city[0]).filter(Venue.state == city[1])
        venues_data.append({
            "city": city[0],
            "state": city[1],
            "venues": venues_in_city
        })
    return render_template('pages/venues.html', areas=venues_data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term')
    venues = Venue.query.filter(
        Venue.name.ilike('%{}%'.format(search_term))).all()

    venues_data = []
    for venue in venues:
        venue_format = venue.format()
        venue_tmp = {}
        venue_tmp['id'] = venue_format['id']
        venue_tmp['name'] = venue_format['name']
        venue_tmp['num_upcoming_shows'] = venue_format['upcoming_shows_count']
        venues_data.append(venue_tmp)

    response = {}
    response['count'] = len(venues_data)
    response['data'] = venues_data
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    data = Venue.query.get_or_404(venue_id)
    venue = data.format()
    return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    venue_name = ''
    try:
        name = request.form['name']
        venue_name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        address = request.form['address']
        phone = request.form['phone']
        tmp_genres = request.form.getlist('genres')
        genres = ','.join(tmp_genres)
        image_link = request.form['image_link']
        facebook_link = request.form['facebook_link']
        website = request.form['website']
        seeking_talent = True if 'seeking_talent' in request.form else False
        seeking_description = request.form['seeking_description']
        venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, facebook_link=facebook_link,
                      image_link=image_link, website=website, seeking_talent=seeking_talent, seeking_description=seeking_description)
        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('Could not create details for venue, please try again')
        return redirect(url_for('create_venue_form'))
    else:
        flash('Venue ' + venue_name + ' was successfully listed!')
        return redirect(url_for('index'))


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = Artist.query.all()
    artists = list(map(lambda x: x.format(), data))
    return render_template('pages/artists.html', artists=artists)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term')
    artists = Artist.query.filter(
        Artist.name.ilike('%{}%'.format(search_term))).all()

    artists_data = []
    for artist in artists:
        artist_format = artist.format()
        artist_tmp = {}
        artist_tmp['id'] = artist_format['id']
        artist_tmp['name'] = artist_format['name']
        artist_tmp['num_upcoming_shows'] = artist_format['upcoming_shows_count']
        artists_data.append(artist_tmp)

    response = {}
    response['count'] = len(artists_data)
    response['data'] = artists_data
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    data = Artist.query.get_or_404(artist_id)
    artist = data.format()
    print(artist)
    return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    form = ArtistForm()
    form.state.default = artist.state
    form.process()
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # artist record with ID <artist_id> using the new attributess
    error = False
    artist_name = ''
    try:
        artist = Artist.query.get_or_404(artist_id)
        artist.name = request.form['name']
        artist_name = request.form['name']
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        tmp_genres = request.form.getlist('genres')
        artist.genres = ','.join(tmp_genres)
        artist.image_link = request.form['image_link']
        artist.facebook_link = request.form['facebook_link']
        artist.website = request.form['website']
        artist.seeking_venue = True if 'seeking_venue' in request.form else False
        artist.seeking_description = request.form['seeking_description']
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('Could not update details for Artist ' + artist_name +
              ', please try again')
        return redirect(url_for('edit_artist', artist_id=artist_id))
    else:
        flash('Artist ' + artist_name +
              ' was successfully updated!')
        return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    form = VenueForm()
    form.state.default = venue.state
    form.process()
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # venue record with ID <venue_id> using the new attributes
    error = False
    venue_name = ''
    try:
        venue = Venue.query.get_or_404(venue_id)
        venue.name = request.form['name']
        venue_name = request.form['name']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        tmp_genres = request.form.getlist('genres')
        venue.genres = ','.join(tmp_genres)
        venue.image_link = request.form['image_link']
        venue.facebook_link = request.form['facebook_link']
        venue.website = request.form['website']
        venue.seeking_talent = True if 'seeking_talent' in request.form else False
        venue.seeking_description = request.form['seeking_description']
        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('Could not update details for Venue ' + venue_name +
              ', please try again')
        return redirect(url_for('edit_venue', venue_id=venue_id))
    else:
        flash('Venue ' + venue_name +
              ' was successfully updated!')
        return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    artist_name = ''
    try:
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        phone = request.form['phone']
        tmp_genres = request.form.getlist('genres')
        genres = ','.join(tmp_genres)
        image_link = request.form['image_link']
        facebook_link = request.form['facebook_link']
        website = request.form['website']
        seeking_venue = True if 'seeking_venue' in request.form else False
        seeking_description = request.form['seeking_description']
        artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link,
                        image_link=image_link, website=website, seeking_venue=seeking_venue, seeking_description=seeking_description)
        artist_name = artist.name
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('Could not create details for artist, please try again')
        return redirect(url_for('create_artist_form'))
    else:
        flash('Artist ' + artist_name + ' was successfully listed!')
        return redirect(url_for('index'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # num_shows should be aggregated based on number of upcoming shows per venue.
    data = Show.query.all()
    shows = list(map(lambda x: x.format(), data))
    return render_template('pages/shows.html', shows=shows)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    form.artist_id.choices = [(artist.id, artist.name)
                              for artist in Artist.query.order_by('name').all()]
    form.venue_id.choices = [(venue.id, venue.name)
                             for venue in Venue.query.order_by('name').all()]
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    error = False
    try:
        artist_id = request.form['artist_id']
        venue_id = request.form['venue_id']
        start_time = request.form['start_time']
        show = Show(artist_id=artist_id, venue_id=venue_id,
                    start_time=start_time)
        db.session.add(show)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('Could not create show, please try again')
        return redirect(url_for('create_shows'))
    else:
        flash('Show was successfully listed!')
        return redirect(url_for('index'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
