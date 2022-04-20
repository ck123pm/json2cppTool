//
// EmployeeNoList.cpp
//
// -- generated class for jsoncpp
//
#include "def.h"
#include "json.hpp"

#include "EmployeeNoList.h"

namespace JsonMapper{
// parse
void from_json(const nlohmann::json& j, EmployeeNoList & EmployeeNoListIn)
{

            if (j.count("employeeNo") !=0 )
            {
                j.at("employeeNo").get_to(EmployeeNoListIn.m_employeeNo); 
            }
                    
}


// serialize
void to_json(nlohmann::json& j, const EmployeeNoList & EmployeeNoListIn)
{

        if(EmployeeNoListIn.m_visibleSet.empty() && EmployeeNoListIn.m_hiddenSet.empty())
        {
            j = nlohmann::json{
        		{ "employeeNo",EmployeeNoListIn.m_employeeNo }};
        }
        else if(!EmployeeNoListIn.m_visibleSet.empty()){
            
                    if(EmployeeNoListIn.m_visibleSet.count("employeeNo")>0)
                    {
                        j["employeeNo"] = EmployeeNoListIn.m_employeeNo;
                    }}
        else if(!EmployeeNoListIn.m_hiddenSet.empty()){
            
                    if(EmployeeNoListIn.m_hiddenSet.count("employeeNo")==0)
                    {
                        j["employeeNo"] = EmployeeNoListIn.m_employeeNo;
                    }
	}
}

} // namespace JsonMapper