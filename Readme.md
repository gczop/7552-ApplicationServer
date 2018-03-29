7552 - Application server

Para ejecutarlo correr el comando: "source env/bin/activate".

Al hacerlo deberia aparecer "(env)" al comienzo de la linea en la terminal.

Una vez que el ambiente virtual esta activado correr el script con el comando: "python app2.py".

API APP SERVER

/App:
	
	/users:
	⁃	GET: Login de Usuarios.  In: User, Password | Out: Token
	⁃	PUT: Creacion de Usuarios. In: Mail, Password | Out: Token

	/relation:
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

	/messages:

	
Bases de Datos en App server

Puntos a resolver: 
	•	Autenticacion.


