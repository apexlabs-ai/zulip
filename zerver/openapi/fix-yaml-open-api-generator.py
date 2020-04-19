# Not a clean code, was hacking away in a hurry trying to understand what works... alexis
# pip install pyyaml stringcase
import yaml
import stringcase


with open('zulip.yaml') as stream:
    schema = yaml.safe_load(stream)


linenr=0
# print(schema['paths'])
for path in schema['paths'].keys():
    linenr += 1
    for method in schema['paths'][path].keys():
        for status in schema['paths'][path][method]['responses'].keys():
            if schema['paths'][path][method]['responses'][status].get('content', None):
                allOf = schema['paths'][path][method]['responses'][status]['content']['application/json']['schema'].get('allOf', None)
                if allOf:
                    print(path)
                    print(method)
                    print(status)
                    if status == '200':
                        suffix = 'response'
                    elif status == '400':
                        suffix = 'error'
                    else:
                        suffix = status
                    refName = stringcase.camelcase("{}_{}_{}".format(
                        path.replace('/', '', 1).replace('/', '_').replace('{', '').replace('}', ''), method, suffix))
                    print(refName)
                    schema['components']['schemas'][refName] = {
                        'allOf': allOf
                    }
                    schema['paths'][path][method]['responses'][status]['content']['application/json']['schema'] = {
                        "$ref": "#/components/schemas/{}".format(refName)
                    }

with open('zulip-open-api-generator.yaml', 'w') as file:
    documents = yaml.dump(schema, file)
