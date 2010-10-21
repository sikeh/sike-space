import re
import os

emphasis_pattern = re.compile(r'''
            \*          # Beginning emphasis tag -- an asterisk
            (           # Begin group for capturing phrase
            [^\*]+      # Capture anything except asterisks
            )           # End group
            \*          # Ending emphasis tag
           ''', re.VERBOSE)

print re.sub(emphasis_pattern, r'<em>\1</em>', 'Hello, *world*!')

print os.linesep

with open('cankiri.py', mode='r') as file:
    print file.read()