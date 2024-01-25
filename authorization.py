from fastapi import FastAPI, HTTPException, Header, Depends

# Données utilisateurs et administrateurs
users = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}
admin = {"admin": "4dm1n"}

api = FastAPI()

### Fonction pour vérifier l'authentification avec type: user/admin

#Vérification de l'authentification
def check_auth_type(user_type = str):
    def check_auth(credentials: str = Header(alias="Authorization", description="Auth method and username:password")):
        if not credentials:
            raise HTTPException(status_code=411, detail="Authorization header missing")

        auth_type, user_pass = credentials.split(' ', 1)
        if auth_type != 'Basic':
            raise HTTPException(status_code=412, detail="Unsupported authentication method")

        username, password = user_pass.split(':', 1)

        #Si type user et credentials sont bien présents dans le distionnaire users
        if user_type == "user" and username in users and users[username] == password:
            return True
        #Si type admin et credentials correcpondent à l'admin
        elif user_type == "admin" and username in admin and admin[username] == password:
            return True
        else:
            raise HTTPException(status_code=413, detail="Invalid credentials")
    return check_auth
    

    
