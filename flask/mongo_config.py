from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

from SQLA_config import Students, Locations, EO, Tests

mongo_client = MongoClient('mongodb://mongodb:27017/')

db = mongo_client.data_base

# 'postgresql+psycopg2://user:password@hostname/database_name'
psql_engine = create_engine("postgresql+psycopg2://postgres:314159265@data_base/data_base")
Session = sessionmaker(bind=psql_engine)
session = Session()

locations_collection = db.locations
eo_collection = db.eo
students_collection = db.students
tests_collection = db.tests


def fix_decimal_problem(column_value):
    return float(column_value) if isinstance(column_value, Decimal) else column_value


def fix_region_space_problem(region):
    return region + " область" if (region != "м.Київ") else region


class Config:

    def __init__(self):
        if locations_collection.count_documents({}) == 0:
            self.createStudentsCollection()
            self.createLocationsCollection()
            self.createEOCollection()
            self.createTestsCollection()

    # Create collections

    def createStudentsCollection(self):
        students_collection = db.students
        document_count = students_collection.count_documents({})
        if document_count == 0:
            for student in session.query(Students):
                student_data = {}
                for column in Students.__table__.columns:
                    column_name = column.name
                    column_value = getattr(student, column_name)
                    column_value = fix_decimal_problem(column_value)
                    student_data[column_name] = column_value
                students_collection.insert_one(student_data)

    def createLocationsCollection(self):
        locations_collection = db.locations
        document_count = locations_collection.count_documents({})
        if document_count == 0:
            for location in session.query(Locations):
                location_data = {}
                for column in Locations.__table__.columns:
                    column_name = column.name
                    column_value = getattr(location, column_name)
                    location_data[column_name] = column_value
                locations_collection.insert_one(location_data)

    def createEOCollection(self):
        eo_collection = db.eo
        document_count = eo_collection.count_documents({})
        if document_count == 0:
            for eo in session.query(EO):
                eo_data = {}
                for column in EO.__table__.columns:
                    column_name = column.name
                    column_value = getattr(eo, column_name)
                    eo_data[column_name] = column_value
                eo_collection.insert_one(eo_data)

    def createTestsCollection(self):
        tests_collection = db.tests
        document_count = tests_collection.count_documents({})
        if document_count == 0:
            for tests in session.query(Tests):
                tests_data = {}
                for column in Tests.__table__.columns:
                    column_name = column.name
                    column_value = getattr(tests, column_name)
                    column_value = fix_decimal_problem(column_value)
                    tests_data[column_name] = column_value
                tests_collection.insert_one(tests_data)

    # fetch rows

    def fetchRowsFromLocations(self):
        return self.listOfDictsToTuple(locations_collection.find({}, {"_id": 0}).sort("location_id").limit(10))

    def fetchRowsFromStudents(self):
        return self.listOfDictsToTuple(students_collection.find({}, {"_id": 0}).sort("student_id").limit(10))

    def fetchRowsFromEO(self):
        return self.listOfDictsToTuple(eo_collection.find({}, {"_id": 0}).sort("eo_id").limit(10))

    def fetchRowsFromTests(self):
        return tuple(self.listOfDictsToTuple(tests_collection.find({}, {"_id": 0}).sort("tests_id").limit(10)))

    # fetch by id

    def fetchLocationsById(self, location_id):
        return self.dictValuesToTuple(locations_collection.find_one({"location_id": location_id}, {"_id": 0}))

    def fetchStudentsById(self, students_id):
        return self.dictValuesToTuple(students_collection.find_one({"students_id": students_id}, {"_id": 0}))

    def fetchEOById(self, eo_id):
        return self.dictValuesToTuple(eo_collection.find_one({"eo_id": eo_id}, {"_id": 0}))

    def fetchTestsById(self, tests_id):
        return self.dictValuesToTuple(tests_collection.find_one({"tests_id": tests_id}, {"_id": 0}))

    # fetch tuples

    def fetchRegnames(self):
        return tuple(locations_collection.distinct("regname"))

    def fetchLocation(self, regname, areaname, tername, tertypename):
        query = db.locations.find_one(
            {"regname": regname, "areaname": areaname, "tername": tername, "tertypename": tertypename}, {"_id": 0})
        return self.dictValuesToTuple(query)

    def fetchTestsColumnNames(self):
        column_names = list(tests_collection.find_one().keys())
        column_names.remove('_id')
        return column_names

    # delete

    def deleteLocation(self, location_id):
        location_id = int(location_id)
        if locations_collection.find_one({"location_id": location_id}):
            locations_collection.delete_one({"location_id": location_id})

    def deleteStudent(self, outid):
        if students_collection.find_one({"outid": outid}):
            students_collection.delete_one({"outid": outid})

    def deleteEO(self, eo_id):
        eo_id = int(eo_id)
        if eo_collection.find_one({"eo_id": eo_id}, {"_id": 0}):
            eo_collection.delete_one({"eo_id": eo_id})

    def deleteTest(self, student_id):
        student_id = int(student_id)
        if tests_collection.find_one({"student_id": student_id}):
            tests_collection.delete_one({"student_id": student_id})

    # update

    def updateLocation(self, location_id, regname, areaname, tername, tertypename):
        location_id = int(location_id)
        if locations_collection.find_one({"location_id": location_id}):
            locations_collection.update_one({"location_id": location_id}, {
                "$set": {
                    "regname": regname,
                    "areaname": areaname,
                    "tername": tername,
                    "tertypename": tertypename
                }
            })

    def updateStudent(self, student_id, year_of_passing, outid, birth, sextypename, location_id, eo_id, tests_results_id):
        student_id = int(student_id)
        if students_collection.find_one({"student_id": student_id}):
            students_collection.update_one({"student_id": student_id}, {
                "$set": {
                    "year_of_passing": year_of_passing,
                    "outid": outid,
                    "birth": birth,
                    "sextypename": sextypename,
                    "location_id": location_id,
                    "eo_id": eo_id,
                    "tests_results_id": tests_results_id
                }
            })

    def updateEO(self, eo_id, eo_name, eo_type, location_id):
        eo_id = int(eo_id)
        if eo_collection.find_one({"eo_id": eo_id}):
            eo_collection.update_one({"eo_id": eo_id}, {
                "$set": {
                    "eo_name": eo_name,
                    "eo_type": eo_type,
                    "location_id": location_id
                }
            })

    def updateTest(self, tests_id, test_data):
        tests_id = int(tests_id)
        if tests_collection.find_one({"tests_id": tests_id}):
            update_query = {"$set": {}}
            for column_name, value in test_data.items():
                if column_name != "tests_id":
                    value = None if value == 'None' else value
                    update_query["$set"][column_name] = value
            tests_collection.update_one({"tests_id": tests_id}, update_query)

    # create

    def createLocation(self, location_id, regname, areaname, tername, tertypename):
        locations_collection.insert_one({
            "location_id": location_id,
            "regname": regname,
            "areaname": areaname,
            "tername": tername,
            "tertypename": tertypename
        })

    def createStudent(self, student_id, year_of_passing, outid, birth, sextypename, location_id, eo_id, tests_results_id):
        students_collection.insert_one({
            "student_id": student_id,
            "year_of_passing": year_of_passing,
            "outid": outid,
            "birth": birth,
            "sextypename": sextypename,
            "location_id": location_id,
            "eo_id": eo_id,
            "tests_results_id": tests_results_id
        })

    def createEO(self, eo_id, eo_name, eo_type, location_id):
        eo_collection.insert_one({
            "eo_id": eo_id,
            "eo_name": eo_name,
            "eo_type": eo_type,
            "location_id": location_id
        })

    def createTest(self, test_data):
        tests_collection.insert_one(test_data)

    def fetchGrade(self, year, regname, subject, function):

        regname = fix_region_space_problem(regname)

        pipeline = [
            {
                '$match': {
                    'year_of_passing': f'{year}'
                }
            },
            {
                '$lookup': {
                    'from': 'tests',
                    'localField': 'student_id',
                    'foreignField': 'student_id',
                    'as': 'tests'
                }
            },
            {
                '$lookup': {
                    'from': 'locations',
                    'localField': 'location_id',
                    'foreignField': 'location_id',
                    'as': 'location'
                }
            },
            {
                '$unwind': '$tests'
            },
            {
                '$match': {
                    'location.regname': f'{regname}',
                    'tests.math_tests_ball100': {'$exists': True}
                }
            },
            {
                '$group': {
                    '_id': None,
                    'max_math_score': {f'${function}': f'$tests.{subject}'}
                }
            }
        ]

        result = students_collection.aggregate(pipeline)
        grade = 0
        if result:
            for row in result:
                grade = row["grade"]
                return grade

        return grade

    def dictValuesToTuple(self, dict):
        return tuple([value for value in dict.values()])

    def listOfDictsToTuple(self, query_result):
        return tuple([self.dictValuesToTuple(dict) for dict in list(query_result)])
