import pymongo
from pymongo import MongoClient, errors
from pprint import pprint
import getpass
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu
from datetime import datetime
from validators import *
from pprint import pprint




def add(db):
    """
    Present the add menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(db):
    """
    Present the delete menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(db):
    """
    Present the list menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


def add_department(db):
    """
    Add a new student, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    students collection.  Theoretically, we could query MongoDB to find
    the uniqueness constraints in place, and use that information to
    dynamically decide what searches we need to do to make sure that
    we don't violate any of the uniqueness constraints.  Extra credit anyone?
    :param collection:  The pointer to the students collection.
    :return:            None
    """

    valid_department = False
    collection = db["departments"]
    while not valid_department:

        name = input("Department name--> ")
        abbreviation = input("Department abbreviation--> ")
        chair_name = input("Department chair name--> ")
        building = input("Department building--> ")
        office = int(input("Department Office--> "))
        description = input("Department description--> ")

        # Create a new departmental document prior to of storing it.
        department = {
            "name": name,
            "abbreviation": abbreviation,
            "chair_name": chair_name,
            "building": building,
            "office": office,
            "description": description
        }
        try:
            collection.insert_one(department)
            valid_department = True
        except Exception as exception:
            print("We received the following exception due to a poor input:")
            pprint(exception)
            print("Please input your values again.")


def select_department(db):
    """
    Select a student by the combination of the last and first.
    :param db:      The connection to the database.
    :return:        The selected student as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Student document from
                    the database.
    """
    # Create a connection from this database to the students' collection.
    collection = db["departments"]
    found: bool = False
    name: str = ''
    abbreviation: str = ''
    while not found:
        name = input("Department's name--> ")
        abbreviation = input("Department's abbreviation--> ")
        name_count: int = collection.count_documents({"name": name, "abbreviation": abbreviation})
        found = name_count == 1
        if not found:
            print("No department found by that name and abbreviation.  Try again.")
    found_department = collection.find_one({"name": name, "abbreviation": abbreviation})
    return found_department


def delete_department(db):
    """
    Delete a department from the database.
    :param db: The current database connection.
    :return: None
    """
    # Ask the department abbreviation from the user.
    department_abbreviation = input("Enter the department abbreviation: ")

    # Make a "pointer" in the database that points to the courses collection.
    courses = db["courses"]

    # Verify if the department offers any courses.
    existing_courses = courses.find({'department_abbreviation': department_abbreviation})

    # Get the count by using count_documents.
    courses_count = courses.count_documents({'department_abbreviation': department_abbreviation})

    if courses_count > 0:
        print("Cannot delete the department. There are existing courses in this department.")
    else:
        # Make a "pointer" in the database to the major's collection.
        majors = db["majors"]

        # Verify if the department offers any majors.
        existing_majors = majors.find({'department_abbreviation': department_abbreviation})

        # Get the count by using count_documents.
        majors_count = majors.count_documents({'department_abbreviation': department_abbreviation})

        if majors_count > 0:
            print("Cannot delete the department. There are existing majors in this department.")
        else:
            # Make a "pointer" in the database to the department's collection.
            departments = db["departments"]

            # If there are no majors or courses available, delete the department.
            deleted = departments.delete_one({'abbreviation': department_abbreviation})

            # For other items, the deleted variable document indicates the number of documents that were removed.
            print(f"We just deleted: {deleted.deleted_count} departments.")


def list_department(db):
    """
    List all of the students, sorted by last name first, then the first name.
    :param db:  The current connection to the MongoDB database.
    :return:    None
    """
    # No real point in creating a pointer to the collection, I'm only using it
    # once in here.  The {} inside the find simply tells the find that I have
    # no criteria.  Essentially this is analogous to a SQL find * from students.
    # Each tuple in the sort specification has the name of the field, followed
    # by the specification of ascending versus descending.
    departments = db["departments"].find({}).sort([("name", pymongo.ASCENDING),
                                                   ("abbreviation", pymongo.ASCENDING)])
    # pretty print is good enough for this work.  It doesn't have to win a beauty contest.
    for department in departments:
        pprint(department)


def validating_time():
    valid_time = False
    while not valid_time:
        time_input = input("Starting time: ")
        if len(time_input) != 7 and len(time_input) != 8:
            print("Invalid input. input structure similar to this -> '5:30 PM'.")
        else:
            if time_input[1] == ":":
                if time_input[5:] == "PM":
                    if int(time_input[0]) == 7 and int(time_input[2:4]) > 30:
                        print("Invalid Input. Class cannot start after 7:30PM")
                        continue
                    elif int(time_input[0]) > 7:
                        print("Invalid input. Class cannot start after 7:30PM")
                        continue
                    elif int(time_input[2:4]) > 59:
                        print("Invalid input. Minutes are incorrect")
                        continue
                    valid_time = True
                else:
                    if int(time_input[0]) < 8:
                        print("Invalid input. Class cannot start before 8:00AM")
                        continue
                    elif int(time_input[2:4]) > 59:
                        print("Invalid input. Minutes are incorrect")
                        continue
                    valid_time = True
            elif time_input[2] == ":":
                if time_input[6:] == "PM":
                    print("Invalid input. Class cannot start after 7:30PM")
                    continue
                else:
                    if (int(time_input[0:2]) > 12):
                        print("Invalid input. Hours are incorrect")
                        continue
                    elif int(time_input[3:5]) > 59:
                        print("Invalid input. Minutes are incorrect")
                        continue
                    valid_time = True
            else:
                print("Invalid input. Input structure similar to this -> '5:30 PM'.")

    return time_input


def add_section(db):

    # gain access to the collection of sections:
    collection_departments = db["departments"]
    collection_course = db["courses"]

    collection = db["sections"]
    valid_section = False

    while not valid_section:

        department_abbreviation = input("Department abbreviation: ")
        department = collection_departments.find_one({"abbreviation": department_abbreviation})
        if not department:
            print(f"Department with abbreviation {department_abbreviation} does not exist. Try again.")
            continue
        course_number = int(input("Course Number: "))
        course = collection_course.find_one({"course_number": course_number})
        if not course:
            print(f"Course in {department_abbreviation} with number {course_number} does not exist.")
            continue
        section_number = int(input("Section Number: "))
        semester = input("Semester: ")
        section_year = int(input("Section year: "))
        building = input("Building name: ")
        room = int(input("Room number: "))
        schedule = input("Schedule(Days): ")
        start_time = validating_time()
        instructor = input("Instructor name: ")

        section = {
            "department_abbreviation": department_abbreviation,
            "course_number": course_number,
            "section_number": section_number,
            'semester': semester,
            'section_year': section_year,
            'building': building,
            'room': room,
            'schedule': schedule,
            'start_time': start_time,
            'instructor': instructor,
            'student_references': [],
        }

        try:
            collection.insert_one(section)
            valid_section = True
        except Exception as exception:
            print("We received the following exception due to a poor input:")
            pprint(exception)
            print("Please input your values again.")


def select_section(db):
    collection = db["sections"]
    found = False
    abbr = ''
    c_num = ''
    s_num = ''
    semester = ''
    year = ''
    while not found:
        abbr = input("Department abbreviation: ")
        c_num = int(input("Course Number: "))
        s_num = int(input("Section Number: "))
        semester = input("Semester: ")
        year = int(input("Section year: "))
        count = collection.count_documents(
            {"department_abbreviation": abbr, "course_number": c_num, "section_number": s_num,
             "semester": semester, "section_year": year})
        found = count == 1
        if not found:
            print("No section found with the given attributes. Try again.")
    found_section = collection.find_one(
        {"department_abbreviation": abbr, "course_number": c_num, "section_number": s_num,
         "semester": semester, "section_year": year})
    return found_section


def delete_section(db):
    section = select_section(db)
    collection = db["sections"]
    if len(section["student_references"]) > 0:
        print("There are still students enrolled in this section. Delete those enrollments first")
        return

    deleted = collection.delete_one({"_id": section["_id"]})
    print(f"We just deleted: {deleted.deleted_count} sections.")


def list_section(db):
    sections = db["sections"].find({}).sort([("department_abbreviation", pymongo.ASCENDING),
                                             ("course_number", pymongo.ASCENDING),
                                             ("section_number", pymongo.ASCENDING),
                                             ("semester", pymongo.ASCENDING),
                                             ("section_year", pymongo.ASCENDING)])
    for section in sections:
        pprint(section)


def add_enrollment(db):
    # access the collection containing the enrollment item.
    collection = db['students']

    # collect data about students
    student = select_student(db)

    # collect the details for the part that the student will be registered in.
    section = select_section(db)
    section_details = {
        "department_abbreviation": section['department_abbreviation'],
        "course_number": section['course_number'],
        "section_number": section['section_number'],
        "semester": section['semester'],
        "section_year": section['section_year']
    }

    # Verify whether someone is enrolled in the same course and semester already.
    for enrollment in student.get("enrollments", []):
        if (enrollment.get("section_details", {}).get("department_abbreviation") == section[
            'department_abbreviation'] and
                enrollment.get("section_details", {}).get("course_number") == section['course_number'] and
                enrollment.get("section_details", {}).get("semester") == section['semester'] and
                enrollment.get("section_details", {}).get("section_year") == section['section_year']):
            print(
                "The student is already registered for the specified year and semester in this course. Not allowed to enroll in two different course sections.")
            return

    # assemble some enrollment-related information
    enrollment_type = input("(string) Choose an enrollment type (letter_grade / pass_fail): ")
    while enrollment_type not in ['letter_grade', 'pass_fail']:
        enrollment_type = input("Not a valid choice. (letter_grade / pass_fail): ")

    enrollments = {
        "type": enrollment_type,
        "section_details": section_details
    }
    # Provide further details according to the chosen registration type.
    # Add a min_satisfactory letter grade if letter grade type
    # If the type is pass_fail, include the enrollment application date.
    if enrollment_type == "letter_grade":
        letter_grade = input("Specify the minimum letter grade to pass (A/B/C): ")
        enrollments["letter_grade"] = {"min_satisfactory": letter_grade}
    elif enrollment_type == "pass_fail":
        application_date = ''
        valid_date = False
        while not valid_date:
            application_date = input("Specify the Pass/Fail application date (YYYY-MM-DD): ")

            # PRESENT DATE <= TODAY AND TO Verify DATE FORMAT
            try:
                application_date = datetime.strptime(application_date, '%Y-%m-%d').date()
                if application_date > datetime.today().date():
                    print("Application date must be on or before today's date.")
                    raise Exception
                valid_date = True
            except ValueError as ve:
                print("Invalid date/format")
                pprint(ve)
            except Exception as e:
                print("Something went wrong. Try again")
                pprint(e)

        enrollments["pass_fail"] = {"application_date": application_date.strftime('%Y-%m-%d')}

    # After obtaining our objects, we must locate the student to whom we are
    # adding the enrollment using the data we first collected about them,
    #  then add the enrollment and update the student's record.
    try:
        update_result = collection.update_one(
            # performs the update of the students object's enrollment object
            {"first_name": student['first_name'], 'last_name': student['last_name'], 'email': student['email']},
            {"$push": {"enrollments": enrollments}}
        )

        collection = db['sections']
        collection.update_one({
            "department_abbreviation": section['department_abbreviation'],
            "course_number": section['course_number'],
            "section_number": section['section_number'],
            "semester": section['semester'],
            "section_year": section['section_year']
        },
            {"$push": {"student_references": student['_id']}})

        if update_result.matched_count == 0:  # If the student object is located, this ought to equal 1.
            print("No matching student found. Check student details entered")
        elif update_result.modified_count == 0:  # If something was added or changed, then this should equal 1. If it equals 0, then duplicates caused an error.
            print("Enrollment data was not added. Duplicate information error")
        else:
            print("Enrollment was added successfully")
    except Exception as exception:
        print("Error adding enrollment. Make sure that you enter either A, B, or C for a minimum letter grade to pass")
        pprint(exception)


def list_section_student(db):
    collection = db['students']
    section = select_section(db)

    refs = section["student_references"]
    if not len(refs):
        print("This section has no students.")
    else:
        for id in refs:
            student = collection.find_one({"_id": id})
            print(f"Name: {student['first_name']}, {student['last_name']}\n   Email: {student['email']}")


def list_student_section(db):
    collection = db['students']

    first_name: str = ''
    last_name: str = ''
    email: str = ''

    # obtain some background data about the student
    print("Give student details to list their enrollments")
    first_name = input("Student's first name: ")
    last_name = input("Student's last name: ")
    email = input("Student's email: ")

    # Locate the student among the collection.
    student = collection.find_one(
        {"first_name": first_name, "last_name": last_name, "email": email}
    )

    # Check now to see if the pupil was located.
    if student:
        print(f"\nListing enrollments for {first_name}  {last_name} ({email}):")
        enrollments = student.get('enrollments', [])
        if enrollments:
            for i, enrollment in enumerate(enrollments, 1):
                print(f"\nEnrollment {i}:")
                for key, value in enrollment.items():
                    print(f"  {key}: {value}")
        else:
            print("No enrollments found for this student.")
    else:
        print("Student not found. Please check the entered details.")


def delete_enrollment(db):
    collection = db['students']

    # assemble some information on the student
    first_name = input("Student's first name: ")
    last_name = input("Student's last name: ")
    email = input("Student's email: ")

    # assemble information about the section to determine whose enrollment needs to be deleted.
    department_abbreviation = input("(string) Department abbreviation: ")
    course_number = int(input("(int) Course number: "))  # Convert to integer
    section_number = int(input("(int) Section number: "))  # Convert to integer
    semester = input("(string) Semester: ")
    section_year = int(input("(int) Section Year: "))  # Convert to integer

    # create the necessary section details object.
    section_details = {
        "department_abbreviation": department_abbreviation,
        "course_number": course_number,
        "section_number": section_number,
        "semester": semester,
        "section_year": section_year
    }

    # locate the student and remove that particular enrollment
    try:
        update_result = collection.update_one(
            {"first_name": first_name, "last_name": last_name, "email": email},
            {"$pull": {"enrollments": {"section_details": section_details}}}
        )

        student = collection.find_one(
            {"first_name": first_name, "last_name": last_name, "email": email}
        )

        collection = db['sections']
        collection.update_one({
            "department_abbreviation": department_abbreviation,
            "course_number": course_number,
            "section_number": section_number,
            "semester": semester,
            "section_year": section_year
        },
            {"$pull": {"student_references": student['_id']}})

        if update_result.matched_count == 0:  # check if student found
            print("No matching student found. Check the entered student details")
        elif update_result.modified_count == 0:  # check for enrollment (pulled out nothing)
            print("Enrollment data was not found or not removed.")
        else:  # success
            print("Enrollment was deleted successfully.")
    except Exception as exception:
        print("Error deleting enrollment")
        pprint(exception)


def add_student_major(db):
    # get to the collection
    collection = db['students']

    valid_addition = False
    while not valid_addition:
        student = select_student(db)
        major = select_major(db)
        declaration_date = input("Enter declaration date of the major (YYYY-MM-DD): ")

        valid_date = False
        while not valid_date:
            try:
                declaration_date = datetime.strptime(declaration_date, '%Y-%m-%d').date()
                if declaration_date > datetime.today().date():
                    print("Declaration date must be on or before today's date.")
                    raise ValueError
                else:
                    valid_date = True
            except ValueError as ve:
                print("Invalid date format. Please use YYYY-MM-DD format.")
                pprint(ve)
                continue
            except Exception as e:
                pprint(e)
                continue


        # create the major object now
        adding_major = {
            "major_name": major['name'],
            "declaration_date": declaration_date.strftime('%Y-%m-%d')
        }

        # locate student if exists, and then add the major to it
        try:
            # if student already enrolled in the major
            if any(m['major_name'] == major['name'] for m in
                   student.get('student_majors', [])):  # checks for duplicate major
                print("This student already is enrolled in that major.")
                raise Exception

            # add the major to the student
            update_result = collection.update_one(
                {"first_name": student['first_name'], "last_name": student['last_name'], "email": student['email']},
                {"$push": {"student_majors": adding_major}}
            )
            if update_result.modified_count == 0:
                print("Student Major data was not added. Undefined error")
                raise Exception
            else:
                print("Student Major data was successfully added")
                valid_addition = True
        except errors.DuplicateKeyError as dke:
            print("Student is already inside this major")
            pprint(dke)
        except Exception as exception:
            print("Error adding major")
            pprint(exception)


def list_major_student(db):
    major = select_major(db)
    students = db['students']
    for student in students.find({}):
        major_count = len(student['student_majors'])
        for i in range(0, major_count):
            if student['student_majors'][i]['major_name'] == major['name']:
                print(f"Name: {student['first_name']}, {student['last_name']}\n   Email: {student['email']}")


def list_student_major(db):
    student = select_student(db)
    major_count = len(student['student_majors'])
    if major_count == 0:
        print("Student is undeclared")
        return
    for i in range(0, major_count):
        print(f"Major: {student['student_majors'][i]['major_name']}")
        print(f"  Declaration Date: {student['student_majors'][i]['declaration_date']}")


def delete_student_major(db):
    collection = db['students']
    print("Deleting student major...")

    valid_deletion = False
    while not valid_deletion:
        student = select_student(db)
        major_count = len(student['student_majors'])
        if major_count == 0:
            print("Student is undeclared")
            return

        major = select_major(db)
        try:
            update_result = collection.update_one(
                {"first_name": student['first_name'], "last_name": student['last_name'], "email": student['email']},
                {"$pull": {"student_majors": {"major_name": major['name']}}}
            )
            if update_result.modified_count == 0:
                print("Major data was not found or not removed.")
                raise Exception
            else:
                print("Major was deleted successfully.")
                valid_deletion = True
        except Exception as exception:
            print("Error deleting major")
            pprint(exception)


def add_student(db):
    valid_student = False
    collection = db["students"]
    while not valid_student:
        # Make a "pointer" in the database that points to the students' collection.
        unique_email_student: bool = False

        last_name: str = ''
        first_name: str = ''
        email: str = ''

        while not unique_email_student:
            last_name = input("Student last name--> ")
            first_name = input("Student first name--> ")

            email = input("Student email--> ")

            name_email_count: int = collection.count_documents(
                {"first_name": first_name, "last_name": last_name, "email": email})
            unique_email_student = name_email_count == 0
            if not unique_email_student:
                print("We already have a student by that name.  Try again.")

        # Create a new departmental document before putting it in storage.
        students = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "student_majors": [],
            "enrollments": []
        }
        try:
            collection.insert_one(students)
            valid_student = True
        except Exception as exception:
            print("We got the following exception from a bad input:")
            pprint(exception)
            print("Please re-enter your values")


def list_student(db):
    students = db["students"].find({}).sort([("first_name", pymongo.ASCENDING),
                                             ("last_name", pymongo.ASCENDING),
                                             ("email", pymongo.ASCENDING)])
    for student in students:
        print(f"Name: {student['first_name']}, {student['last_name']}\n   Email: {student['email']}")


def select_student(db):
    collection = db["students"]
    found: bool = False
    first_name: str = ''
    last_name: str = ''
    email: str = ''
    while not found:
        first_name = input("Student's first name--> ")
        last_name = input("Student's last name--> ")
        email = input("Student's email--> ")
        name_email_count: int = collection.count_documents(
            {"first_name": first_name, "last_name": last_name, "email": email})
        found = name_email_count == 1
        if not found:
            print("No student found by that name and email.  Try again.")
    found_student = collection.find_one(
        {"first_name": first_name, "last_name": last_name, "email": email})
    return found_student


def delete_student(db):
    student = select_student(db)
    students = db["students"]
    if len(student["enrollments"]) > 0:
        print("This student is still enrolled in at least one section. Delete those enrollments first")
        return
    deleted = students.delete_one({"_id": student["_id"]})
    print(f"We just deleted: {deleted.deleted_count} student(s).")


def add_major(db):
    valid_major = False
    majors_collection = db["majors"]
    departments_collection = db["departments"]

    while not valid_major:
        # Find out whether the department has an abbreviation by asking for it.
        department_abbreviation = input("Department abbreviation--> ")
        name = input("Major name--> ")
        description = input(f"Description for {name}--> ")

        # Verify the department's existence.
        department_exists = departments_collection.count_documents({'abbreviation': department_abbreviation}) > 0

        major = {
            "name": name,
            "department_abbreviation": department_abbreviation,
            "description": description
        }

        try:
            if not department_exists:
                print("Department does not exist.")
                raise Exception

            majors_collection.insert_one(major)
            print("Successfully added major.")
            valid_major = True
        except errors.DuplicateKeyError as exception:
            print("This major already exists in this department")
            pprint(exception)
        except Exception as exception:
            print("An error occurred, please re-enter your values")
            pprint(exception)


def delete_major(db):
    # To pick the major to be deleted, use the select_major method.
    selected_major = select_major(db)

    valid_major = False
    while not valid_major:
        if selected_major:
            collection = db["majors"]
            deleted = collection.delete_one({"_id": selected_major["_id"]})
            print(f"We just deleted: {deleted.deleted_count} major(s)")
            valid_major = True
        else:
            print("No major found.")


def list_major(db):
    collection = db["majors"]
    majors = collection.find({}).sort([("department_abbreviation", pymongo.ASCENDING),
                                       ("name", pymongo.ASCENDING)])
    try:
        for major in majors:
            print(f"{major['department_abbreviation']} - {major['name']}")
    except KeyError as ve:
        print("A property was searched for that does not exist")
        pprint(ve)


def add_course(db):
    collection_courses = db["courses"]
    collection_departments = db["departments"]
    valid_course = False

    while not valid_course:
        try:
            department_abbreviation = input("Department abbreviation: ")

            # Verify the department's existence.
            department = collection_departments.find_one({"abbreviation": department_abbreviation})
            if not department:
                print(f"Department with abbreviation {department_abbreviation} does not exist. Try again.")
                return

            course_number = int(input("Course number: "))
            name = input("Course name: ")
            description = input("Course description: ")
            units = int(input("Course units: "))

            # Create course
            course = {
                "department_abbreviation": department_abbreviation,
                "course_number": course_number,
                "name": name,
                "description": description,
                "units": units
            }

            # Insert course
            collection_courses.insert_one(course)

            print("Course added successfully!")
            valid_course = True

        except ValueError as ve:
            print("Invalid input. Please enter valid values.")
            pprint(f"Error: {ve}")
        except errors.DuplicateKeyError as dke:
            print("Duplicate course. New course must be unique")
            pprint(dke)
        except Exception as e:
            print("An unexpected error occurred. Please try again.")
            pprint(f"Error: {e}")


def select_course(db):
    # Obtain the collection of "courses"
    courses = db["courses"]

    valid_course = False
    while not valid_course:
        # assemble data on the course
        department_abbreviation = input("Enter the department abbreviation: ")
        course_number = int(input("Enter the course number: "))

        # Using the course number and department abbreviation supplied, locate the course.
        try:
            course = courses.find_one({
                'department_abbreviation': department_abbreviation,
                'course_number': course_number
            })
            if course:
                return course
            else:
                print("No matching course found. Please try again.")
        except Exception as e:
            print("Error, Try again")
            pprint(e)


def delete_course(db):
    courses = db["courses"]

    # Request the course number and department abbreviation from the user.
    department_abbreviation = input("Enter the department abbreviation: ")
    course_number = input("Enter the course number: ")

    # Check if the course exists
    existing_course = courses.find_one({
        'department_abbreviation': department_abbreviation,
        'course_number': int(course_number)  # Convert to integer
    })

    if existing_course:
        sections_count = db["sections"].count_documents({
            'department_abbreviation': department_abbreviation,
            'course_number': int(course_number)
        })

        if sections_count > 0:
            print("Cannot delete the course. There are existing sections for this course.")
        else:
            # Delete the course if no sections are found
            courses.delete_one({
                'department_abbreviation': department_abbreviation,
                'course_number': int(course_number)
            })
            print(f"Course '{department_abbreviation} {course_number}' deleted successfully.")
    else:
        print(f"Course '{department_abbreviation} {course_number}' not found.")


def list_course(db):
    # Get the "courses" collection
    courses = db["courses"]

    # Ask the user for the department abbreviation
    department_abbreviation = input("Enter the department abbreviation: ")

    # Find and list all courses in the specified department
    department_courses = courses.find({'department_abbreviation': department_abbreviation})

    # Using count_documents to get the count
    courses_count = courses.count_documents({'department_abbreviation': department_abbreviation})

    if courses_count == 0:
        print(f"No courses found for department '{department_abbreviation}'.")
    else:
        print(f"Courses in department '{department_abbreviation}':")
        for course in department_courses:
            print(f"{course['department_abbreviation']} {course['course_number']}: {course['name']}")


def boilerplate(db):

    collection = db['departments']
    department = {
        'name': "Computer Engineering and Computer Science",
        'abbreviation': "CECS",
        'chair_name': "Jack",
        'building': "VEC",
        'office': 100,
        'description': "This is Comp Eng and Comp Sci"
    }
    collection.insert_one(department)

    collection = db['majors']
    major = {
        'name': "Computer Science",
        'department_abbreviation': "CECS",
        'description': "Computer science focuses on the development and testing of software."
    }
    collection.insert_one(major)

    collection = db['courses']
    course = {
        'department_abbreviation': "CECS",
        'course_number': 425,
        'name': "AI",
        'description': "Artificial intelligence",
        'units': 3,
    }
    collection.insert_one(course)

    collection = db['students']
    student_majors = {
        'major_name': "Computer Science",
        'declaration_date': "2024-10-01"
    }

    section_details = {
        'department_abbreviation': "CECS",
        'course_number': 425,
        'section_number': 3,
        'semester': "Fall",
        'section_year': 2023,
    }

    enrollment = {
        'type': "letter_grade",
        'section_details': section_details
    }
    students = {
        'first_name': "Jorge",
        'last_name': "Mejia",
        'email': "jorgemejia@mail.com",
        'enrollments': [enrollment],
        'student_majors': [student_majors]
    }
    collection.insert_one(students)

    collection = db['sections']
    student_references = []
    section = {
        'department_abbreviation': "CECS",
        'course_number': 425,
        'section_number': 3,
        'semester': "Fall",
        'section_year': 2023,
        'building': "VEC",
        'room': 326,
        'schedule': "MW",
        'start_time': "6:50 PM",
        'instructor': "Steven Gold",
        'student_references': student_references
    }
    collection.insert_one(section)


def select_major(db):
    collection = db["majors"]
    found = False
    department_abbreviation = ''
    major_name = ''

    while not found:

        department_abbreviation = input("Department abbreviation --> ")
        major_name = input("Major name --> ")

        count = collection.count_documents({"department_abbreviation": department_abbreviation, "name": major_name})
        found = count == 1
        if not found:
            print(
                f"No major found with the department abbreviation '{department_abbreviation}' and name '{major_name}'. Try again.")

    found_major = collection.find_one({"department_abbreviation": department_abbreviation, "name": major_name})
    return found_major


if __name__ == '__main__':
    password: str = input('Mongo DB password -->')
    username: str = input('Database username [username] -->')
    project: str = input('Mongo project name [cecs-323-fall] -->')
    hash_name: str = input('7-character database hash [qurrflj] -->')

    cluster = f"mongodb+srv://{username}:{password}@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority"
    print(f"Cluster: mongodb+srv://{username}:********@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority")
    client = MongoClient(cluster)
    print(client.list_database_names())
    db = client["TermProject"]
    print(db.list_collection_names())

    students = db['students']
    majors = db['majors']
    sections = db['sections']
    courses = db["courses"]
    departments = db["departments"]

    print("Would you like to: \n1. Use an existing collection \n2. Start from scratch")
    choice = int(input("Choice: "))
    if choice == 2:

        if "students" in db.list_collection_names():
            print("dropping the students collection.")
            students.drop()
        if "majors" in db.list_collection_names():
            print("dropping the majors collection.")
            majors.drop()
        if "courses" in db.list_collection_names():
            print("dropping the courses collection.")
            courses.drop()
        if "sections" in db.list_collection_names():
            print("dropping the sections collection.")
            sections.drop()
        if "departments" in db.list_collection_names():
            print("dropping the departments collection.")
            departments.drop()

        # db.create_collection('students', check_exists=True)
        print(db.create_collection("students", **students_validator))
        students.create_index(
            [('first_name', pymongo.ASCENDING), ('last_name', pymongo.ASCENDING), ('email', pymongo.ASCENDING)],
            unique=True, name='unique_name_email')
        students_indexes = students.index_information()

        # db.create_collection('majors', check_exists=True)
        print(db.create_collection("majors", **majors_validator))
        majors.create_index(
            [('name', pymongo.ASCENDING)],
            unique=True, name='unique_major')

        # db.create_collection('sections', check_exists=True)
        print(db.create_collection('sections', **sections_validator))
        sections.create_index(
            [('course_number', pymongo.ASCENDING), ('section_number', pymongo.ASCENDING),
             ('semester', pymongo.ASCENDING),
             ('section_year', pymongo.ASCENDING)],
            unique=True, name="courseNumber_sectionNumber_semester_sectionYear")
        sections.create_index(
            [('building', pymongo.ASCENDING), ('room', pymongo.ASCENDING), ('semester', pymongo.ASCENDING),
             ('section_year', pymongo.ASCENDING), ('schedule', pymongo.ASCENDING), ("start_time", pymongo.ASCENDING)],
            unique=True, name="building_room_semester_sectionYear_starTime_schedule")
        sections.create_index(
            [('instructor', pymongo.ASCENDING), ('semester', pymongo.ASCENDING),
             ('section_year', pymongo.ASCENDING), ('schedule', pymongo.ASCENDING), ("start_time", pymongo.ASCENDING)],
            unique=True, name="instructor_semester_sectionYear_starTime_schedule")

        # db.create_collection('courses', check_exists=True)
        print(db.create_collection("courses", **courses_validator))
        courses.create_index([('department_abbreviation', pymongo.ASCENDING), ('course_number', pymongo.ASCENDING)],
                             unique=True, name="departmentAbbreviation_courseNumber")
        courses.create_index([('department_abbreviation', pymongo.ASCENDING), ('name', pymongo.ASCENDING)],
                             unique=True, name="departmentAbbreviation_courseName")

        # db.create_collection('departments', check_exists=True)
        print(db.create_collection('departments', **departments_validator))
        departments.create_index([('abbreviation', pymongo.ASCENDING)], unique=True, name="departments_abbreviations")
        departments.create_index([('chair_name', pymongo.ASCENDING)], unique=True, name='departments_chair_names')
        departments.create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)],
                                 unique=True, name="departments_buildings_and_offices")
        departments.create_index([('name', pymongo.ASCENDING)], unique=True, name="departments_names")

    # main menu running
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)