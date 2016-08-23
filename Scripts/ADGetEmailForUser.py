# Optional arguments and default values
attrs = 'name,displayname,mail'
if demisto.get(demisto.args(), 'attributes'):
    attrs += "," + demisto.args()['attributes']

memberDN = ''
if demisto.get(demisto.args(), 'dn'):
    memberDN = demisto.args()['dn']
elif demisto.get(demisto.args(), 'name'):
    resp = demisto.executeCommand( 'ad-search', { 'filter' : "(&(objectClass=User)(name=" + demisto.args()['name'] + "))" } )
    if type(resp)==list and len(resp)==1 and type(resp[0])==dict and 'Contents' in resp[0] and type(resp[0]['Contents'])==list and len(resp[0]['Contents'])==1 and type(resp[0]['Contents'][0])==dict and 'dn' in resp[0]['Contents'][0]:
        memberDN = resp[0]['Contents'][0]['dn']
    else:
        demisto.results( resp )
        sys.exit(0)
else:
    demisto.results( { 'Type' : entryTypes['error'], 'ContentsFormat' : formats['text'], 'Contents' : 'You must provide either dn or name as argument!' } )
    sys.exit(0)

if memberDN:
    filterstr = r"(&(objectClass=User)(distinguishedName=" + memberDN + "))"
    demisto.results( demisto.executeCommand( 'ad-search' , { 'filter' : filterstr, 'attributes' : attrs } ) )
else:
    demisto.results( { 'Type' : entryTypes['error'], 'ContentsFormat' : formats['text'], 'Contents' : 'User not found.' } )