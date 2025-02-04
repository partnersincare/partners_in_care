# file descriptions and filters

## self_identified_vets

veteran status, yes
head_of_household, yes
enrolled in a non-Homelessness Prevention during the relevant time period

## coordinated_entry_vets

veteran status, yes
head_of_household, yes
enrolled in a coordinated entry program during the relevant time period

## bnl_list_vets

veteran status, yes
head_of_household, yes
enrolled in a coordinated entry program during the relevant time period
assessment date for VI-SPDAT within a year of the relevant time period

## bnl_list_vets_eligible

veteran status, yes
head_of_household, yes
enrolled in a coordinated entry program during the relevant time period
assessment date for VI-SPDAT within a year of the relevant time period
discharge status is one of [
    "General",
    "Honorable",
    "Eligible: National Guard/Reserves",
    "Ineligible VHA due to length of active service",
    "Other Than Honorable (OTH)",
    "Bad Conduct Discharge (BCD)",
]

## vets_with_dd214

veteran status, yes
head_of_household, yes
enrolled in a coordinated entry program during the relevant time period
assessment date for VI-SPDAT within a year of the relevant time period
discharge status is one of [
    "General",
    "Honorable",
    "Eligible: National Guard/Reserves",
    "Ineligible VHA due to length of active service",
    "Other Than Honorable (OTH)",
    "Bad Conduct Discharge (BCD)",
]
has a file named DD 214 (Veterans Only) on file

## chronic_vets

veteran status, yes
head_of_household, yes
enrolled in a coordinated entry program during the relevant time period
assessment date for VI-SPDAT within a year of the relevant time period
discharge status is one of [
    "General",
    "Honorable",
    "Eligible: National Guard/Reserves",
    "Ineligible VHA due to length of active service",
    "Other Than Honorable (OTH)",
    "Bad Conduct Discharge (BCD)",
]
not in transitional housing
either chronically homeless at project start is yes
OR
(disabling condition is yes AND current episode of homelessness started more than 365 days ago)

## sheltered_vets

veteran status, yes
head_of_household, yes
enrolled in a coordinated entry program during the relevant time period
assessment date for VI-SPDAT within a year of the relevant time period
discharge status is one of [
    "General",
    "Honorable",
    "Eligible: National Guard/Reserves",
    "Ineligible VHA due to length of active service",
    "Other Than Honorable (OTH)",
    "Bad Conduct Discharge (BCD)",
]
was enrolled in one of [
    "Safe Haven",
    "Transitional Housing",
    "Emergency Shelter – Entry Exit",
]
during the relevant time period

## inflow_vets

veteran status, yes
head_of_household, yes
enrolled in a coordinated entry program during the relevant time period
assessment date for VI-SPDAT within a year of the relevant time period
discharge status is one of [
    "General",
    "Honorable",
    "Eligible: National Guard/Reserves",
    "Ineligible VHA due to length of active service",
    "Other Than Honorable (OTH)",
    "Bad Conduct Discharge (BCD)",
] and didn't meet one or more of these conditions in previous month

## outflow_vets

does not meet one fo more of these conditions
veteran status, yes
head_of_household, yes
enrolled in a coordinated entry program during the relevant time period
assessment date for VI-SPDAT within a year of the relevant time period
discharge status is one of [
    "General",
    "Honorable",
    "Eligible: National Guard/Reserves",
    "Ineligible VHA due to length of active service",
    "Other Than Honorable (OTH)",
    "Bad Conduct Discharge (BCD)",
] and did meet all of these conditions in previous month
