#!/user/bin/env python

import json5
import os
import sys
from types import *
#from collections import OrderedDict

class Json2cpp():
    __filelist = []
    __cb = None

    def __cpp_identifier(self, name):
        identifier = name
        if (identifier[0].isdigit()):
            identifier = "_" + identifier
        return identifier.replace(".", "_")

    def __cpp_typename(self, name):
        return self.__cpp_identifier(name)

    def __cpp_filename(self, name):
        return self.__cpp_identifier(name)

    def __cpp_type(self, value):
        if isinstance(value, bool):
            return 'bool'
        elif isinstance(value, int):
            return 'int'
        elif isinstance(value, float):
            return 'double'
        elif isinstance(value, str):
            return 'std::string'
        elif isinstance(value, list):
            return 'std::list'
        elif isinstance(value, dict):
            return 'class' #'std::map' #TODO - anonymous class (in array?) ??
        else: #dict?
            #print("unsupported type {}".format(type(value)))
            pass #return None

    def __generate_variable_info(self, data):
        includes = []
        varinfo = []
        for k, v in list(data.items()):    
            if isinstance(v, list): #json array
                #if not 'vector' in includes:
                #    includes.append('#include <vector>')
                if isinstance(v[0], dict):
                    includes.append('#include "{}.h" //generated'.format(self.__cpp_filename(k)))
                    varinfo.append((self.__cpp_type(v), self.__cpp_type(v[0]), k, v))
                else:
                    varinfo.append((self.__cpp_type(v), self.__cpp_type(v[0]), k))
            elif isinstance(v, dict): #json object
                if not k in includes:
                    includes.append('#include "{}.h" //generated'.format(self.__cpp_filename(k)))
                varinfo.append(('class',k, data[k]))
            else: #simple type
                typename = self.__cpp_type(v)
                varinfo.append((typename, k))
                #if 'string' in typename and not 'string' in includes:
                #    includes.append('#include <string>')
        return includes, varinfo


    def __membersList(self, varinfo, obj = None):
        members = []
        for info in varinfo:
            memberName = 'm_' if obj is None else '{}.m_'.format(obj)
            memberName += __cpp_identifier(info[2] if len(info) >= 3 and info[0] != "class" else info[1])
            members.append(memberName)
        return ", ".join(members)
        
    # generate output .h
    def __generate_header(self, classname, includes, varinfo, dirname):
        f = open(dirname + '/' + classname + '.h', 'wt')
        # f.write('#include \"json.hpp\"\n\n')
        f.write('//\n// {}.h\n'.format(classname))
        f.write('//\n// -- generated file, do NOT edit\n//\n')
        f.write('#pragma once\n\n')
        for i in range(len(includes)):
            f.write("{}\n".format(includes[i]))

        # namespace
        f.write('namespace JsonMapper{')
        #class definition
        f.write('\n\nstruct {}\n'.format(classname))
        f.write('{\n')
        #constructors
        f.write('\t//constructors\n')
        f.write('\t{}() = default;\n'.format(classname)) #explicitly defaulted ctor (force compiler generated default-ctor since the user ctor below otherwise inhibits it)
        
        #data members
        f.write('\n\t//member data\n')
        for info in varinfo:
            if len(info) >= 3:
                if info[0] == "class": #json object
                    f.write('\t{} m_{};\n'.format(self.__cpp_typename(info[1]), self.__cpp_identifier(info[1])))
                else: #json array
                    itemType = "{}".format(info[2]) if info[1] == "class" else info[1]
                    f.write('\t{}<{}> m_{};\n'.format(info[0], self.__cpp_typename(itemType), self.__cpp_identifier(info[2])))
            elif len(info) == 2: #simple type
                f.write('\t{} m_{};\n'.format(self.__cpp_typename(info[0]), self.__cpp_identifier(info[1])))
        f.write('\tstd::set<std::string> m_visibleSet;\n')
        f.write('\tstd::set<std::string> m_hiddenSet;\n')
        f.write('\tstd::string class_name_ = "{}";\n'.format(classname))
        f.write('};\n')

        #load/save methods
        f.write('//json parsing and serializing mapper function\n')
        
        f.write('void from_json(const nlohmann::json& j, {} & {});\n'.format(classname,classname+"In"))
        f.write('void to_json(nlohmann::json& j, const {} & {});\n'.format(classname,classname+"In"))

        f.write('\n} // namespace JsonMapper')

    def __generate_full(self, f,classname, varinfo,dirname):
        f.write('''
        if({cname}.m_visibleSet.empty() && {cname}.m_hiddenSet.empty())
        {{
            j = nlohmann::json{{
        '''.format(cname = classname+"In"))

        lines = ""
        for info in varinfo:
            if len(info) >= 3:
                if (info[0] == "class"): #json object
                    lines+='\t\t{{ "{}",{}.m_{} }},\n'.format(info[1], classname+"In", self.__cpp_identifier(info[1]))               
                    self.__generate(info[1], info[2], dirname) #recursively generate related classes
                elif 'list' in info[0]: #json array
                    lines+='\t\t{{ "{}",{}.m_{} }},\n'.format(info[2], classname+"In", self.__cpp_identifier(info[2])) 
                    if info[1] == "class": 
                        self.__generate("{}".format(info[2]), info[3][0], dirname) #recursively generate related classes
            elif len(info) == 2: #simple type
                if not info[0] is None:
                    lines+='\t\t{{ "{}",{}.m_{} }},\n'.format(info[1], classname+"In", self.__cpp_identifier(info[1]))
        lines = lines[:-2]
        f.writelines(lines)
        f.write('''};
        ''')

    def __generate_visible(self, f,classname, varinfo):
        f.write('''}}
        else if(!{cname}.m_visibleSet.empty()){{
            '''.format(cname = classname+"In"))
        for info in varinfo:
            if len(info) >= 3:
                if (info[0] == "class"): #json object
                    lines = '''
                    if({cname}.m_visibleSet.count("{member}")>0)
                    {{
                        j["{member}"] = {cname}.m_{member};
                    }}'''.format(cname = classname+"In",member = self.__cpp_identifier(info[1]))     
                    f.write(lines)   
                elif 'list' in info[0]: #json array
                    lines = '''
                    if({cname}.m_visibleSet.count("{member}")>0)
                    {{
                        j["{member}"] = {cname}.m_{member};
                    }}'''.format(cname = classname+"In",member = self.__cpp_identifier(info[2]))
                    f.write(lines)   
            elif len(info) == 2: #simple type
                if not info[0] is None:
                    lines = '''
                    if({cname}.m_visibleSet.count("{member}")>0)
                    {{
                        j["{member}"] = {cname}.m_{member};
                    }}'''.format(cname = classname+"In",member = self.__cpp_identifier(info[1]))
                    f.write(lines)   
        # f.write('\n\t}\n')

    def __generate_hidden(self, f,classname, varinfo):
        f.write('''}}
        else if(!{cname}.m_hiddenSet.empty()){{
            '''.format(cname = classname+"In"))
        for info in varinfo:
            if len(info) >= 3:
                if (info[0] == "class"): #json object
                    lines = '''
                    if({cname}.m_hiddenSet.count("{member}")==0)
                    {{
                        j["{member}"] = {cname}.m_{member};
                    }}'''.format(cname = classname+"In",member = self.__cpp_identifier(info[1]))     
                    f.write(lines)   
                elif 'list' in info[0]: #json array
                    lines = '''
                    if({cname}.m_hiddenSet.count("{member}")==0)
                    {{
                        j["{member}"] = {cname}.m_{member};
                    }}'''.format(cname = classname+"In",member = self.__cpp_identifier(info[2]))
                    f.write(lines)   
            elif len(info) == 2: #simple type
                if not info[0] is None:
                    lines = '''
                    if({cname}.m_hiddenSet.count("{member}")==0)
                    {{
                        j["{member}"] = {cname}.m_{member};
                    }}'''.format(cname = classname+"In",member = self.__cpp_identifier(info[1]))
                    f.write(lines)   
        f.write('\n\t}\n')

    # generate output .cpp
    def __generate_source(self, classname, varinfo, dirname):
        f = open(dirname + '/' + classname + '.cpp', 'wt')
        f.write('//\n// {}.cpp\n'.format(classname))
        f.write('//\n// -- generated class for jsoncpp\n//\n')
        f.write('#include \"stdafx.h\"\n\n')
        f.write('#include \"../../nlohmann/json.hpp\"\n\n')
        f.write('#include \"{}.h\"\n\n'.format(classname))
        
        # namespace
        f.write('namespace JsonMapper{\n')

        
        #load method:
        f.write('// parse\n')
        f.write('void from_json(const nlohmann::json& j, {} & {})\n'.format(classname,classname+"In"))
        f.write('{\n')
        # f.write('\ttry\n')
        # f.write('\t{\n')
        for info in varinfo:
            if len(info) >= 3:
                if (info[0] == "class"): #json object
                    f.writelines('''
            if (j.count("{}") !=0 )
            {{
                j.at("{}").get_to({}.m_{}); //json object
            }}
                    '''.format(info[1],info[1], classname+"In",self.__cpp_identifier(info[1])))
                elif 'list' in info[0]: #json array
                    f.writelines('''
            if (j.count("{}") !=0 )
            {{
                j.at("{}").get_to({}.m_{}); //json object
            }}
                    '''.format(info[2], info[2], classname+"In",self.__cpp_identifier(info[2]))) 
            elif len(info) == 2: #simple type
                if not info[0] is None:
                    f.writelines('''
            if (j.count("{}") !=0 )
            {{
                j.at("{}").get_to({}.m_{}); 
            }}
                    '''.format(info[1],info[1], classname+"In",self.__cpp_identifier(info[1]))) 

        # f.write('\r\t}\n')
        # f.writelines('''
        # catch (std::exception& e)
        # {
        #   std::cout << "exception:" << e.what() << std::endl;
        #     DAM_LOG_ERROR(str(boost::format("Deserialize from json catch exception. info is %1%") % e.what() % ));
        # }
        # ''')
        f.write('\n')
        f.write('}\n')
        f.write('\n')

        #save method
        f.write('\n// serialize\n')
        f.write('void to_json(nlohmann::json& j, const {} & {})\n'.format(classname,classname+"In"))
        f.write('{\n')
        self.__generate_full(f,classname,varinfo,dirname)
        
        self.__generate_visible(f,classname,varinfo)
        self.__generate_hidden(f,classname,varinfo)

        f.write('}\n')
        


        f.write('\n} // namespace JsonMapper')


    # generate output files
    def __generate(self, classname, data, dirname):
        includes, varinfo = self.__generate_variable_info(data)
        varinfo.sort()
        try:
            os.stat(dirname)
        except:
            os.mkdir(dirname)
        classId = self.__cpp_identifier(classname)
        self.__generate_header(classId, includes, varinfo, dirname)
        self.__generate_source(classId, varinfo, dirname)
        print("Generated class: {}".format(classId))
        if self.cb != None:
            self.cb("Generated class: {}".format(classId))

    def runJsonData(self, jsondata, path = './' , callback = None):
        self.cb = callback
        data = []
        try:
            data = json5.loads(jsondata) #data = json.loads(content, object_pairs_hook=OrderedDict)
        except :
            callback("Json data parse error.")
            return
        keys = list(data.keys())
        classname = keys[0]
        data = data[classname]
        self.__generate(classname, data, path)

    def run(self, filelist, path ='./' , callback = None):
        __filelist = filelist
        self.cb = callback
        for filename in __filelist:
            try:
                with open(filename,encoding='UTF-8') as f:
                    content = f.read()
            except IOError:
                print ("Can't open/read file {}".format(filename))
                callback("Can't open/read file {}".format(filename))
                continue
            data = []
            try:
                data = json5.loads(content) #data = json.loads(content, object_pairs_hook=OrderedDict)
            except :
                real_filename = os.path.basename(filename)
                callback(real_filename+" parse error.")
                return
            keys = list(data.keys())
            classname = keys[0]
            data = data[classname]
            self.__generate(classname, data, path)


#entry point
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ('Usage: {} <json file>'.format(sys.argv[0]))
        sys.exit(1)
    filename = sys.argv[1]
    filelist = [filename]
    # filename = 'ClearPlansCfg.json'
    # classname = __cpp_identifier(filename.split('.')[0])
    j = Json2cpp()
    j.run(filelist)
    sys.exit(0)

#
# based on https://gist.github.com/soharu/5083914
#
# Generate c++(11) mapping classes for the object(s) inside a given json file. 
# Each data member of a generated class is mapped onto an existing json property.
# Note: the json is actually loaded/saved using an external library (cpprest).
#
# Warning: json arrays must be homogeneous
#