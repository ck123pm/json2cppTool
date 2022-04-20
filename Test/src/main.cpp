#include "def.h"
#include "json.hpp"
#include "jsonParse.hpp"

#include <iostream>
#include "UserInfoDetail.h"

using namespace JsonMapper;
int main(int, char**) {
    UserInfoDetail user_info_detail;
    EmployeeNoList employee_no_list;
    employee_no_list.m_employeeNo = "test123";
    user_info_detail.m_mode = "string";
    user_info_detail.m_EmployeeNoList.push_back(employee_no_list);
    std::string content = JsonSerialize(user_info_detail);

    std::cout<<content<<endl;
    std::cout<<JsonSerialize(employee_no_list) <<endl;

    UserInfoDetail user_info_detail_new;
    if( !JsonDeserialize(content, user_info_detail_new)){
        return -1;
    }
    
    return 0;
    
}
