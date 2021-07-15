# json2cppTool
A tool used to generate cpp structs based on [nlohmann/json](https://github.com/nlohmann/json)

## 快速开始
### 生成cpp文件
为了方便使用，基于tkinter做了一个界面，可以用Pyinstaller或者pyApp等打包成对应平台的可执行程序方便使用。目前该工具只支持包含外层节点的JSON数据格式。
1. cd python
2. pip install -r requirements.txt
3. python json2cppTool.py
4. 填入JSON数据或者选择JSON数据文件
5. 选择输出路径
6. 点击生成

JSON数据如下：
```json
{
    "UserInfoDetail": {
        "mode": "",
        "EmployeeNoList": [
            {
                "employeeNo": ""
            }
        ]
    }
}

```
   
![json2cpp.png](https://upload-images.jianshu.io/upload_images/14735454-549c3dcaecfbec8b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


### 文件导入工程
生成文件如下:
```
UserInfoDetail.h
UserInfoDetail.cpp
EmployeeNoList.h
EmployeeNoList.cpp
```

### C++程序中使用
**序列化**
```c++
UserInfoDetail user_info_detail ;
user_info_detail.m_mode = "all";
string str_json = JsonSerialize(user_info_detail);
```
**反序列化**
```
ResponseStatus response_status;
if (!JsonDeserialize(str_raw, response_status))
{
    return false;
}
```
That's it!
> 对于列表`std::list<T>`类型的节点，我们也无需做特殊处理，`nlohmann`已经将列表和`JSON Array`间的转换实现掉了。

### 进阶用法
#### 序列化时控制是否输出外层节点
默认会输出外层节点，但是可以通过JsonSerialize(Obj,**false**)来指定不生成外层节点。

示例：
```c++
string str_json = JsonSerialize(user_info_detail, false);
```
输出的JSON：
```json
{ 
    "mode": "",
    "EmployeeNoList": [
        {
            "employeeNo": ""
        }
    ]
}
```

#### 指定组装的节点
在默认情况下，自动映射会将c++结构体中的所有成员均映射到JSON中的节点。

但有的场景，我们希望发送给客户端或服务端的JSON数据中，只包含部分必填字段。
自动生成的c++结构体中包含了一个`std::set<std::string> m_visibleSet;`成员，通过该成员控制需要输出的节点。

示例：
```c++
UserInfoDetail user_info_detail ;
user_info_detail.m_mode = "all";
user_info_detail.m_visibleSet = {
    "mode",
};
string str_json = JsonSerialize(clearCfg);
```
输出的JSON：
```json
{
    "UserInfoDetail": {
        "mode": "all"
    }
}
```

#### 指定需要忽略的节点
在默认情况下，自动映射会将c++结构体中的所有成员均映射到JSON中的节点。

但有的场景，我们希望发送给客户端或服务端的JSON数据中，能忽略某些节点。
自动生成的c++结构体中包含了一个`std::set<std::string> m_hiddenSet;`成员，通过该成员控制需要忽略的节点。

示例：
```c++
UserInfoDetail user_info_detail ;
user_info_detail.m_mode = "all";
user_info_detail.m_hiddenSet = {
    "EmployeeNoList",
};
string str_json = JsonSerialize(clearCfg);
```
输出的JSON：
```json
{
    "UserInfoDetail": {
        "mode": "all"
    }
}
```
