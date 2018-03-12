import json
import asyncio

from aiohttp import ClientSession

from errors import TooManyRequests, MissingArgument


class BandsInTownRequest:
    """
    A class that implements asynchronous API requests to
    the Bandsintown API

    Usage
    ---------
        request = BandsInTownRequest()
        request.fetch(location='Los Angeles, CA', artists=["mastodon", "tool"])
        print(request.results)
    """
    def __init__(self):
        self._loop = asyncio.get_event_loop()
        self.responses = None
        self.parameters = {
            'app_id': 'async-bandsintown',
            'api_version': '2.0',
            'location': None,
            'radius': '150',
            'format': 'json'
        }

    def error_handler(func):
        def decorator(self, *args, **kwargs):
            try:
                func(self, *args, **kwargs)
            except TypeError:
                raise MissingArgument("Expected one or more arguments to be passed.")
        return decorator

    @error_handler
    def fetch(self, location=None, artists=None):
        """
        The user entry point

        Parameters
        ----------
        location: str
            The location to search.
        artists: List[str]
            The artist(s) to search for.
        """
        self.parameters['location'] = location
        self.artists = artists
        self.urls = self._generate_urls()
        self._request_controller()

    def _generate_urls(self):
        urls = []
        for artist in self.artists:
            URL = 'http://api.bandsintown.com/artists/'+artist+'/events/search'
            urls.append(URL)
        return urls

    def _request_controller(self):
        future = self._gather_all_future_events()
        self._start_event_loop(future)

    def _gather_all_future_events(self):
        return self._schedule_future_event(self._run_tasks())

    def _start_event_loop(self, future):
        self._loop.run_until_complete(future)

    def _schedule_future_event(self, coroutine):
        return asyncio.ensure_future(coroutine)

    async def _run_tasks(self):
        async with ClientSession() as session:
            tasks = await self._gather_tasks(session)
            self.responses = await asyncio.gather(*tasks)

    async def _gather_tasks(self, session):
        tasks = []
        for url in self.urls:
            task = self._schedule_future_event(self._request(url, session))
            tasks.append(task)
        return tasks

    async def _request(self, url, session):
        async with session.get(url, params=self.parameters) as response:
            if response.status != 200:
                raise TooManyRequests("API rate limit was exceeded.")

            data = json.loads(await response.text())
            return self._create_concert(data)

    def _create_concert(self, data):
        if data:
            data = data[0]
            concert = {
                'id': data['id'],
                'city': data['venue']['city'] + ', ' + data['venue']['region'],
                'title': data['title'],
                'venue': data['venue']['name'],
                'thumb': data['artists'][0]['thumb_url'],
                'artist': data['artists'][0]['name'],
                'tickets': data['ticket_url'],
                'fmt_date': data['formatted_datetime'],
                'ticket_status': data['ticket_status']
            }
            return concert

    @property
    def results(self):
        if self.responses:
            self._clean_up_results()
            return self.responses

    def _clean_up_results(self):
        # Removes empty responses
        self.responses = [r for r in self.responses if r is not None]
