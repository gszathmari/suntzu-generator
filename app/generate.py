#!/usr/bin/env python

import markovgen
import time
import json
import os

def getQuote(corpus=None):
  # Recursion goodness
  if corpus:
    quoteGenerator = corpus
  else:
    quoteGenerator = markovgen.Markov()
    path, file     = os.path.split(os.path.abspath(__file__))
    lines          = [line.strip() for line in open(path + '/data/artofwar.txt')]
    [quoteGenerator.feed(line) for line in lines]

  # Generate quote
  quote	= quoteGenerator.generate_markov_text(max_size=128, seed=None, backward=False).capitalize()

  # If quote is too short, roll again
  if len(quote) > 128 or len(quote) < 50:
    return getQuote(quoteGenerator)
  else:
    return str(quote)

# Generate JSON output
def generateResponse():
  response = {'quote': getQuote(),
              'timestamp': int(time.time())}
  return json.dumps(response)

# Simple HTTP server
def run(environ, start_response):
  requestPath = str(environ['PATH_INFO'])

  if requestPath == '/v1/getquote': 
    data = generateResponse().encode('utf-8')
    status = '200 OK'
    response_headers = [
      ('Content-type','application/json'),
      ('Content-Length', str(len(data)))
    ]
  else:
    data = 'Not found'.encode('utf-8')
    status = '404 Not Found'
    response_headers = [
      ('Content-type','text/plain'),
      ('Content-Length', 0)
    ]
  start_response(status, response_headers)
  return iter([data])
