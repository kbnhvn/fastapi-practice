from fastapi import FastAPI, HTTPException, Query, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import random

#Import modules 
from data_operations import load_csv_data, add_data_to_csv, filter_uses, filter_subjects_by_use, filter_questions_by_use, filter_questions_by_subjects
from authorization import check_auth_type

#Import de la fonction permettant de charger le csv
file_path='questions.csv'
csv_data=load_csv_data(file_path)

description= """
## Features

### Users
- Read all questions
- Read all uses
- Read all subjects associated with a use 
- Generate a QCM by chosing a use and subjects

### Admin
- Add a new question

**This API is protected, so you will need to check authorization by adding auth method and credentials as header parameters, for each route**

#### Tools
- Check the health and functionality of the API

"""

api = FastAPI(
    title='My API - QCM',
    summary="This API allow you to generate QCM by chosing a use and subjects, and create a random list of questions.",
    description=description,
    contact={
        "name": "Joel LOURENCO",
        "email": "joel.lourenco.pro@gmail.com",
    },
)

## ------- Gestion des exceptions
@api.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

@api.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )

@api.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"}
    )

#### -------------------------------- ####
#### ------------ ROUTES ------------ ####
#### -------------------------------- ####

### ------ Routes GET

# ---- Affichage des données complètes

#Documentatiopn des status_code
responses = {
    200: {"description": "OK"},
    411: {"description": "Authorization header missing"},
    412: {"description": "Unsupported authentication method"},
    413: {"description": "Invalid credentials"},
    500: {"description": "Internal server error"},
}

@api.get('/', name='Get all questions', tags=['Users'], responses=responses)
#La vérification du type d'user et les identifiants est réalisée par la dépendance check_auth_type()
def get_questions(authentified: str = Depends(check_auth_type("user"))):
    """
    Display all datas

    * **This is a protected route, so you will need to check authorization by adding auth method and credentials as header parameters**
    """
    #Si l'user est bien authentifié, sinon il retourne les erreurs spécifiques à la dépendance
    if authentified:
        try:
            return {'data': csv_data}
        except Exception :
            raise HTTPException(status_code=500, detail="Internal Server Error")

# ---- Permet d'obtenir les différentes valeurs (uniques) de types de QCM
        
#Documentation des status_code
responses = {
    200: {"description": "OK"},
    411: {"description": "Authorization header missing"},
    412: {"description": "Unsupported authentication method"},
    413: {"description": "Invalid credentials"},
    500: {"description": "Internal server error"},
}

@api.get('/use', name='Get uses', tags=['Users'], responses=responses)
#La vérificatiion du type d'user et les identifiants est réalisée par la dépendance check_auth_type()
def get_uses(authentified: str = Depends(check_auth_type("user"))):
    """
    Get use values

    * **This is a protected route, so you will need to check authorization by adding auth method and credentials as header parameters**
    """
    #Si l'user est bien authentifié, sinon il retourne les erreurs spécifiques à la dépendance
    if authentified:
        try:
            return {'uses': filter_uses(csv_data)}
        except Exception :
            raise HTTPException(status_code=500, detail="Internal Server Error")       


# ---- Permet d'obtenir les différentes valeurs (uniques) de catégories pour un type donné
        
#Documentatiopn des status_code
responses = {
    200: {"description": "OK"},
    404: {"description": "Item not found"},
    411: {"description": "Authorization header missing"},
    412: {"description": "Unsupported authentication method"},
    413: {"description": "Invalid credentials"},
    500: {"description": "Internal server error"},
}
        
@api.get('/subjects', name='Get subjects by use', tags=['Users'], responses=responses)
#La vérificatiion du type d'user et les identifiants est réalisée par la dépendance check_auth_type()
def get_subjects(use: str, authentified: str = Depends(check_auth_type("user"))):
    """
    Get subjects by use :
    * Add a use name as query parameter to display all subjects related to this use

    * **This is a protected route, so you will need to check authorization by adding auth method and credentials as header parameters**
    """
    #Si l'user est bien authentifié, sinon il retourne les erreurs spécifiques à la dépendance
    if authentified:
        try:
            list_subjects = filter_subjects_by_use(csv_data,use)
            if not list_subjects:
                raise HTTPException(status_code=404, detail="Use not found")
            return {'subjects': list_subjects}
        
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        except HTTPException as err:
            raise err
        except Exception as err:
            raise HTTPException(status_code=500, detail="Internal Server Error")

## ------- Génération d'un QCM ----- ##

#Documentatiopn des status_code
responses = {
    200: {"description": "OK"},
    404: {"description": "Item not found"},
    405: {"description": "Number of questions not valid"},
    406: {"description": "Not enough questions on selected subjects"},
    411: {"description": "Authorization header missing"},
    412: {"description": "Unsupported authentication method"},
    413: {"description": "Invalid credentials"},
    500: {"description": "Internal server error"},
}

@api.get('/test', name='Generate a test', tags=['Users'], responses=responses)
#La vérificatiion du type d'user et les identifiants est réalisée par la dépendance check_auth_type()
def get_test(use: str, nbr_questions: int, subjects: List[str] = Query(), authentified: str = Depends(check_auth_type("user"))):
    """Generate a test :
    * Add a use name
    * Add a number of questions (5, 10 or 20)
    * Add subjects ((multiple can be added) related to chosen use

    * **This is a protected route, so you will need to check authorization by adding auth method and credentials as header parameters**

    """
    #Si l'user est bien authentifié, sinon il retourne les erreurs spécifiques à la dépendance
    if authentified:
        try:
            #Validation du type
            if use not in filter_uses(csv_data):
                raise HTTPException(status_code=404, detail="Use {} not found".format(use))

            #Récupération des questions pour le type donné
            list_questions=filter_questions_by_use(csv_data, use)

            #Validation des catégories
            valid_subjects = {element.get('subject') for element in list_questions}
            for subject in subjects:
                if subject not in valid_subjects:
                    raise HTTPException(status_code=404, detail="Subject '{}' not found".format(subject))

            #Récupération des questions pour les catégories données
            filtered_questions=filter_questions_by_subjects(list_questions, subjects)

            #Validation du nombre de questions
            possible_questions_number=[5,10,20]
            if nbr_questions not in possible_questions_number:
                raise HTTPException(status_code=405, detail="Number of questions must be 5, 10 or 20")
            
            test=[]

            #Vérification du nombre de questions et randomisation
            if len(filtered_questions) <= nbr_questions:
                raise HTTPException(status_code=406, detail="Not enough questions on selected subjects. Add Another subject or lower the number of questions.")  
            else:
                ##Génération du test aléatoire avec le nombre d'éléments donnés
                test = random.sample(filtered_questions, nbr_questions)

            return {'test': test}
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        except HTTPException as err:
            raise err
        except Exception as err:
            raise HTTPException(status_code=500, detail="Internal Server Error")
        

### ------ Route POST
        

## ------ Classe Question

class Question(BaseModel):
    """
        A question in the pool
    """
    question: str=""
    subject: str=""
    use: str=""
    correct: str=""
    responseA: str=""
    responseB: str=""
    responseC: str=""
    responseD: Optional[str]=""
    remark: Optional[str]=""
        
## ------ Ajout d'une nouvelle question
    
responses = {
    200: {"description": "OK"},
    400: {"description": "Bad type"},
    407: {"description": "Element is missing"},
    408: {"description": "Bad value"},
    411: {"description": "Authorization header missing"},
    412: {"description": "Unsupported authentication method"},
    413: {"description": "Invalid credentials"},
    500: {"description": "Internal server error"},
}

@api.post('/new_question', name='Add a new question', tags=['Admin'], responses=responses)
def add_question(question: Question, authentified: str = Depends(check_auth_type("admin"))):
    """Add a new question :
    * Add the **question**
    * Add the **subject** of this question
    * Add the **use** of this question
    * Add the **correct answer (A, B, C or D)**
    * Add the **answer A**
    * Add the **answer B**
    * Add the **answer C**
    * Add the answer D (_optional_)
    * Add a remark (_optional_)

    * **This is a protected route, so you will need to check authorization by adding auth method and credentials as header parameters**

    """
    #Si l'admin est bien authentifié, sinon il retourne les erreurs spécifiques à la dépendance
    if authentified:
        try:
            ##Vérification des valeurs :
            if question.question == "":
                raise HTTPException(status_code=407, detail="Question is blank, you must type a question.")
            elif question.subject == "":
                raise HTTPException(status_code=407, detail="Subject is blank, you must type a subject.")
            elif question.use == "":
                raise HTTPException(status_code=407, detail="Use is blank, you must type a use.")
            elif question.correct not in ["A","B","C","D"]:
                raise HTTPException(status_code=408, detail="Correct answer must be A,B,C or D.")
            elif question.responseA == "":
                raise HTTPException(status_code=407, detail="Response A is blank, you must type response A.")
            elif question.responseB == "":
                raise HTTPException(status_code=407, detail="Response B is blank, you must type response B.")
            elif question.responseC == "":
                raise HTTPException(status_code=407, detail="Response C is blank, you must type response C.")
            elif question.responseD == "" and question.correct == "D":
                raise HTTPException(status_code=407, detail="Response D is blank, you must type response D or chose an other correct response.")
            else:
                #Ajout de la question à la liste
                csv_data.append(question)

                #Ajout de la question au fichier csv
                add_data_to_csv(file_path, question)

                return {
                        'message': 'Question successfully added',
                        'question': question
                        }  
        
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        except HTTPException as err:
            raise err
        except Exception as err:
            raise HTTPException(status_code=500, detail="Internal Server Error")
        

### ------ Autre

# ---- Route de test de l'API
        
responses = {
    200: {"description": "OK"},
    500: {"description": "Internal server error"},
}

@api.get('/health', name='Health check', tags=['Tools'], responses=responses)
def health_check():
    """
    Health Check Endpoint.
    This route is used to check the health and functionality of the API.
    """
    try:
        return {"status": "OK", "message": "API is up and running"}
        
    except Exception as err:
        raise HTTPException(status_code=500, detail="Internal Server Error")
