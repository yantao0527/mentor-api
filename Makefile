
install:
	python -m pip install -r requirements.txt

dev:
	uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload

#	  -e MONGO_INITDB_ROOT_USERNAME=admin \
#	  -e MONGO_INITDB_ROOT_PASSWORD=mcafee123 \

mongo-run:
	docker run -d --name mongo \
	  -p 27017:27017 \
	  -v mongo_db:/data/db \
	  mongo:3.6.17

mongo-start:
	docker start mongo

volume-db:
	docker volume create mongo_db

mongo-cli:
	docker exec -it mongo bash -c 'mongo mongodb://localhost/admin'

## Test

API_BASE=http://127.0.0.1:8000

test-register:
	curl -X 'POST' \
	'${API_BASE}/auth/register' \
	-H 'accept: application/json' \
	-H 'Content-Type: application/json' \
	-d '{"email": "yantao0527@gmail.com", "password": "nice", "is_active": true, "is_superuser": false, "is_verified": false}'

test-login:
	curl -X 'POST' \
	  '${API_BASE}/auth/bearer/login' \
	  -H 'accept: application/json' \
	  -H 'Content-Type: application/x-www-form-urlencoded' \
	  -d 'grant_type=password&username=yantao0527%40gmail.com&password=nice&scope=scopes'
	@echo "\nSet env: export BEARER_TOKEN=..."

test-me:
	curl -X 'GET' \
	  '${API_BASE}/users/me' \
	  -H 'accept: application/json' \
	  -H "Authorization: Bearer ${BEARER_TOKEN}"