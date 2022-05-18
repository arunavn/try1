import os
def execute_groovy_by_cli(config_dict):
    #download cli
    download_cli_cmd= f"curl --output jenkins-cli.jar {config_dict['base_url']}/jnlpJars/jenkins-cli.jar"
    s1= os.popen(download_cli_cmd)

    #run script
    stream= os.popen('clear')
    groovy_cmd= f"java -jar jenkins-cli.jar -s {config_dict['base_url']} -auth {config_dict['user']}:{config_dict['password']} groovy = < ./{config_dict['groovy_script']}"
    stream = os.popen(groovy_cmd)
    output = stream.readlines()
    os.remove(config_dict['groovy_script'])
    return output
    


def modify_groovy_script(config_dict, param_dict):
    in_file= config_dict['groovy_script']
    out_file= in_file.split('.')[0] + '-tempfile.' + 'groovy'
    with open(in_file, 'r') as fd:
        data_lines = fd.readlines()
    data_lines_out= []
    for l in data_lines:
        for k, v in param_dict.items():
            param_str= f'<param>{k}</param>'
            l= l.replace(param_str, v )
        data_lines_out.append(l)
    with open(out_file, 'w') as fd:
         fd.writelines(data_lines_out)
    config_dict['groovy_script']= out_file
    return config_dict

def execute_groovy_script(param_dict, config_dict= None, script_name= None, base_url= None):

    if config_dict == None:
        config_dict= {
            'base_url': 'http://localhost:8080',
            'user': 'arunav',
            'api_token': '11a27f4c2dd249a61598c93d315e528b27',
            'password': 'hello123',
            'groovy_script': 'groovy-file.groovy'
        }
    if script_name is not None:
        config_dict['groovy_script']= script_name
    if base_url is not None:
        config_dict['base_url']= base_url

    config_dict= modify_groovy_script(config_dict, param_dict)
    output1= execute_groovy_by_cli(config_dict)
    return output1

def main():
    param_dict= {
        "user1": "arun1",
        "user2": "arun2",
        "pass1": "heelo1",
        "pass2": "hello2",
    }    
    output1= execute_groovy_script(param_dict)
    """output is a list of output line in grrovy"""
    for l in output1:
        print(l)

if __name__ == '__main__':
    main()
