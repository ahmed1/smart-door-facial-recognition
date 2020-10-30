sam build --use-container --template-file template.yaml

sam local invoke SDLF1Function -e events/$1 # event.json, event-unknown_face.json
