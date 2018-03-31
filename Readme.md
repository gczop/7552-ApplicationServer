+h7552 - Application server

Para ejecutarlo correr el comando: "source env/bin/activate".

Al hacerlo deberia aparecer "(env)" al comienzo de la linea en la terminal.

Una vez que el ambiente virtual esta activado correr el script con el comando: "python app2.py".

Las instrucciones de arriba ya estan agregadas en el Procfile que es lo que ejecuta Heroku al subir un nuevo push

Para correrlo en heroku de forma local:

$ pipenv --three
$ pipenv install
$ pipenv shell #Ahi se abre un shell que simula heroku

#Correrlo heroku local
$ heroku local web #Lo corre en localhost:5000

#Correrlo de forma local
$ source env/bin/activate
$ gunicorn wsgi

#Correrlo en heroku web
Fijarse si funciona con su cuenta de heroku, sino avisarme A MI (GUIDO PEIRANO)
Para correrlo en heroku hay que pushearlo al git de heroku
$ git push heroku master

Lo ideal seria fijarse si esta corriendo de forma correcta, para eso
$ heroku logs
Ahi fijarse que es lo que imprimer de app

Si no tira nada nuevo es porque los workers de heroku estan inactivos
$ heroku ps
Asi se fijan como estan los workers de heroku

$ heroku ps:scale web=1
Ahi prenden un worker de heroku



API APP SERVER

/App:
	
	/users/login:
	⁃	POST: Login de Usuarios.  In: LoginInfo| Out: Token Errores: 401 (Fallo login), 400 (Falta de parametros)

	/user/signup 
	⁃	POST: Creacion de Usuarios. In: LoginInfo| Out: Token

	/friends:
	⁃	GET: Conseguir todos los amigos de un Usuario. In: User Token | Out: Lista de amigos
	⁃	PUT: Agregar un amigo a un usuario. In: { Usr:Token de usuario, Friend: Usuario al cual se desea agregar} | Out: undefined
	⁃	DELETE: Permite eliminar a un usuario de tu lista de amigos. In: { Usr: Token de usuario, Friendo: Usuario al que se desea elminar}. Out: Undefined 

	/invitations:
	⁃	GET: Devuelve todas las invitaciones de amistad de un usuario. In: User Token | Out: Lista de invitaciones
	⁃	PUT: Acepta una invitacion de amistad determinada. In: { Usr: Token de usuario, Invitation: Invitacion especifica} | Out: undefined

	/people:
	⁃	GET: Encontrar usuarios a partir de un pedazo de informacion. In: Informacion de Usuario. Out: Lista de posibles matchs y su informacion
	
	/people/{id}:
	⁃	GET: Devuelve la informacion de un usuario especifico a partir de un Id. In: Id de usuario. Out: Id de usuario

	/notifications:
	⁃	GET: Devuelve todas las noticiaciones de un usuario. In: User Token. Out: Notificaciones de un usuario

	/profile:
	⁃	GET: Devuelve la informacion personal de un usuario. In: User Token. Out: Informacion de un usuario.
	⁃	POST: Permite agregar o modificar informacion de un usuario. In: Informacion del usuario vieja mas la deseada a agregar. Out: undefined

	/stories:
	⁃	GET: Devuelve todas las historias que deberia ver en el inicio el usuario. In: User Token. Out: Historias de inicio.
	⁃	PUT: Agrega una nueva historia a un usuario. In: {User:Token, Story: informacion necesaria de la story}. Out: Undefined.
	⁃	POST: Permite modificar informacion de una historia. In:{User: Token, Story: infromacion de la story}. Out: Undefined.
	⁃	DELETE: Permite borrar una stroy de un perfil. In:{User: Token, Story: Informacion de la story(id)}. Out: Undefined.
	
	/reactions:
	⁃	GET: Permite obtener todas las reacciones a una story determinada. In: {Usr: Token, Story: Informacion de la story(id)}. Out: Reacciones de la story.
	⁃	PUT: Permite reaccionar a una story determinada. In: {Usr: Token, Story: informacion de la story(id), Reaction: Reaccion}. Out: undefined.
	⁃	DELETE: Permite eliminar la reaccion a una story determinada. In: {Usr: Token, Story: Informacion de la story(id)}. Out: undefined

	/comments:
	⁃	GET: Permite obtener todas los comentarios a una story determinada. In: {Usr: Token, Story: Informacion de la story(id)}. Out: Comentarios de la story.
	⁃	PUT: Permite comentar una story determinada. In: {Usr: Token, Story: informacion de la story(id), Comment: Comentario}. Out: Id del comentario.
	⁃	DELETE: Permite eliminar el comentario a una story determinada. In: {Usr: Token, Story: Informacion de la story(id), Comment: Id del comentario}. Out: undefined


	/conversations:
	⁃	GET: Permite obtener todas las conversaciones que tiene un usuario. In: User Token. Out: Conversaciones del usuario.
	⁃	PUT: Permite crear una nueva conversacion con un usuario. In: {Usr: Token, Id: Destinatario}. Out: Id de la conversacion.

	/conversations/{id}:
	⁃	GET: Permite obtener una conversacion especifica de un usuario con otro. In:{Usr: token, Conversation: Id de la conversacion}. Out: Conversacion e informacion.
	⁃	PUT: Permite enviar un mensaje en una conversacion especifica. In:{Usr: token, Conversation: Id, Message: Mensaje}. Out: Undefined.
	⁃	DELET: Permite eliminar una conversacion. In:{Usr: Token, Conversation: Id}. Out: Undefined

	/ping:
	⁃	GET: Permite obtener el estado del servidor

	/stats:
	⁃	GET: Permite Obetener datos acerca del uso del application server


DEFINITIONS

LoginInfo = {
	user: user
	password: password
	fbToken: fbToken
}


Bases de Datos en App server
	Tentativa:
		Users: Aca metemos de todo, users y amigos

		Stories Largas: Metemos todo de las stories largas, reacciones comentarios etc etc

		Stories Rapidas: Metemos todo de las stories rapidas, reacciones comentarios etc etc
Puntos a resolver: 
	•	Autenticacion.




