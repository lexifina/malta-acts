## SCHEDULE 2
# schedule-2
(Regulation 5(1))
Inland Revenue - Malta
Savings Directive Guidelines
Reporting Requirements Specifications Background
The Inland Revenue has issued guidelines for the implementation of the European Union Directive 2003/48/EC of 3 June 2003 on taxation of savings income in the form of interest payments - hereinafter in these Guidelines referred to as the "Savings Directive".
The information required by the Inland Revenue Department for the purpose of the Savings Directive is to be received in electronic format.
Scope of document
This document outlines the process that is to be used by paying agents and economic operators for the submission of information to the Inland Revenue Department in line with the Savings Directive.
It includes a brief description of the business process, the file layout and the rules related to the information that is to be submitted to the Inland Revenue Department.
Business Process
All Paying Agents are to register for the purposes of the Savings Directive with the Inland Revenue Department. This means that both Paying Agents who pay interest income directly to beneficial owners and Paying Agents who receive income on behalf of beneficial owners are to be registered with the Inland Revenue Department.
Paying Agents need to submit information to the Inland Revenue Department in the format described below in electronic format. The electronic file may be submitted on magnetic media such as diskettes and CD's.
The information is to be submitted to the Commissioner of Inland Revenue by 28th February of the year immediately following the year in which the interest payments were made.
The electronic information submitted will be accompanied by the following reconciliation form:- Savings Directive Report Reconciliation Form
Notes regarding Completion
Payors will complete Section A of the reconciliation form with the registration number given to them by the Inland Revenue for the purposes of this directive. The Name is the official name of the payor.
The Contact Name, Contact Address, Telephone Numbers and e-mail address (if applicable) are details of the person responsible for the compilation of information report submitted to the Inland Revenue.
Section B will contain details of the file information. For each file on the magnetic media that will be submitted to the Inland Revenue, the file name, the number of records and the sum of the interests reported (irrespective of the currency) are to be filled in the appropriate fields.
The form will be completed by the signature, name and date to be filled in by the person responsible for the compilation of the report.
Data Transfer Requirements
Media
The data maybe transferred on double sided high density diskette (1.44 Mb) or on a Compact Disk (CD).
The Inland Revenue Department is considering the Internet as a future medium for these data transfers. Further information regarding this medium shall be issued in due course.
File Naming Structure
The files submitted by Paying Agents on the CD or diskette shall have a unique filename, and this shall be in accordance with the following convention:
PYR9999XXXZYY99V.txt
Where: PYR9999 = Paying Agent Registration Number
XXX = Abbreviation for the Paying Agent given by the Inland Revenue upon registration for this purpose
Z = Report Type which will always be "S" for the Savings Directive report
YY = Last two digits of the year for which filename information relates
99 = Sequential file number V = Version of the file starting with 1 Examples:
(a) Submission of first report in January / February 2006 relating to an interest payment made in 2005: Filename will be PYR9999XXXS05011.txt.
(b) Submission of additional, new record in February 2006, relating to an interest payment made in 2005 and inadvertently omitted from the first report: Filename will be PYR9999XXXS05021.txt.
(c) Correction of details of an account reported in (a): Filename will be PYR9999XXXS05012.txt.
(d) Correction of details of an account reported in (b): Filename will be PYR9999XXXS05022.txt.
(e) Submission of report in January / February 2007, relating to interest payments effected in 2006 : Filename will be PYR9999XXXS06031.txt.
Format
All records are to be provided as 'pipe -delimited' variable length records. This means that all leading and trailing zeroes or blanks will be removed from the data file records.
The Inland Revenue Department will be using the OECD Automatic Exchange of Information as the main guidelines for the reporting requirements. However the full OECD format will not be implemented. The record lengths specified below should be regarded as maximum values allowed and these maximum values are based on the OECD format. The mandatory data items and related conditions are also in line with the OECD format.
File preparation and handling procedures allow for the amendment and replacement of data files. In the event of account details requiring correction for any reason, the entire file containing the defective records shall be replaced, and re-issued to the Inland Revenue Department with a revised filename, amended with the modified records indicated as Type 2 records in field Number 1. Additional, new records may be submitted in a separate new file with the file name indicating the correct sequence.
Thus in the earlier example, in the case of (c) and (d), Field No 1 for those accounts to which the corrections relate will be 2. All other accounts will show 1 in Field No1. In the case of (a), (b) and (e), Field No1 will always show 1.
Record Layout
The Inland Revenue Department needs the following information for each payment effected to the paying agent or the beneficial owner regarding which, the following general rules apply:
• Where alphabetic characters are required, the Latin Alphabetic characters only are to be reported;
• Characters that are not alphanumeric such as ", !, @, $, %, &, etc should never be reported, except for the character "-".. These characters have ascii values outside the ranges of 48 to 57 (numeric characters) and 97 to 122 (alphabetic);
• All date formats must be given in ddmmccyy format where dd is day of month, mm is month and ccyy is the full year of the date (e.g. 1999, 2001); • Data Requirements are: mandatory (M), mandatory subject to conditions
(C) or optional (O). In the format described below, where a conditional requirement or validation exists then further explanation is given under the additional information heading.
IRD OEC Field Name Type Size Data Remarks Field D Requir No Ref ement
F001 Document Type N M 1= New
Indicator 2 = Correction
F002 Residence Country A M Country Codes ISO 3166 Code of recipient
Type of recipient N M 0=Beneficial Owner 1=Paying Agent Article 4
(2)
Pre Jan 2004 N M 0 = Registered before
Registration 01/01/2004
= Registered after 31/12/2003
Paying Agent AN M Inland Revenue Registration Code Registration number of Paying Agent (PYR999)
F003 Tax Identification AN C Tax Identification Number. Number of recipient May be blank as indicated in Additional information
F007 Date of Birth N C Date format ddmmccyy Maybe blank if:
payment is made to Paying Agent or data in Field 6 (TIN) is given or Field 4 = 0 i.e Registered before 01/01/2004
F009 Surname AN M Surname of beneficial owner or name of paying agent receiving the income
F010 Other Names AN M/C All Other Names of beneficial owner or paying agent receiving the income F014 Birth City AN C Maybe blank if:
payment is made to Paying Agent or data in Field 6 is given or Field 4 = 0 i.e Registered before 01/01/2004
F016 Birth Country Code A C Country Codes ISO 3166
Maybe blank if TIN is given or payment received by a paying agent on behalf of a beneficial owner or Field 4 = 0 i.e Registered before 01/01/2004
Abode AN M Door Number and/or House Name of beneficial owner or paying agent receiving income on behalf of beneficial owner
F029 Street Address AN M Street Address of Beneficial owner or Paying Agent Receiving Income
F030 City AN M City of address of Beneficial owner or Paying Agent Receiving Income
F032 Postcode AN O Postcode of address Beneficial owner or Paying Agent Receiving Income
F033 Country Code A M Country Codes ISO 3166 2 of address of Beneficial owner or Paying Agent Receiving Income
F034 Other Address N O 0= Residential or Type Business
1=Registered Office 2=Other/Unknown Type
Other address AN C Door Number and/or abode House Name of other address of beneficial owner or paying agent receiving income on behalf of beneficial owner
F036 Other address AN C Street Address of other Street Address address
F037 Other Address City AN C City of other address
F039 Other Address AN O Postcode of Other Postcode Address
F040 Other Address AN C Country Codes ISO 3166 Country Code 2 of other address
F088 Year of date of N M Year for which Interest Payment payments were made for the account in ccyy format
F090 Type of Income AN M As per Rules in Additional Information
F091 Currency of Paid A M Currency code compliant Income with ISO 4217 3
F092 Amount-Major Unit N M Major units of currency of Income only, i.e. no decimals, no number formats and no currency indicators will be entered in this field.
F103 Bank Account AN M Relevant IBAN Number (international Bank Account number) or any identification code or the ISIN code of the debt Claim Additional Information
IRD Field Name Additional Information Fiel d No
Tax This information may not be given when:
Identification Field 4 = 0 i.e. Registered before 01/01/2004 Number (TIN) For registrations after 31/12/2003 if TIN is not given then Date of Birth and Place of Birth have to be provided in fields 7, 10 and 11.
Date of Birth Compulsory if information in field 6 (TIN) related to a beneficial owner is not given. It is optional in the other circumstances
Other Names Always mandatory for a beneficial owner. If the recipient is a paying agent on behalf of a beneficial owner then if the name of the paying agent fits in field 8 this field may be left blank.
Birth City Mandatory if TIN (Field 6) is not given or account registered after 31/12/2003, else optional.
Birth Country This field is mandatory when the TIN (Field 6) information is not given or registered after 31/12/2003. Optional in other circumstances.
Other Address Mandatory if Other Address is given (Field 17) abode
Other address Mandatory if Other Address is given (Field 17) Street Address
Other Address Mandatory if Other Address is given (Field 17) City Other Address Mandatory if Other Address is given (Field 17) Country Code
Type of Income Detailed description of type of Income paid (Article numbers refer
to Articles of the Savings Directive):
First Character must be one of a, b, c, or d where these refer to Article 8 (2) or briefly:
a = interest paid in terms of article 6 (1) (a)
b = interest paid or full amount from proceeds of sale,
redemption or refund in terms of article 6 (1) (b) or (d) c = interest paid in terms of article 6 (1) (c) income d = interest paid in terms of article 6 (4)
Second Character must be 1 or 2 where:
1= Total amount of Interest or income 2 = Total amount of proceed from sale, redemption or refund
Therefore: a can only have 1 attributed to it
b can have either 1 or 2 attributed to it
c can only have 1 attributed to it
d can only have 1 attributed to it
Third Character must be x or y where
x relates to payments made directly to beneficial owners (Article4(1)) y relates to payments made to paying agents on behalf of beneficial owners (Article 4(2)).".
