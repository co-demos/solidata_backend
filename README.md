<div align=center> 
	<h2>an open source <br> authentication REST API microservice </h2>
	<!-- <h4>aka TokTok</h4> -->
</div>

---------

<h2 align=center>
	<img src="./static/logo_auth_microservice_300px.png">
</h2>

-------
## PRESENTATION

#### _TokTok_ is a microservice (a REST API) for users management and authentication based on access and refresh JSON Web Tokens (JWT)

- this auth server was extracted / insulated / forked / adapted from **[solidata_backend](https://github.com/entrepreneur-interet-general/solidata_backend)** project.
- compatible with the **TADATA!** sofware suite ( [ApiViz](https://github.com/co-demos/apiviz) / [Solidata_frontend](https://github.com/entrepreneur-interet-general/solidata_frontend) / [OpenScraper](https://github.com/entrepreneur-interet-general/OpenScraper) )



-------

## GOALS

- a simple server to manage users and authorizations based on JWT exchanges between client and server
- possibility to switch on/off some extra features as : RSA decryption/encryption, anonymous JWT, sending confirmation email

--------

## DEVELOPERS

- Hi! Nice to see you around :)
- Check also the **[`prod_snippets` folder](./prod_snippets)** if you encounter problems while installing locally or setting your server : [install mongodb](./prod_snippets/prod_mongodb.md), [set up supervisor](./prod_snippets/prod_supervisor.md), [set up git](./prod_snippets/prod_git.md), [set up nginx](./prod_snippets/prod_nginx.md), [set up ubuntu](./prod_snippets/prod_ubuntu.md)...
- If you want to contribute please check out our **[guidelines](./GUIDELINES_DEV.md)** first


------

## TECHNICAL POINTS

#### Tech stack
- _Language_  : **[Python 3.6](https://www.python.org/)**... praise be...
- _Framework_ : **[Flask](http://flask.pocoo.org/)**... minimalistic Python framework
- _API_       : **[Flask-RestPlus](http://flask-restplus.readthedocs.io/en/stable/)**... Swagger documentation integrated, praise be noirbizarre...
- _Security_  : **[Flask-JWT-extended](https://flask-jwt-extended.readthedocs.io/en/latest/)**... wrapper JWT for Flask
- _Emailing_  : **[Flask-email](https://pythonhosted.org/Flask-Mail/)**... templating, sending, etc...
- and more...

#### Features :

- JWT (JSON Web Tokens) :
	- access and refresh token for security over all the app
- RSA encryption (optionnal)
	- RSA encryption : server can send to the client a RSA public key for encryption client-side
	- RSA decryption : server can decode forms (login/register) encoded client-side with the RSA public key

- Users management :
	- login / register user 
	- anonymous login (optionnal) : sends a JWT for an anonymous use. Can be expected by server for routes with `@anonymous_required` decorator like `/login` or `/register`
	- confirm email (optionnal in dev mode): confirm user by sending a confirmation link (protected) in an email 
	- password forgotten by sending a link (protected) in an email with redirection to new password form 
	- reset password from client interface (protected) ...
	s
- Documentation 
	- on all API endpoints with Swagger (and some patience from the developers)

##### Features TO DO  :
- user : 
	- edit user (working on)
	- edit email (protect email update)


-------

## INSTALLATION WALKTHROUGH 

### _LOCALLY_

- clone / fork the depo 

	```bash 
	git clone https://github.com/co-demos/toktok.git
	```

- create a virtual environment for Python3
	
	```bash
	python3 -m venv venv
	source venv/bin/activate
	pip install --upgrade pip
	pip install -r requirements.txt
	```

- **optionnal** : create a secret config_file `config_prod.py` in the folder `./auth_api` based 

	```bash
	cp ./auth_api/config_prod_example.py ./auth_api/config_prod.py
	nano ./auth_api/config_prod.py 
	```

- pay attention at the MONGO_URI variable depending on your local mongodb configuration...
	- The following is the standard URI connection scheme (from [mongo documentation](https://docs.mongodb.com/manual/reference/connection-string/)):
		```bash
		mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
		```

- run the app in itts default mode (without possibility to send email) :

	```bash
	python appserver.py
	``` 

- test the following urls :
	
	```
	http://localhost:4100/api/auth/documentation
	http://localhost:4100/api/usr/documentation
	```

- once you stop the app if no longer needed deactivate your virtual environment

	```bash
	deactivate
	```

### _CLI OPTIONS_

There are some options you can play with while running the service :
- **`--mode`** : `dev` (default), `dev_email`, `preprod`, `production`
- **`--host`** : the IP of your server (default : `localhost`)
- **`--port`** : the port you want to run the app on (default : `4100`)
- **`--rsa`** : if you want receive the forms RSA encrypted and send the RSA public key (default : `no`)... protects the `/login` + `/register` +  `/password_forgotten` + `/reset_password` endpoints
- **`--anojwt`** : if you need to check the presence/validity of an "anonymous_jwt" in the request (default : `no`)... protects the `/login` + `/register` +  `/password_forgotten`  endpoints
- **`--antispam`** : if you need to check the presence/validity" in the request (default : `no`)... protects at the `/login` + `/register` + `/password_forgotten` endpoints
- **`--antispam_val`** : if you need to check the validity of the content of the `antispam` field in the form sent by the client (default : "")

In practice : 

- you can run the app in dev mode (with possibility to send email) : 

	```bash
	python appserver.py --mode=dev_email
	``` 

- you can choose to deactivate the integrated RSA decryption in the `/login` and `/register` endpoints

	```bash
	python appserver.py --rsa=no
	``` 

- you can choose to activate the check for an anonymous JWT in the `/login` and `/register` endpoints

	```bash
	python appserver.py --anojwt=yes
	``` 

- you can choose to activate the antispam in the `/login` and `/register` endpoints

	```bash
	python appserver.py --antispam=yes --antispam_val=my-value
	``` 

- you can add up those options in the command line
	```bash
	python appserver.py --anojwt=no --rsa=yes --mode=dev_email --antispam=yes
	``` 

### _PRODUCTION_

- for now we are using the following configuration

	- droplet in digitalocean.com
	- ubuntu 18.04
	- 3Go RAM / 2CPU
	- 60Go memory

- configure your server (user, firewall...): 
	- cf : [ docs 1 ](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04) 
	- cf : [ docs 2 ](https://www.digitalocean.com/community/tutorials/how-to-setup-a-firewall-with-ufw-on-an-ubuntu-and-debian-cloud-server) 
	- cf : [ docs 3 ](https://scottlinux.com/2011/10/10/ufw-allow-from-specific-ip-on-specific-port/ )

- install mongodb : 
	- cf : [ docs 1 ](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)
	- cf : [ docs 2 ](https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-18-04)	
	- cf : [ docs 3 ](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-mongodb-on-ubuntu-16-04#part-two-securing-mongodb) 
	- cf : [ docs 4 ](https://www.tecmint.com/install-mongodb-on-ubuntu-18-04/ )


- install nginx : 
	- cf : [ docs 1 ](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04)
	- cf :[ docs 2](https://linuxize.com/post/how-to-install-nginx-on-ubuntu-18-04/)
	- cf : [ docs 3 ](https://linuxize.com/post/how-to-set-up-nginx-server-blocks-on-ubuntu-18-04/ )


- install git on your server
	- cf : [ docs 1 ](https://www.digitalocean.com/community/tutorials/how-to-install-git-on-ubuntu-18-04)	- basically : 
		```bash
		sudo apt-get update
		sudo apt-get install git
		git --version
		```
	- go to your directory and init git :
		```
		git init . 
		git remote add origin https://github.com/co-demos/toktok.git
		git pull origin master
		```

- same steps than for local installation (virtual env, install dependencies, config_prod.py file, ) ... 

- test to run the app in production mode (with possibility to send email) : 

	```bash 
	python appserver.py --mode=production
	``` 

- it is then necessary to set up some service on the server to run the app as daemon. You could use `supervisor` for instance (check our [snippets and walkthrough here](./prod_snippets/prod_supervisor.md))

------

## INSPIRATIONS / BENCHMARK

- not finding a simple enough open source solution resolving the following problem : having a third party service (on a distant server) able to serve reasonnably secure tokens and manage users, so to avoid to build/re-invent a custom authentication for login/register every time we work on an app... 
- more, be able to share user/credentials between multiple services 
- we looked at [Oauth2.0](https://oauth.net/2/) (but doesn't manage users per say), meteor-password (but dialog with websocket)...


-------

## CREDITS 

#### TokTok's team thanks :

- the [SocialConnect](https://entrepreneur-interet-general.etalab.gouv.fr/defi/2017/09/26/socialconnect/) project, aka "Carrefour des Innovations Sociales"
- the [EIG](https://entrepreneur-interet-general.etalab.gouv.fr/) program by [Etalab](https://www.etalab.gouv.fr/)
- the [CGET](http://www.cget.gouv.fr/)
- [Guillaume Lancrenon](https://github.com/guillim)

#### Contacts - maintainance :

- [Julien Paris](<mailto:codemos.infos@gmail.com>), developer (aka [JPy](https://twitter.com/jparis_py) on Twitter)

-------

## SCREENSHOTS

-------
![alt text](./screenshots/endpoints_users.png "endpoint users")

-------
![alt text](./screenshots/endpoints_auth_server.png "endpoint auth users")



