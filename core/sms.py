import sys, requests, urllib.parse, math, random, string

apikey = '9675e543f2b75cfcdfdb7c4ae4f1545c'
#46d37c2b31294928c6c046424ee324aa
#1f20d54e5a2be69af7ba00f5530fa359
sendername = ''

def send_message(message, number):
	print ('Sending Message...')
	params = (
		('apikey', apikey),
		('sendername', sendername),
		('message', message),
		('number', number),
	)
	path = 'https://semaphore.co/api/v4/otp?' + urllib.parse.urlencode(params)
	requests.post(path)
	print (path, params, 'Message Sent!')

if __name__ == '__main__':
	message = sys.argv[1]
	number = sys.argv[2]
	send_message(message, number)

def rand_pass(size): 	
	generate_pass = ''.join([random.choice( string.ascii_uppercase +
											string.ascii_lowercase +
											string.digits) 
											for n in range(size)]) 			
	return generate_pass 


