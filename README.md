# websocket-feed-examples
Examples using Benzinga's streaming websocket feeds. Documentation available at [https://docs.benzinga.io/](https://docs.benzinga.io/). 

See [https://docs.benzinga.io/benzinga/newsfeed-stream-v1.html](https://docs.benzinga.io/benzinga/newsfeed-stream-v1.html) for Newsfeed streaming documentation.

## Usage/Development

This is provided as an example only. It is not intended to be used as production code.

### Python

*Requires Python 3+*

Assumes Mac/Linux environment.

Using [Poetry](https://python-poetry.org/docs/), clone repo, change to `python-newsfeed` and run `poetry install`.

#### Run

```
export BZ_API_KEY='your api key'
python python-newsfeed/python_newsfeed/newsfeed.py
```
