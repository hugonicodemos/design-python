"""List Comprehensions Lesson.

Link: https://classroom.udacity.com/courses/cs212/lessons/48703331/concepts/487282070923 # NOQA
"""

udactiy_tas = ['peter', 'andy', 'sarah', 'gundega', 'job', 'sean']
bad_uppercase_tas = [name.upper() for name in udactiy_tas]

# for i in range(len(udactiy_tas)):
#    bad_uppercase_tas.append(udactiy_tas[i].upper())

ta_data = [('Peter', 'USA', 'CS262'),
           ('Andy', 'USA', 'CS212'),
           ('Sarah', 'England', 'CS101'),
           ('Gundega', 'Latvia', 'CS373'),
           ('Job', 'USA', 'CS387'),
           ('Sean', 'USA', 'CS253')]

ta_facts = [name + ' lives in ' + country + ' and is the TA for ' +
            course for name, country, course in ta_data]

remote_ta_facts = [name + ' lives in ' + country + ' and is the TA for ' +
                   course for name, country, course in ta_data
                   if country != 'USA']

ta_300 = [name + ' is the TA for ' + course for name, country, course
          in ta_data if course.find('3') == 2]

print ta_300
