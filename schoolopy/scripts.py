import os
import pandas as pd
import schoolopy

schoology = schoolopy.Schoology(schoolopy.Auth(consumer_key = os.environ['schoology_consumer_key'], consumer_secret = os.environ['schoology_consumer_secret']))

schoology.start = 0
schoology.limit = 200

def getAllItems(functionCallAsString, objectName):
    import math
    schoology.start = 0
    results = eval(functionCallAsString)
    items = results[objectName]
    if 'total' in results.keys():
        total = int(results['total'])
        iterations =  math.ceil((total - len(items))/schoology.limit)
        if iterations > 5:
            from tqdm import tqdm
            for i in tqdm(range(0, iterations)):
                schoology.start = schoology.start + schoology.limit
                results = eval(functionCallAsString)
                items.extend(results[objectName])
        else:
            for i in range(0, iterations):
                schoology.start = schoology.start + schoology.limit
                results = eval(functionCallAsString)
                items.extend(results[objectName])
    return pd.DataFrame(items)
    

def getAllSchools():
    
    return getAllItems('schoology.get_schools()', 'school')

def getAllBuildings(school_id):
    
    return getAllItems('schoology.get_buildings(' + str(school_id) + ')', 'building')

def getAllCourses():
    
    return getAllItems('schoology.get_courses()', 'course')

def getAllSections(course_id, include_past = 0):
    
    return getAllItems('schoology.get_sections(' + str(course_id) + ', include_past = ' + str(include_past) + ')', 'section')

def getAllUsers(building_id = None, role_ids = None, parent_access_codes = None, school_uids = None):
    
    return getAllItems('schoology.get_users(' + str(building_id) + ', ' + str(role_ids) + ', ' + str(parent_access_codes) + ', ' +  str(school_uids) + ')',   'user')

def getAllInactiveUsers():
    
    return getAllItems('schoology.get_inactive_users()', 'user')
    
def getAllRoles():
    
    return getAllItems('schoology.get_roles()', 'role')