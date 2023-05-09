#En vez de Importar el framework fastapi, importamos APIRouter a nuestro entorno de trabajo
from fastapi import APIRouter, HTTPException, status
#Invocamos la entidad que hemos creado ****nEw
from db.models.user import User
#Importamos la instancia que devolvera al usuario en formato user ***new
from db.schemas.user import user_schema
#Importamos nuestro cliente para poder agregar usuarios a la db****nEw
from db.Client_9 import db_client
from bson import ObjectId
#Creamos un objeto a partir de la clase FastAPI
router= APIRouter()

#*****************************GET*********************
@router.get("/userdb/", response_model=list[User], status_code=status.HTTP_200_OK)
async def users():
    users_list= user_schema(db_client.computacion.ModelosWEB.find())
    return (users_list)
 # En el explorador colocamos la raiz de la ip: http://127.0.0.1:8000/usersclass/


#***Get con Filtro Path
@router.get("/userdb/{id}", status_code=status.HTTP_200_OK)
async def user(id: str):
    
    user_found= search_user_error("_id", ObjectId(id))
    
    if not user_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe")
    else:
        return search_user_error("_id", ObjectId(id))
 
#************************************POST*********************************
@router.post("/userdb/",response_model=User, status_code=201)
async def create_user(user:User):
    if type(search_user("NOMBRE", user.NOMBRE)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    #2Transformo mi entidad user en un diccionario. Transformo User en diccionario
    user_dict= dict (user) ## Se crea una variable llamada dict, donde se va a transformar el user a un DICCIONARIO
    del user_dict["id"]#Elimino id del diccionario
    #1 Creo un esquema que se llama usuarios dentro de Computacion
    #Computación= Base de datos
    #users= Colección
    id= db_client.Computacion.ModelosWEB.insert_one(user_dict).inserted_id
    
    #Consultamos el user insertado en la bd con todo y id asignado automaticamente
    #Me devuelve un JSON hay que convertirlo a un objeto tipo User (user.py en schemas)
    new_user=  user_schema(db_client.Computacion.ModelosWEB.find_one({"_id":id}))
    #La base de datos devuelve un JSON debemos transformarlo a un objeto tipo user:
    return User(**new_user)
    #http://127.0.0.1:8000/userdb/
   
   
    #*********************PUT*******************************
@router.put("/userdb/{id}", response_model=User, status_code=status.HTTP_202_ACCEPTED)
async def search_user(user: User, id: str):
    user_dict= dict(user)
    del user_dict["id"]
    
    try:
        db_client.Computacion.ModelosWEB.find_one_and_replace({"_id":ObjectId(user.id)}, user_dict)
    except:
        return {"Error":"Actualizacion fallida"}
    
    return search_user("_id", ObjectId(id))

        
#******************DELETE****************************************************
@router.delete("/userdb/{id}")
async def delete_user(id:str):
    found = db_client.Computacion.ModelosWEB.delete_one({"_id": ObjectId(id)})
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe *_*")
    else:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="Eliminado Correctamente :)")
        
#--------------------------------------------------------
        
def search_user(field: str, key):
    try:
        user_find = db_client.Computacion.ModelosWEB.find_one({field: key})
        return User (**user_schema(user_find))
    except:
        return {"Error": "Usuario no encontrado"}

def search_user_error(field: str, key):
    try:
        user_find = db_client.Computacion.ModelosWEB.find_one({field: key})
        return User (**user_schema(user_find))
    except:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="El usuario no existe")


def search_user_error_2(field: str, key):
    try:
        user_find = db_client.Computacion.ModelosWEB.find_one({field: key})
        return User (**user_schema(user_find))
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe")

