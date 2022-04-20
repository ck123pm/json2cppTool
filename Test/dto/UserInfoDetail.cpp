//
// UserInfoDetail.cpp
//
// -- generated class for jsoncpp
//
#include "def.h"
#include "json.hpp"

#include "UserInfoDetail.h"

namespace JsonMapper{
// parse
void from_json(const nlohmann::json& j, UserInfoDetail & UserInfoDetailIn)
{

            if (j.count("EmployeeNoList") !=0 )
            {
                j.at("EmployeeNoList").get_to(UserInfoDetailIn.m_EmployeeNoList); //json object
            }
                    
            if (j.count("mode") !=0 )
            {
                j.at("mode").get_to(UserInfoDetailIn.m_mode); 
            }
                    
}


// serialize
void to_json(nlohmann::json& j, const UserInfoDetail & UserInfoDetailIn)
{

        if(UserInfoDetailIn.m_visibleSet.empty() && UserInfoDetailIn.m_hiddenSet.empty())
        {
            j = nlohmann::json{
        		{ "EmployeeNoList",UserInfoDetailIn.m_EmployeeNoList },
		{ "mode",UserInfoDetailIn.m_mode }};
        }
        else if(!UserInfoDetailIn.m_visibleSet.empty()){
            
                    if(UserInfoDetailIn.m_visibleSet.count("EmployeeNoList")>0)
                    {
                        j["EmployeeNoList"] = UserInfoDetailIn.m_EmployeeNoList;
                    }
                    if(UserInfoDetailIn.m_visibleSet.count("mode")>0)
                    {
                        j["mode"] = UserInfoDetailIn.m_mode;
                    }}
        else if(!UserInfoDetailIn.m_hiddenSet.empty()){
            
                    if(UserInfoDetailIn.m_hiddenSet.count("EmployeeNoList")==0)
                    {
                        j["EmployeeNoList"] = UserInfoDetailIn.m_EmployeeNoList;
                    }
                    if(UserInfoDetailIn.m_hiddenSet.count("mode")==0)
                    {
                        j["mode"] = UserInfoDetailIn.m_mode;
                    }
	}
}

} // namespace JsonMapper