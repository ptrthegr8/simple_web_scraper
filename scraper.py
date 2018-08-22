#!/usr/bin/env python
'''
Simple Web Scraper

Given a website url, this program finds all urls, email addresses
and phone numbers in website's html code and prints them.
'''
import sys
import re
import requests
import argparse


def get_response(url):
    '''Returns text from targeted url if valid url.'''
    res = requests.get(url)
    try:
        res.raise_for_status()
        return res.text
    except Exception as exc:
        print 'Problem Encountered: %s' % exc
        sys.exit(1)


def scrape_urls(string):
    '''Returns a sorted string of urls'''
    matches = sorted(set(re.findall(
        (r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
         r'(?:%[0-9a-fA-F][0-9a-fA-F]))+'), string
    )))
    return '\n'.join(matches)


def scrape_emails(string):
    '''Returns sorted string of emails'''
    matches = sorted(set(re.findall(
        r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', string
    )))
    return '\n'.join(matches)


def scrape_phonenums(string):
    '''Returns sorted string of phone numbers'''
    matches = re.findall(
        (r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})'
         r'(\se?x?t?(\d*))?'), string
    )
    digits = map(lambda x: x[0:3], matches)
    joined_digits = sorted(set(['-'.join(d) for d in digits]))
    return '\n'.join(joined_digits)


def create_parser():
    '''Returns argument parser for use in main() function'''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'website', help='website to extract urls, emails, & phone numbers from'
    )
    return parser


def main(args):
    '''Parses arguments, calls scrape functions, and prints results'''
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    if parsed_args.website:
        text = get_response(parsed_args.website)
        urls = scrape_urls(text)
        emails = scrape_emails(text)
        phonenums = scrape_phonenums(text)

        print '\n'
        print 'URLS:', '\n'
        print urls if urls else None, '\n'
        print 'EMAILS:', '\n'
        print emails if emails else None, '\n'
        print 'PHONE NUMBERS:', '\n'
        print phonenums if phonenums else None, '\n'
    else:
        parser.print_usage()
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
