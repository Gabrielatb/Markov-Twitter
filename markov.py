"""A Markov chain generator that can tweet random messages."""

import os
import sys
from random import choice
import twitter


def open_and_read_file(filenames):
    """Take list of files. Open them, read them, and return one long string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Take dictionary of Markov chains; return random text."""
    key = choice(chains.keys())
    words = [key[0], key[1]]
    chars_count = len(words[0]) + len(words[1]) + 1 

    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text).
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.
        word = choice(chains[key])

        if chars_count < 140 and (chars_count + 1 + len(word) <= 140):
            words.append(word)
            chars_count += len(word) + 1
            key = (key[1], word)
        else:
            return " ".join(words)
        



def tweet():
    """Create a tweet and send it to the Internet."""

    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.

    api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    print api.VerifyCredentials()

    filenames = sys.argv[1:]
    text = open_and_read_file(filenames)
    chains = make_chains(text)
    gen_text = make_text(chains)
    status = api.PostUpdate(gen_text)
    print status.text

tweet()
# Your task is to write a new function tweet, that will take chains as input
# tweet(chains)
