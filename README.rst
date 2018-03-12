AsyncBandsintown
Make asynchronous requests to the Bandsintown API for concert data


Examples
---------

.. code:: python

    request = BandsInTownRequest()
    request.fetch(location="austin, tx" artists=["mastodon", "russian circles"])
    print(request.results)

    [
      {'id': 16615838, 'city': 'Houston, TX', 'title': 'Mastodon @ White Oak Music Hall in Houston, TX', 
       'venue': 'White Oak Music Hall', 'thumb': 'https://s3.amazonaws.com/bit-photos/thumb/7419985.jpeg', 
       'artist': 'Mastodon', 'tickets': 'http://www.bandsintown.com/event/16615838/buy_tickets?app_id=async-bandsintown&artist=Mastodon&came_from=67', 
       'fmt_date': 'Wednesday, May 9, 2018 at 7:00PM', 'ticket_status': 'available'}, 
        
      {'id': 16641349, 'city': 'Austin, TX', 'title': 'Russian Circles @ Levitation in Austin, TX', 
       'venue': 'Levitation', 'thumb': 'https://s3.amazonaws.com/bit-photos/thumb/313047.jpeg', 
       'artist': 'Russian Circles', 'tickets': 'http://www.bandsintown.com/event/16641349/buy_tickets?app_id=async-bandsintown&artist=Russian+Circles&came_from=67', 
       'fmt_date': 'Friday, April 27, 2018 at 7:00PM', 'ticket_status': 'available'}
    ]

