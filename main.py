import sys
import json

import couchdb

def read_json_file(file_name):
    with open(file_name, "r") as json_file:
        json_data = json.load(json_file)

    return json_data

def get_shape_list (l):
    return len(l), len(l[0])

def is_header_line(s):
    return s.startswith("#")

def read_csv(file_name):
    table = []
    file_object = open(file_name)
    for line in file_object:
        table.append(line.rstrip().split(";") )
       
    file_object.close()

    return table

def check_table(table):
    no_row , no_col = get_shape_list(table)
    for i in range(no_row):
        if len(table[i]) != no_col:
            sys.exit("wrong number of columns in line {}".format(i))

def clear_string(s):
    s = s.lstrip("#")
    s = s.replace(":", "")
    s = s.lstrip().rstrip()
    s = s.replace(" ", "_")
    
    return s

def remove_element(line_list,d):
    r = d.get("remove", False) 
    if r:
        for i in r:
            del line_list [i]

    return line_list

def translate_header(line_list, db_dict, header_dict):
    key_entry = line_list[0]
    clear_key = clear_string( key_entry )
    d = header_dict.get( clear_key, False )
    
    if d:
        v = d.get("value")
        k = d.get("key")
        line_list=remove_element(line_list,d)

        all=range (len(line_list))

        if type(v) == list:
            if len(v) == 1:
                db_dict[k] = line_list[ v[0] ]
            else: 
                db_dict[k] = [line_list[i] for i in v] 
        if type(v) == str:
            db_dict[k] = v
            if v == "@all":
                db_dict[k] = [line_list[i] for i in all]

    return db_dict

def translate_data(line_list, db_dict):
    

    return db_dict


def table_to_dict(table, header_dict):
    db_dict = {}
    
    for line in table:
        first_entry = line[0]

        if is_header_line(first_entry):
            db_dict = translate_header(line, db_dict, header_dict)
        else:
            db_dict = translate_data(line, db_dict)

    return db_dict

if __name__ == "__main__":
    table = read_csv("AP.csv")
    header_dict = read_json_file("header.json")

    check_table(table)

    db_dict = table_to_dict(table, header_dict)
    
    #write_to_db(db_dict)

    print(db_dict)
