from sendwithus import SWUAPI

a = SWUAPI('68c9f6ccd3aa206362640c7fa9be236d4e0dd837', 
        DEBUG=True,
        API_PROTO='http',
        API_HOST='localhost:8000')
        #API_HOST='betawithus.herokuapp.com')

print '\t\tSend'
print '\t\tWith'
print '\t\t Us '
print '\n\n'

print '\t 1 > Testing Send'

try:
    a.send('good', 'matt@sendwithus.com', data={'name': 'Jimmy'})
except Exception as e:
    print ' => FAILED'
    print ' |\t%s' % e
    print ' \\\t Exiting, Goodbye!'
    exit()

print '\t   > Passed!'

