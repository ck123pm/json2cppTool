//
// EmployeeNoList.h
//
// -- generated file, do NOT edit
//
#pragma once

namespace JsonMapper{

struct EmployeeNoList
{
	//constructors
	EmployeeNoList() = default;

	//member data
	std::string m_employeeNo;
	std::set<std::string> m_visibleSet;
	std::set<std::string> m_hiddenSet;
	std::string class_name_ = "EmployeeNoList";
};
//json parsing and serializing mapper function
void from_json(const nlohmann::json& j, EmployeeNoList & EmployeeNoListIn);
void to_json(nlohmann::json& j, const EmployeeNoList & EmployeeNoListIn);

} // namespace JsonMapper