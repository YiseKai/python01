#!/usr/bin/env python

#Incluir los archivos de cabecera
import twitter
import urllib2 
import io
import json
import time


#Iniciar sesion
#Boot es variable global de la aplicacion
#postcondicion: creacion de un objeto boot de la API de Twitter

CONSUMER_KEY = 'YoRulp1bpZyWPiONmQfoRhPPJ'
CONSUMER_SECRET = 'uvTy5TwzRU69mKDOTQLHI4nJU4nFZ4ujp8QzjYcKNdiaa5fFiy'
OAUTH_TOKEN = '3235938934-SgpruAx6V1pzfuc9FN9WiaZF4rCQS9vt3KtcEpB'
OAUTH_TOKEN_SECRET = 'jpG3I9h9wS8Kf0Vy6EiVT4JgNGHGS3fQi8Sh69AjdviZM'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,CONSUMER_KEY, CONSUMER_SECRET)
boot = twitter.Twitter(auth = auth)
#Funcion: leer_mencion
#Precondicion: Se ha creado un objeto de tipo Twitter
#Postcondicion: Devuelve una variable con el contenido de la mencion

def leer_mencion():
	return boot.statuses.mentions_timeline(count = 1)


#Funcion: guardar_json
#Precondicion: Recibe como parametro el nombre del archivo y su objeto
#Postcondicion: Guarda un archivo de tipo .json a modo local

def guardar_json(filename,data):
	with io.open('{0}.json'.format(filename), 'w', encoding='utf-8') as f:
		f.write(unicode(json.dumps(data, ensure_ascii = False)))

#Funcion: leer_json
#Precondicion: Recibe como parametro el nombre del archivo guardado de forma local
#Postcondicion: devuelve la lectura de dicho archivo

def leer_json(filename):
	return json.loads(open(filename).read())




#Funcion: formatear_ciudad
#Precondicion: recibe como parametro un String de la lectura de la mencion
#Postcondicion: Remplaza los espacios por guiones bajos y devuelve el String
def formatear_ciudad(ciudad):
	return ciudad.replace(' ', '_')

#Funcion: peticion_weather
#Precondicion: recibe la ciudad sobre la que hacer la consulta
#Postcondicion: devuelve la lectura de la web originada
def peticion_weather(nombre):
	web = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+nombre+',ES')
	data = json.load(web)
	return data

#Funcion: crear_tweet
#Precondicion: Recibe la lectura de la Web en formato JSON
#Postcondicion: Se crea unos String que se almacenan en una lista de tipo global
def crear_tweet(web,usuario):
	for webi in web['weather']:
		estado = webi['main']
	temperatura = web['main']['temp'] - 273.15
	viento = web['wind']['speed']
	nombre = web['name']
	cadena = usuario+" Ciudad: "+nombre+"\nEstado: "+estado+"\nTemperatura: "+str(temperatura)+"\nViento: "+str(viento)
	publicar_tweet(cadena)

	

#Funcion: publicar_tweet
#Precondicion: Recibe por parametros la lista de los campos que introduciremos en el tweet y al usuario que se lo enviamos
#Postcondicion: Publica en la red social Twitter la respuesta a nuestra peticion.
def publicar_tweet(cadena):
	boot.statuses.update(status = cadena)
	print "Publicado con exito"

def inicio_rec(palabra_antigua,usuario_antiguo):
	mencion = leer_mencion()
	guardar_json('tweet_json', mencion)
	tweet_json = leer_json('tweet_json.json')
	for tweety in tweet_json:
		palabra = tweety[ 'text' ]
		user = tweety[ 'user' ]['screen_name']
	palabra = palabra[14:]
	user = "@"+user
	if(palabra_antigua != palabra or usuario_antiguo != user):
		print "El antiguo fue: "+usuario_antiguo+" y pidio: "+palabra_antigua
		print "El usuario: "+user+" hace la siguiente peticion: "+palabra
		palabra = formatear_ciudad(palabra)
		web_json = peticion_weather(palabra)
		crear_tweet(web_json,user)
		inicio_rec(palabra,user)
		
def inicio():
	mencion = leer_mencion()
	guardar_json('tweet_json', mencion)
	tweet_json = leer_json('tweet_json.json')
	for tweety in tweet_json:
		palabra = tweety[ 'text' ]
		user = tweety[ 'user' ]['screen_name']
	palabra = palabra[14:]
	user = "@"+user
	palabra = formatear_ciudad(palabra)
	web_json = peticion_weather(palabra)
	crear_tweet(web_json,user)
	inicio_rec(palabra,user)


while True: 
	inicio()
	time.sleep(30) # Delay for 1 minute (60 seconds)
