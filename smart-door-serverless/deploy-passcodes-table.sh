sam build --use-container --template-file passcodes-template.yaml

sam package --s3-bucket smart-door-cloudformation-template --output-template-file packaged.yaml

sam deploy --template-file ./packaged.yaml --stack-name smart-door-passcodes-table --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
