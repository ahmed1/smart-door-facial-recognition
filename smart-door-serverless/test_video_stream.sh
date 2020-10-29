sam build --use-container --template-file template.yaml

sam local invoke SDLF1Function -e events/event.json
