
export interface Employee {
  first_name: string,
  last_name: string,
  birthday: Date,
  employee_id: number,
  curp: string,
  ssn: string,
  phone: string,
  nationality: string,
  beneficiary_count: number
}

export interface Beneficiaries {
  first_name: string,
  last_name: string,
  birthday: string,
  employee_id: number,
  curp: string,
  ssn: string,
  phone: string,
  nationality: string,
  percentage: number
}
