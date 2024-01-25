#Tester le fonctionnement de l'API
curl -X 'GET' \
  'http://127.0.0.1:8000/health' \
  -H 'accept: application/json'

#Lister les questions
curl -X 'GET' \
  'http://127.0.0.1:8000/' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic bob:builder'

#Lister les différents types de QCM
curl -X 'GET' \
  'http://127.0.0.1:8000/use' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic bob:builder'

#Lister les différentes catégories pour un type (ici Test de positionnement)
curl -X 'GET' \
  'http://127.0.0.1:8000/subjects?use=Test%20de%20positionnement' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic bob:builder'

#Générer un test de 10 questions sur le type Total Bootcamp et les catégories Machine Learning et Data Science
curl -X 'GET' \
  'http://localhost:8000/test?use=Total%20Bootcamp&nbr_questions=10&subjects=Machine%20Learning&subjects=Data%20Science' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic bob:builder'

#Ajout d'une nouvelle question
curl -X 'POST' \
  'http://localhost:8000/new_question' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic admin:4dm1n' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "Nouvelle question",
  "subject": "BDD",
  "use": "Test de positionnement",
  "correct": "A",
  "responseA": "Réponse A",
  "responseB": "Réponse B",
  "responseC": "Réponse C",
  "responseD": "",
  "remark": ""
    }'
