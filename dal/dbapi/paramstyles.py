###############################################################################
###
### Python DBAPI 2.0 Paramstyle Conversions
###
### Peter L. Buschman <plb@iotk.com>
###
### 2004-08-25
###
###
###############################################################################

import string
import re


##
## Categorization of paramstyles into different categories.  Different types of conversions
## will have different optimal algorithms.
##
PARAMSTYLES    = {
    'all'      : [ 'qmark', 'numeric', 'named', 'format', 'pyformat' ],
    'sequence' : [ 'qmark', 'numeric', 'format' ],
    'dict'     : [ 'named', 'pyformat' ],
    'token'    : [ 'qmark', 'format' ],
}


##
## Valid quote characters.
##
QUOTE_CHARS = [ '"', "'" ]  # " or '


##
## Valid escape characters.
##
ESCAPE_CHARS = [ '\\' ]


##
## This dictionary is used to lookup the placeholder strings for paramstyles whose
## placeholders are always the same.  This is currently just qmark and format.
##
PLACEHOLDER_TOKENS = {
    'qmark'    : '?',
    'format'   : '%s',
}


##
## This dictionary is used to lookup regular expressions for matching placeholders
## in a query string for a given paramstyle.
##
PLACEHOLDER_EXPS = {
    'qmark'    : re.compile(r'(\?)'),
    'numeric'  : re.compile(r'(:\d+)'),
    'named'    : re.compile(r'(:\w+)'),
    'format'   : re.compile(r'(%s)'),
    'pyformat' : re.compile(r'(%\(\w+\)s)'),
}

##
## This dictionary is used to lookup regular expressions for matching the parameter
## name contained within the placeholder of a named paramstyle.  This is currently
## just named and pyformat.
##
PARAMNAME_EXPS = {
    'named'    : re.compile(':(\w+)'),
    'pyformat' : re.compile('%\((\w+)\)s'),
}


##
## This dictionary contains lambda functions that return the appropriate replacement
## string given the parameter's sequence number.
##
PLACEHOLDER_SUBS = {
    'qmark'     : lambda param_number : '?',
    'numeric'   : lambda param_number : ':%d' % (param_number),
    'named'     : lambda param_number : ':param%d' % (param_number),
    'format'    : lambda param_number : '%s',
    'pyformat'  : lambda param_number : '%%(param%d)s' % (param_number),
}


##
## The following conversion matrix was inspired by similar code in Wichert Akkerman's dhm
## module at http://www.wiggy.net/code/python-dhm.
##
## The primary reason for listing conversion algorithms in a lookup table like this is that
## it allows for individual conversions to be overridden as additional, possibly experimental,
## algorithms are developed without breaking the functionality of the entire module.
##
CONVERSION_MATRIX = {
    'qmark' : {
        'qmark'    : lambda query, params : (query, params),
        'numeric'  : lambda query, params : sequence_to_sequence( 'qmark', 'numeric', query, params ),
        'named'    : lambda query, params : sequence_to_dict( 'qmark', 'named', query, params ),
        'format'   : lambda query, params : sequence_to_sequence( 'qmark', 'format', query, params ),
        'pyformat' : lambda query, params : sequence_to_dict( 'qmark', 'pyformat', query, params ),
    },
    'numeric' : {
        'qmark'    : lambda query, params : sequence_to_sequence( 'numeric', 'qmark', query, params ),
        'numeric'  : lambda query, params : (query, params),
        'named'    : lambda query, params : sequence_to_dict( 'numeric', 'named', query, params ),
        'format'   : lambda query, params : sequence_to_sequence( 'numeric', 'format', query, params ),
        'pyformat' : lambda query, params : sequence_to_dict( 'numeric', 'pyformat', query, params ),
    },
    'named' : {
        'qmark'    : lambda query, params : dict_to_sequence( 'named', 'qmark', query, params ),
        'numeric'  : lambda query, params : dict_to_sequence( 'named', 'numeric', query, params ),
        'named'    : lambda query, params : (query, params),
        'format'   : lambda query, params : dict_to_sequence( 'named', 'format', query, params ),
        'pyformat' : lambda query, params : dict_to_dict( 'named', 'pyformat', query, params ),
    },
    'format' : {
        'qmark'    : lambda query, params : sequence_to_sequence( 'format', 'qmark', query, params ),
        'numeric'  : lambda query, params : sequence_to_sequence( 'format', 'numeric', query, params ),
        'named'    : lambda query, params : sequence_to_dict( 'format', 'named', query, params ),
        'format'   : lambda query, params : (query, params),
        'pyformat' : lambda query, params : sequence_to_dict( 'format', 'pyformat', query, params ),
    },
    'pyformat' : {
        'qmark'    : lambda query, params : dict_to_sequence( 'pyformat', 'qmark', query, params ),
        'numeric'  : lambda query, params : dict_to_sequence( 'pyformat', 'numeric', query, params ),
        'named'    : lambda query, params : dict_to_dict( 'pyformat', 'named', query, params ),
        'format'   : lambda query, params : dict_to_sequence( 'pyformat', 'format', query, params ),
        'pyformat' : lambda query, params : (query, params),
    },
}

##
## Return True if the character at pos in string is escaped.
##
def escaped( string, pos ):
    escape_chars = ESCAPE_CHARS
    count = 0
    if pos > 0:
        pos -= 1
        if string[pos] in escape_chars:
            escape_char = string[pos]
            while string[pos] == escape_char and pos >= 0:
                count += 1
                pos -= 1
    if count % 2 == 1:
        return True
    else:
        return False

##
## Return True if the string is quoted.
##
def quoted( string ):
    if string[0] in QUOTE_CHARS and string[-1] in QUOTE_CHARS:
        return True
    else:
        return False

##
##
##
class SegmentizeError(Exception):
    """
    Error associated with string segmentization.
    """
    pass


##
## Parse a string into quoted and non-quoted segments.  We do this so that it is easy to tell
## which segments of a string to look for placeholders in and which to ignore.
##
def segmentize( string ):
    """
    Split a string into quoted and non-quoted segments.
    """
    quote_chars     = QUOTE_CHARS
    segments        = []
    current_segment = ''
    previous_char   = None
    quote_char      = None
    quoted          = False
    pos             = 0
    for char in string:
        if quoted:
            if char == quote_char and not escaped( string, pos ):
                current_segment += char
                segments.append(current_segment)
                current_segment = ''
                previous_char = char
                quoted = False
            else:
                current_segment += char
                previous_char = char
        elif not quoted:
            if char in quote_chars and not escaped( string, pos ):
                if current_segment != '':
                    segments.append(current_segment)
                    current_segment = ''
                quoted = True
                quote_char = char
                current_segment += char
                previous_char = char
            else:
                current_segment += char
                previous_char = char
        pos += 1
    if current_segment != '':
        segments.append(current_segment)
    if quoted:
        raise SegmentizeError, 'Unmatched quotes in string'

    return segments


##
## Convert from a sequence-based paramstyle to another sequence-based paramstyle.
##
def sequence_to_sequence( from_paramstyle, to_paramstyle, query, params ):
    placeholder_exp = PLACEHOLDER_EXPS[from_paramstyle]
    placeholder_sub = PLACEHOLDER_SUBS[to_paramstyle]
    new_query = ''
    segments = segmentize(query)
    new_params = params
    param_num = 0
    for segment in segments:
        #
        # If the segment is a quoted string, do not check for placeholders.
        #
        if quoted(segment):
            new_query += segment
        else:
            #
            # ...otherwise, check for any placeholder matches.
            #
            pos = 0
            match = placeholder_exp.search(segment, pos)
            if match != None:
                #
                # If there are placeholders...
                #
                while match != None:
                    new_query += segment[pos:match.start()]
                    #
                    # Ignore the placeholder if it is escaped...
                    #
                    if escaped( segment, match.start() ):
                        new_query += segment[match.start():match.end()]
                    else:
                        #
                        # ...otherwise replace it.
                        #
                        param_num += 1
                        new_placeholder = placeholder_sub(param_num)
                        new_query += new_placeholder
                    pos = match.end()
                    match = placeholder_exp.search(segment, pos)
                #
                # Tack on the end of the string segment when there are no more matches.
                #
                if pos < len(segment):
                    new_query += segment[pos:]
            #
            # If there were no placeholders, just add the segment to our query.
            #
            else:
                new_query += segment

    return new_query, new_params


##
## Convert from a sequence-based paramstyle to a dictionary-based paramstyle.
##
def sequence_to_dict( from_paramstyle, to_paramstyle, query, params ):
    placeholder_exp = PLACEHOLDER_EXPS[from_paramstyle]
    placeholder_sub = PLACEHOLDER_SUBS[to_paramstyle]
    new_query = query
    new_params = {}
    param_num = 0
    for placeholder in placeholder_exp.findall(query):
        param_num += 1
        param_name = 'param%d' % (param_num)
        new_placeholder = placeholder_sub(param_num)
        new_query = string.replace(new_query, placeholder, new_placeholder, 1)
        new_params[param_name] = params[param_num-1]
    return new_query, new_params


##
## Convert from a dictionary-based paramstyle to a sequence-based paramstyle.
##
def dict_to_sequence( from_paramstyle, to_paramstyle, query, params ):
    placeholder_exp = PLACEHOLDER_EXPS[from_paramstyle]
    placeholder_sub = PLACEHOLDER_SUBS[to_paramstyle]
    paramname_exp   = PARAMNAME_EXPS[from_paramstyle]
    new_query = query
    new_params = []
    param_num = 0
    for placeholder in placeholder_exp.findall(query):
        param_num += 1
        param_name = paramname_exp.findall(placeholder)[0]
        new_placeholder = placeholder_sub(param_num)
        new_query = string.replace(new_query, placeholder, new_placeholder, 1)
        new_params.append(params[param_name])
    return new_query, new_params


##
## Convert from a dictionary-based paramstyle to a dictionary-based paramstyle.
##
def dict_to_dict( from_paramstyle, to_paramstyle, query, params ):
    placeholder_exp = PLACEHOLDER_EXPS[from_paramstyle]
    placeholder_sub = PLACEHOLDER_SUBS[to_paramstyle]
    paramname_exp   = PARAMNAME_EXPS[from_paramstyle]
    new_query = query
    new_params = params
    param_num = 0
    for placeholder in placeholder_exp.findall(query):
        param_num += 1
        param_name = paramname_exp.findall(placeholder)[0]
        new_placeholder = placeholder_sub(param_num)
        new_query = string.replace(new_query, placeholder, new_placeholder, 1)
    return new_query, new_params


##
## Convert from any paramstyle to any other paramstyle.
##
def paramstyle_convert( from_paramstyle, to_paramstyle, query, params ):

    try:
        convert = CONVERSION_MATRIX[from_paramstyle][to_paramstyle]
    except KeyError:
        raise NotImplementedError, 'Unsupported paramstyle conversion: %s to %s' % (from_paramstyle, to_paramstyle)

    new_query, new_params = convert(query, params)

    return new_query, new_params

##
## Unit Tests
##
if __name__ == '__main__':
    sequence_params = ['a', 'b', 'c', 'd']
    dict_params = {
        'foo'  : 'a',
        'bar'  : 'b',
        'baz'  : 'c',
        'quux' : 'd',
    }
    tests = {
        'qmark'    : [ 'SELECT * FROM ? WHERE ? > ? OR ? IS NOT NULL', sequence_params ],
        'numeric'  : [ 'SELECT * FROM :1 WHERE :2 > :3 OR :4 IS NOT NULL', sequence_params ],
        'named'    : [ 'SELECT * FROM :foo WHERE :bar > :baz OR :quux IS NOT NULL', dict_params ],
        'format'   : [ 'SELECT * FROM %s WHERE %s > %s OR %s IS NOT NULL', sequence_params ],
        'pyformat' : [ 'SELECT * FROM %(foo)s WHERE %(bar)s > %(baz)s OR %(quux)s IS NOT NULL', dict_params ],
    }
    print ''
    print '[ PLACEHOLDER MATCH TESTS ]'
    print ''
    for paramstyle in tests.keys():
        query        = tests[paramstyle][0]
        regexp       = PLACEHOLDER_EXPS[paramstyle]
        print regexp.findall(query)
    indent = 4
    width = 16
    print ''
    print '[ TOKEN TO TOKEN TESTS ]'
    print ''
    for from_paramstyle in PARAMSTYLES['token']:
        from_query  = tests[from_paramstyle][0]
        from_params = tests[from_paramstyle][1]
        print "%s[ %s ] '%s' '%s'" % ( ' ' * indent, from_paramstyle, from_query, from_params )
        print ''
        for to_paramstyle in PARAMSTYLES['token']:
            to_query, to_params = sequence_to_sequence(from_paramstyle, to_paramstyle, from_query, from_params)
            print '%s%s%s: %s' % ( ' ' * indent * 2, to_paramstyle,  '.' * (width + indent - len(to_paramstyle)), to_query  )
            print '%s%s: %s' % ( ' ' * indent * 2, ' ' * (width + indent), to_params )
        print ''
    print ''
    print '[ SEQUENCE TO SEQUENCE TESTS ]'
    print ''
    for from_paramstyle in PARAMSTYLES['sequence']:
        from_query  = tests[from_paramstyle][0]
        from_params = tests[from_paramstyle][1]
        print "%s[ %s ] '%s' '%s'" % ( ' ' * indent, from_paramstyle, from_query, from_params )
        print ''
        for to_paramstyle in PARAMSTYLES['sequence']:
            to_query, to_params = sequence_to_sequence(from_paramstyle, to_paramstyle, from_query, from_params)
            print '%s%s%s: %s' % ( ' ' * indent * 2, to_paramstyle,  '.' * (width + indent - len(to_paramstyle)), to_query  )
            print '%s%s: %s' % ( ' ' * indent * 2, ' ' * (width + indent), to_params )
        print ''
    print ''
    print '[ SEQUENCE TO DICT TESTS ]'
    print ''
    for from_paramstyle in PARAMSTYLES['sequence']:
        from_query  = tests[from_paramstyle][0]
        from_params = tests[from_paramstyle][1]
        print "%s[ %s ] '%s' '%s'" % ( ' ' * indent, from_paramstyle, from_query, from_params )
        print ''
        for to_paramstyle in PARAMSTYLES['dict']:
            to_query, to_params = sequence_to_dict(from_paramstyle, to_paramstyle, from_query, from_params)
            print '%s%s%s: %s' % ( ' ' * indent * 2, to_paramstyle,  '.' * (width + indent - len(to_paramstyle)), to_query  )
            print '%s%s: %s' % ( ' ' * indent * 2, ' ' * (width + indent), to_params )
        print ''
    print ''
    print '[ DICT TO SEQUENCE TESTS ]'
    print ''
    for from_paramstyle in PARAMSTYLES['dict']:
        from_query  = tests[from_paramstyle][0]
        from_params = tests[from_paramstyle][1]
        print "%s[ %s ] '%s' '%s'" % ( ' ' * indent, from_paramstyle, from_query, from_params )
        print ''
        for to_paramstyle in PARAMSTYLES['sequence']:
            to_query, to_params = dict_to_sequence(from_paramstyle, to_paramstyle, from_query, from_params)
            print '%s%s%s: %s' % ( ' ' * indent * 2, to_paramstyle,  '.' * (width + indent - len(to_paramstyle)), to_query  )
            print '%s%s: %s' % ( ' ' * indent * 2, ' ' * (width + indent), to_params )
        print ''
    print ''
    print '[ PARAMSTYLE TRANSLATIONS ]'
    for from_paramstyle in PARAMSTYLES['all']:
        query  = tests[from_paramstyle][0]
        params = tests[from_paramstyle][1]
        print ''
        print '%s[ %s ]' % (' ' * indent, from_paramstyle.upper())
        print ''
        label = 'query'
        print '%s%s%s: %s' % (' ' * indent, label, '.' * (width + indent - len(label)), query)
        label = 'paramstyle'
        print '%s%s%s: %s' % (' ' * indent, label, '.' * (width + indent - len(label)), from_paramstyle)
        print ''
        for to_paramstyle in PARAMSTYLES['all']:
            converted_query, converted_params = paramstyle_convert(from_paramstyle, to_paramstyle, query, params)
            label = '%s_query' % (to_paramstyle)
            print '%s%s%s: %s' % (' ' * indent * 2, label, '.' * (width - len(label)), converted_query)
            label = '%s_params' % (to_paramstyle)
            print '%s%s%s: %s' % (' ' * indent * 2, label, '.' * (width - len(label)), converted_params)
        print ''

