#!/usr/bin/env python

import markovgen
import time
import json
import os
import re

def getQuote(quoteLength, corpus=None):
  # Recursion goodness
  if corpus:
    quoteGenerator = corpus
  else:
    quoteGenerator = markovgen.Markov()
    path, file     = os.path.split(os.path.abspath(__file__))
    lines          = [line.strip() for line in open(path + '/data/artofwar.txt')]
    [quoteGenerator.feed(line) for line in lines]

  # Generate quote
  quote	= quoteGenerator.generate_markov_text(max_size=quoteLength, seed=None, backward=False)

  # If quote is too short, roll again
  if len(quote) > quoteLength or len(quote) < 50:
    return getQuote(quoteLength, quoteGenerator)
  else:
    return capitalizeQuote(str(quote))

def capitalizeQuote(quote):
  rtn = re.split('([.!?] *)', quote)
  return ''.join([each.capitalize() for each in rtn])

# Generate JSON output
def generateResponse(quoteLength=250):
  response = {'quote': getQuote(quoteLength),
              'timestamp': int(time.time())}
  return json.dumps(response)

# Simple HTTP server
def run(environ, start_response):
  requestPath = str(environ['PATH_INFO'])
  status      = '200 OK'

  if requestPath == '/v1/getquote': 
    data = generateResponse().encode('utf-8')
    response_headers = [
      ('Content-type','application/json'),
    ]
  elif requestPath == '/v1/gettweet': 
    data = generateResponse(140).encode('utf-8')
    response_headers = [
      ('Content-type','application/json'),
    ]
  elif requestPath == '/healthcheck':
    data = 'OK\n'.encode('utf-8')
    response_headers = [
      ('Content-type','text/plain'),
    ]
  else:
    data = 'Not found'.encode('utf-8')
    status = '404 Not Found'
    response_headers = [
      ('Content-type','text/plain'),
    ]

  response_headers.append(('Content-Length', str(len(data))))
  response_headers.append(('Access-Control-Allow-Origin','*'))
  start_response(status, response_headers)
  return iter([data])
