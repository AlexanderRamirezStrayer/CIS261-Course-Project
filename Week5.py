import datetime

# --- Helper Functions for Efficient Code (Part 2) ---

def get_validated_float(prompt, min_val=0.0):
    """Inputs and returns a float value with basic validation."""
    while True:
        try:
            value = float(input(prompt).strip())
            if value >= min_val:
                return value
            else:
                print(f"Value must be non-negative (>= {min_val}). Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# --- Employee Input Functions (Part 1) ---

# 1. New function to input and return from and to dates
def get_dates():
    """
    Inputs and returns the start and end dates for the pay period in mm/dd/yyyy format.
    This should be the first function called in the loop.
    """
    date_format = "%m/%d/%Y"
    while True:
        try:
            from_date_str = input("Enter Pay Period Start Date (mm/dd/yyyy): ").strip()
            datetime.datetime.strptime(from_date_str, date_format) # Validation check
            
            to_date_str = input("Enter Pay Period End Date (mm/dd/yyyy): ").strip()
            datetime.datetime.strptime(to_date_str, date_format) # Validation check
            
            return from_date_str, to_date_str
        except ValueError:
            print("ERROR: Date must be in the mm/dd/yyyy format. Please try again.")

def get_employee_name():
    """Inputs and returns the employee's name or 'End' to terminate the loop."""
    while True:
        name = input("\nEnter Employee Name (or type 'End' to finish): ").strip()
        if name.lower() == 'end':
            return 'End'
        if name:
            return name
        print("Name cannot be empty. Please try again.")

def get_total_hours():
    """Inputs and returns the employee's total hours worked."""
    return get_validated_float("Enter Total Hours Worked: ", min_val=0.0)

def get_hourly_rate():
    """Inputs and returns the employee's hourly pay rate."""
    return get_validated_float("Enter Hourly Pay Rate ($): ", min_val=0.01)

def get_income_tax_rate():
    """Inputs and returns the income tax rate (as a decimal)."""
    while True:
        tax_rate = get_validated_float("Enter Income Tax Rate (as decimal, e.g., 0.15): ", min_val=0.0)
        if tax_rate <= 1.0:
            return tax_rate
        print("Tax rate must be entered as a decimal (max 1.0). Please try again.")

# --- Payroll Calculation Function ---

def calculate_employee_pay(hours, rate, tax_rate):
    """
    Calculates and returns gross pay, income tax, and net pay.
    Using a tuple for return values minimizes lines of code (Part 2).
    """
    gross_pay = hours * rate
    income_tax = gross_pay * tax_rate
    net_pay = gross_pay - income_tax
    
    return gross_pay, income_tax, net_pay

# --- Final Processing and Display Functions (Part 3 & 4) ---

def display_employee_details(employee_data):
    """
    Displays all calculated and input data for a single employee in a formatted report.
    """
    print("\n" + "=" * 65)
    print(f"PAYROLL REPORT FOR: {employee_data['name'].upper()}")
    print("=" * 65)
    print(f"{'Pay Period:':<25} {employee_data['from_date']} - {employee_data['to_date']}")
    print(f"{'Total Hours Worked:':<25} {employee_data['hours']:,.2f}")
    print(f"{'Hourly Rate:':<25} ${employee_data['rate']:,.2f}")
    print("-" * 65)
    print(f"{'Gross Pay:':<25} ${employee_data['gross_pay']:,.2f}")
    print(f"{'Income Tax Rate:':<25} {employee_data['tax_rate'] * 100:.2f}%")
    print(f"{'Income Tax Withheld:':<25} ${employee_data['income_tax']:,.2f}")
    print(f"{'Net Pay:':<25} ${employee_data['net_pay']:,.2f}")
    print("=" * 65)

def process_all_employees(employee_list):
    """
    Reads list(s), calculates pay, displays details, and stores grand totals in a dictionary.
    """
    grand_totals = {
        'total_employees': 0,
        'total_hours': 0.0,
        'total_gross_pay': 0.0,
        'total_tax': 0.0,
        'total_net_pay': 0.0
    }

    print("\n\n" + "#" * 70)
    print("        *** INDIVIDUAL EMPLOYEE PAYROLL REPORTS ***")
    print("#" * 70)
    
    for employee in employee_list:
        # Calculate the income tax and net pay (Part 3.1)
        gross_pay, income_tax, net_pay = calculate_employee_pay(
            employee['hours'], employee['rate'], employee['tax_rate']
        )
        
        # Add calculated values to the employee dictionary
        employee['gross_pay'] = gross_pay
        employee['income_tax'] = income_tax
        employee['net_pay'] = net_pay
        
        # Display the employee details (Part 3.2)
        display_employee_details(employee)
        
        # Increment the grand totals (Part 3.3)
        grand_totals['total_employees'] += 1
        grand_totals['total_hours'] += employee['hours']
        grand_totals['total_gross_pay'] += gross_pay
        grand_totals['total_tax'] += income_tax
        grand_totals['total_net_pay'] += net_pay
        
    return grand_totals

# 4. Modified function that displays totals reading from a dictionary
def display_grand_totals(totals_dict):
    """
    Displays the summary of all processed employees and their financial totals
    by reading data from the provided dictionary object.
    """
    print("\n" + "*" * 70)
    print("                 *** GRAND TOTALS SUMMARY ***")
    print("*" * 70)
    
    if totals_dict['total_employees'] == 0:
        print("No employee data was processed.")
        print("*" * 70)
        return

    print(f"{'Total Number of Employees:':<30} {totals_dict['total_employees']}")
    print(f"{'Total Hours Worked:':<30} {totals_dict['total_hours']:,.2f}")
    print("-" * 70)
    print(f"{'Total Gross Pay:':<30} ${totals_dict['total_gross_pay']:,.2f}")
    print(f"{'Total Tax Withheld:':<30} ${totals_dict['total_tax']:,.2f}")
    print(f"{'Total Net Pay:':<30} ${totals_dict['total_net_pay']:,.2f}")
    print("*" * 70)

# --- Main Application Logic ---

def main():
    """
    Main function containing the input loop and final processing calls.
    """
    # 2. Storage for employee records (List of Dictionaries)
    employee_records = [] 
    
    print("-" * 50)
    print("Welcome to the Modular Payroll System")
    print("-" * 50)
    
    while True:
        
        # Employee Name is the loop termination condition
        name = get_employee_name()
        if name == 'End':
            break

        # 1. Get Dates (First function call in the loop)
        from_date, to_date = get_dates()
        
        # Get remaining input data
        hours = get_total_hours()
        rate = get_hourly_rate()
        tax_rate = get_income_tax_rate()
        
        # 2. Store all input data in a list object (as a dictionary)
        employee_records.append({
            'from_date': from_date,
            'to_date': to_date,
            'name': name,
            'hours': hours,
            'rate': rate,
            'tax_rate': tax_rate
        })
        
        print("\nEmployee data recorded. Ready for next employee.")

    # 3. Process all data after the user terminates the loop
    if employee_records:
        grand_totals_data = process_all_employees(employee_records)
        
        # 4. Display grand totals from the dictionary
        display_grand_totals(grand_totals_data)
    else:
        print("\nNo employee records entered.")
        
    print("\nApplication session finished.")

if __name__ == "__main__":
    main()
