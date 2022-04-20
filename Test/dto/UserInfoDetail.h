//
// UserInfoDetail.h
//
// -- generated file, do NOT edit
//
#pragma once

#include "EmployeeNoList.h" //generated



namespace JsonMapper{

struct UserInfoDetail
{
	//constructors
	UserInfoDetail() = default;

	//member data
	std::list<EmployeeNoList> m_EmployeeNoList;
	std::string m_mode;
	std::set<std::string> m_visibleSet;
	std::set<std::string> m_hiddenSet;
	std::string class_name_ = "UserInfoDetail";
};
//json parsing and serializing mapper function
void from_json(const nlohmann::json& j, UserInfoDetail & UserInfoDetailIn);
void to_json(nlohmann::json& j, const UserInfoDetail & UserInfoDetailIn);

} // namespace JsonMapper