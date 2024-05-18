

students_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': "object",
            'title': "students",
            'required': ["last_name", "first_name", "email"],
            'additionalProperties': False,
            'properties': {
                "_id": {},
                'last_name': {'bsonType': "string",
                              "minLength": 1,
                              },
                'first_name': {'bsonType': "string",
                               "minLength": 1,
                               },
                'email': {'bsonType': "string",
                          "minLength": 1,
                          },
                'enrollments': {
                    'bsonType': "array",
                    'items': {
                        'bsonType': "object",
                        'title': "enrollments",
                        'required': ["type", "section_details"],
                        'additionalProperties': False,
                        'properties': {
                            'type': {'enum': ["letter_grade", "pass_fail"]},
                            'section_details': {
                                'bsonType': "object",
                                'items': [
                                    {'bsonType': "string",
                                     "minLength": 1,
                                     },  # Considering that section_details's items are all strings

                                    {'bsonType': "int"},
                                    {'bsonType': "int"},
                                    {'bsonType': "string",
                                     "minLength": 1,
                                     },
                                    {'bsonType': "int"}
                                ],
                            },
                            'letter_grade': {
                                'bsonType': "object",
                                'title': "letter_grade",
                                'description': "must be an object if bsonType is letter_grade",
                                'additionalProperties': False,
                                # If necessary, specify the letter_grade's characteristics.
                                "properties": {
                                    "min_satisfactory": {
                                        'enum': ["A", "B", "C"],
                                        "description": "must be a string and is required if bsonType is letter_grade"
                                    }
                                }
                            },
                            'pass_fail': {
                                'bsonType': "object",
                                'title': "pass_fail",
                                'description': "must be an object if bsonType is pass_fail",
                                # If necessary, provide the characteristics of pass_fail.
                                'additionalProperties': False,
                                "properties": {
                                    "application_date": {
                                        "bsonType": "string",
                                        "description": "must be a string and is required if bsonType is pass_fail"
                                    }
                                }
                            }
                        }
                    }
                },
                'student_majors': {
                    'bsonType': "array",
                    'items': {
                        'bsonType': "object",
                        'title': "student_majors",
                        'required': ["major_name", "declaration_date"],
                        'additionalProperties': False,
                        'properties': {
                            'major_name': {'bsonType': "string",
                                           "minLength": 1,
                                           },
                            'declaration_date': {'bsonType': "string",
                                                 "minLength": 1,
                                                 }  # Consider that declaration_date is a string.
                        }
                    }
                }
            }
        }
    }
}


sections_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': "object",
            'title': "section",
            'required': ["department_abbreviation", "course_number", "section_number", "semester", "section_year",
                         "building", "room", "schedule", "start_time",
                         "instructor", "student_references"],
            'additionalProperties': False,
            'properties': {
                "_id": {},
                'department_abbreviation': {
                    'bsonType': "string",
                    "minLength": 1,
                    'description': "short identifier for department"
                },
                'course_number': {
                    'bsonType': "int",
                    'description': "must be an integer and is required"
                },
                'section_number': {
                    'bsonType': "int",
                    'description': "must be an integer and is required"
                },
                'semester': {
                    'enum': ["Fall", "Spring", "Summer I", "Summer II", "Summer III", "Winter"],
                    'description': "must be a string and is required"
                },
                'section_year': {
                    'bsonType': "int",
                    'description': "must be an integer and is required"
                },
                'building': {
                    'enum': ["ANAC", "CDC", "DC", "ECS", "EN2", "EN3", "EN4", "EN5", "ET", "HSCI", "NUR", "VEC"],
                    'description': "must be a string and is required"
                },
                'room': {
                    'bsonType': "int",
                    'minimum': 1,
                    'maximum': 999,
                    'description': "must be an integer and is required"
                },
                'schedule': {
                    'enum': ["MW", "TuTh", "MWF", "F", "S"],
                    'description': "must be a string and is required"
                },
                'start_time': {
                    'bsonType': "string",
                    "minLength": 1,
                    'description': "must be a string and is required"
                },
                'instructor': {
                    'bsonType': "string",
                    "minLength": 1,
                    'description': "must be a string and is required"
                },
                'student_references': {
                    'bsonType': "array",
                    'items': {
                        'bsonType': "objectId",
                        'description': "must be integers representing student IDs"
                    }
                }
            }
        }
    }
}



courses_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': "object",
            'title': "course",
            'required': ["department_abbreviation", "course_number", "name", "description", "units"],
            'additionalProperties': False,
            'properties': {
                "_id": {},
                'department_abbreviation': {
                    'bsonType': "string",
                    "minLength": 1,
                    'description': "must be a string and is required"
                },
                'course_number': {
                    'bsonType': "int",
                    'minimum': 100,
                    'maximum': 699,
                    'description': "must be an integer and is required"
                },
                'name': {
                    'bsonType': "string",
                    "minLength": 1,
                    'description': "must be a string and is required"
                },
                'description': {
                    'bsonType': "string",
                    "minLength": 1,
                    'description': "must be a string and is required"
                },
                'units': {
                    'bsonType': "int",
                    'minimum': 1,
                    'maximum': 5,
                    'description': "must be an integer and is required"
                }
            }
        }
    }
}

majors_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': "object",
            'title': "major",
            'required': ["name", "department_abbreviation", "description"],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'name': {
                    'bsonType': "string",
                    "minLength": 1,
                    'description': "must be a string and is required"
                },
                'department_abbreviation': {
                    'bsonType': "string",
                    "minLength": 1,
                    'description': "must be a string and is required, referring to the department offering the major"
                },
                'description': {
                    'bsonType': "string",
                    'description': "must be a string and is required",
                    "minLength": 1,
                    'maxLength': 80
                }
            }
        }
    }
}


departments_validator = {
                'validator': {
                    '$jsonSchema': {
                        'bsonType': "object",
                        'title': "department",
                        'required': ["name", "abbreviation", "chair_name", "building", "office", "description"],
                        'additionalProperties': False,
                        'properties': {
                            '_id': {},
                            'name': {
                                'bsonType': "string",
                                'minLength': 1,
                                "description": "The identifier of a department"
                            },
                            'abbreviation': {
                                'bsonType': "string",
                                'minLength': 1,
                                'maxLength': 6,
                                "description": "a short string identifying just one department"
                            },
                            'chair_name': {
                                'bsonType': "string",
                                'minLength': 1,
                                'maxLength': 80,
                                "description": "The person who is in charge of the department"
                            },
                            'building': {
                                'bsonType': "string",
                                'enum': ["ANAC", "CDC", "DC", "ECS", "EN2", "EN3", "EN4", "EN5", "ET", "HSCI", "NUR", "VEC"],
                                "description": "string name of the architecture where the department head office will be"
                            },
                            'office': {
                                'bsonType': "int",
                                'minimum': 1,
                                "description": "Integer value identifying the office"

                            },
                            'description': {
                                'bsonType': "string",
                                'minLength': 10,
                                'maxLength': 80,
                                "description": "A sentence describing the department"
                            }
                        }
                    }
                }
            }
