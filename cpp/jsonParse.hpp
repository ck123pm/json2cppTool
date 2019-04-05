#include "nlohmann/json.hpp"

// 序列化(Copy Version)
// c++结构体转JSON数据(string)
// 默认带外层节点
template<typename T>
inline string JsonSerialize(const T& obj, bool hasClassName = true) noexcept
{
    string str_temp;
    try
    {
        nlohmann::json j = obj;
        if (hasClassName)
        {
            nlohmann::json outer_j;
            outer_j[obj.class_name_] = j;
            str_temp = outer_j.dump();
        }
        else
        {
            str_temp = j.dump();
        }
    }
    catch (std::exception& e)
    {
        std::cout << "exception:" << e.what() << std::endl;
    }
    return str_temp;
}

// 序列化(NonCopy Version)
// c++结构体转JSON数据(string)
// 默认带外层节点
template<typename T>
inline bool JsonSerialize(const T& obj, string& str_out, bool hasClassName = true) noexcept
{
    
    try
    {
        nlohmann::json j = obj;
        if (hasClassName)
        {
            nlohmann::json outer_j;
            outer_j[obj.class_name_] = j;
            str_out = outer_j.dump();
        }
        else
        {
            str_out = j.dump();
        }
    }
    catch (std::exception& e)
    {
        std::cout << "exception:" << e.what() << std::endl;
        return false;
    }
    return true;
}

// 序列化
// c++结构体转JSON对象
// 默认带外层节点
template<typename T>
inline bool JsonSerialize(const T& obj, nlohmann::json& j, bool hasClassName = true) noexcept
{
    try
    {
        if (hasClassName)
        {
            nlohmann::json iner_j = obj;
            j[obj.class_name_] = iner_j;
        }
        else
        {
            j = obj;
        }
    }
    catch (std::exception& e)
    {
        std::cout << "exception:" << e.what() << std::endl;
        return false;
    }
    return true;
}

// 反序列化
// JSON数据（string）转c++结构体
// 外层节点自适应解析
template<typename T>
inline bool JsonDeserialize(const string& str_raw, T& obj)  noexcept
{
    nlohmann::json j;
    try
    {
        j = nlohmann::json::parse(str_raw);

        if (j.count(obj.class_name_)>0)
        {
            obj = j[obj.class_name_];
        }
        else
        {
            obj = j;
        }
        
    }
    catch (const std::exception& e)
    {
        std::cout << "exception:" << e.what() << std::endl;
        return false;
    }
    return true;
}

// 反序列化
// JSON对象转c++结构体
// 外层节点自适应解析
template<typename T>
inline bool JsonDeserialize(const nlohmann::json& j, T& obj)  noexcept
{
    try
    {
        
        if (j.count(obj.class_name_) > 0)
        {
            obj = j[obj.class_name_];
        }
        else
        {
            obj = j;
        }
        
    }
    catch (const std::exception& e)
    {
        std::cout << "exception:" << e.what() << std::endl;
        return false;
    }
    return true;
}

// JSON数据解析
// JSON数据转JSON对象
bool JsonParse(const string& str_raw, nlohmann::json& j) noexcept
{
    try
    {
        j = nlohmann::json::parse(str_raw);
    }
    catch (const std::exception& e)
    {
        std::cout << "exception:" << e.what() << std::endl;
        return false;
    }
    return true;
}