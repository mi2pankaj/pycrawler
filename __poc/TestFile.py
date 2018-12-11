from builtins import str


import urllib3
from __crawler import utills
import csv


a = 1;


# m1 = {'http://www.lenskart.com/opensearch.xml': 200, 'https://www.lenskart.com/opensearch.xml': 200, 'https://store.lenskart.com/xmlrpc.php': 405, 'http://blog.lenskart.com/high-five-top-sunglasses-to-posses-this-spring-summer/amp/': 404, 'http://blog.lenskart.com/6-sunglasses-you-must-own/amp/': 404, 'http://www.lenskart.com/contact-lenses/': 200, 'http://blog.lenskart.com/too-good-to-be-free/amp/': 404, 'http://www.lenskart.com/catalogsearch/result/?cat=0&amp;q=oversized+sunglasses#cat=0&amp;q=oversized+sunglasses&amp;oos_searchable=Yes&amp;gan_data=true': 520, 'http://blog.lenskart.com/breaking-down-the-eyewear-stereotypes/amp/': 404, 'http://www.lenskart.com/sunglasses-home.html': 200, 'http://www.lenskart.com/contact-lens-home.html': 200, 'http://blog.lenskart.com/oh-my-star-whats-on-your-eyes/amp/': 404, 'http://www.lenskart.com/eyeglasses-home.html': 200, 'http://www.lenskart.com/catalogsearch/result/?cat=0&amp;q=wooden+wayfarer': 404, 'http://www.lenskart.com/catalogsearch/result/?cat=0&amp;q=golden+rim#cat=0&amp;q=golden+rim&amp;oos_searchable=Yes&amp;gan_data=true': 404, 'http://www.lenskart.com/referralcopy.html': 200, 'http://blog.lenskart.com/a-flash-of-glitz-and-glory-vincent-chase-reflectors/amp/': 404, 'http://www.lenskart.com/catalogsearch/result/?cat=0&amp;q=Tortoise+sunglasses#cat=0&amp;q=Tortoise+sunglasses&amp;oos_searchable=Yes&amp;gan_data=true': 504, 'http://articles.lenskart.com/xmlrpc.php': 405, "http://www.lenskart.com/catalogsearch/result/?cat=0&amp;q=aviator+men%27s+mirror+sunglasses&amp;oos_searchable=Yes#cat=0&amp;q=aviator+men's+mirror+sunglasses&amp;gan_data=true": 504, 'http://www.lenskart.com/catalogsearch/result/?cat=0&amp;q=oversized#cat=0&amp;q=oversized&amp;oos_searchable=Yes&amp;gan_data=true': 404, 'http://www.lenskart.com/american-optical-lenses.html': 404, 'https://www.lenskart.com/eyeglasses-home.html': 200, 'http://www.lenskart.com/catalogsearch/result/?cat=0&amp;q=aviator+polaroid#cat=0&amp;q=aviator+polaroid&amp;oos_searchable=Yes&amp;gan_data=true': 404, 'http://www.lenskart.com/kodak-lenses.html': 200, 'http://www.lenskart.com/klar-lenses.html': 200, 'http://www.lenskart.com/faq/Prescription-Sunglasses': 200, 'http://www.lenskart.com/catalogsearch/result/?cat=0&amp;q=vincent+chase+wayfarer#cat=0&amp;q=vincent+chase+wayfarer&amp;oos_searchable=Yes&amp;gan_data=true': 404, 'https://www.lenskart.com/mauijimdescription': 200, 'http://lenskartblog.tumblr.com/': 404, 'http://www.lenskart.com/eyeglasses/round.html': 200, 'http://store.lenskart.com/xmlrpc.php': 405, 'http://lenskart.webs.com/': 410, 'http://www.lenskart.com/catalogsearch/result/?cat=0&amp;q=carrera+sunglasses#cat=0&amp;q=carrera+sunglasses&amp;oos_searchable=Yes&amp;gan_data=true': 520, 'http://www.lenskart.com/christmas-newyear-offer.html': 200, 'http://www.lenskart.com/catalogsearch/result/?cat=0&amp;q=wayfarer+glasses#cat=0&amp;q=wayfarer+glasses&amp;c2c_gender=10529&amp;gan_data=true': 404, 'http://www.lenskart.com/fathers-day-offers-2014': 200, 'http://www.lenskart.com/catalogsearch/result/?cat=0&amp;q=tortoise#cat=0&amp;q=tortoise&amp;oos_searchable=Yes&amp;gan_data=true': 404, 'http://www.lenskart.com/catalogsearch/result/?cat=0&amp;q=ray+ban#cat=0&amp;q=ray+ban&amp;oos_searchable=Yes&amp;gan_data=true': 404, 'http://www.lenskart.com/catalogsearch/result/?cat=0&amp;q=tortoise+sunglasses#cat=0&amp;q=tortoise+sunglasses&amp;c2c_gender=10529&amp;c2c_frametype=11370&amp;c2c_frame_size=11340&amp;gan_data=true': 504, 'http://www.lenskart.com/catalogsearch/result/?cat=0&amp;q=Tommy+Hilfiger#cat=0&amp;q=Tommy+Hilfiger&amp;oos_searchable=Yes&amp;gan_data=true': 404, 'http://www.lenskart.com/catalogsearch/result/?cat=0&amp;q=oversize+sunglasses#cat=0&amp;q=oversize+sunglasses&amp;oos_searchable=Yes&amp;gan_data=true': 504}
# for k,v in m1.items():
#     if(v==200):
#         v=str('DAMN')
#     print(v)

pap={}
pap.update({'a':'b'})
pap.update({'aaa':'aaaanh'})

print(pap)

if pap.get('a') == None:
    print(True)

pap = [{'URL': 'abc.com', 'Status_Code':'200'}, {'URL': 'abc.com', 'Status_Code':'200'}]

'write damn page in csv '
with open('BrokenUrls.csv', mode='w') as csv_file:
    fieldnames = ['URL', 'Status_Code']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    for dat in list(pap):                
        writer.writerow(dat)
#         writer.writerow({'emp_name': 'Erica Meyers', 'dept': 'IT', 'birth_month': 'March'})


pap = {'URL_Found': 'abc.com', 'Status_Found':'200', 'Status_Code':'777'}

with open('BrokenUrls11.csv', mode='w') as csv_file:
    writer = csv.writer(csv_file)
    for k,v in pap.items():                
        writer.writerow([k,v])
        writer.writerow('')

    
a = 'ABC'
if(a.lower().endswith('c')):
    print('sss')
    

http = urllib3.PoolManager()
url = 'http://www.thefamouspeople.com/singers.php'
response = http.request('GET', url)
print(response.data)
print(response.status)
    
m1 = {'1':'2', '11':'22'}
print(m1.get('1'))
print(m1.get('13'))

if((m1.get('13') == None) ):
    print('huhuaa') 

url = '#'
if ( (not(url.startswith('http'))) & (not(utills.GenericMethods().ifLenskartDomain(url)))):
    print('remove')
else:
    print('===== > updating url in glbal map '+url)



url = str(' https://www.lenskart.com/contact-lenses/top-contact-lenses-brands/glamour-eye-contact-lenses.html')

url1 = url[url.find('//')+2:]
url2 = url1[:url1.find('/')]

print('==> ' +url2)

abc ='lenskart.com'
a = abc.find('lenskart')
print(a)
    
map11 = {}
   
map11.update({'1':'2'})
map11.update({'111':'2'})

print(map11)
   
while(a < 10):
        print(a)
        a = a + 1
        if(a == 7 | a < 10):
            print('Breaking Code Now : ', a)
            break

a='1234'
b='abcd'
if(b.__contains__(a)):
    print('yeah')
 

def function1():
    for letter in 'Python Is Good':
        print('Current Letter: ', letter)
        if(letter == ' '):
            print('Breaking With Space : ', letter)
            break
        
function1();
##sys.exit()

## Get user input
# str=raw_input('Enter Pankaj')
# print ('print', str)


def assertMethod(abc):
    assert(abc == 'Pankaj')
    print('Assert...')
    return 'Assert Completed'

# assertMethod(str);

## Get exception
def getException(number):
    try:
        number / 0;
    except Exception:
        print('Exception')
    
getException(11);



