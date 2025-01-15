<%def name="radios(name, options)">\
% for option in options:
<div><input type="radio" name="${name}" id="${name + option}" value="${option}"><label for="${name + option}">${option}</label></div>
% endfor
</%def>\
# Demographics Form

1. Are you Hispanic or Latin(x)?

    ${radios("hispanic", ["Yes", "No"])}

2. With which racial category or categories do you most closely identify:

    ${radios("racialCategories", ["American Indian / Alaskan Native", "Asian", "Black or African American", "Native Hawaiian or Other Pacific Islander", "White", "Multiracial"])}

    If you picked "Multiracial", please note which categories you identify with: <input type="text" name="racialCategoriesMultiracial">

3. With which gender identity do you most closely identify:

    ${radios("gender", ["Male", "Female", "Non-binary or gender non-confirming", "Prefer not to say", "Prefer to self describe"])}

    If you picked "Prefer to self describe", please describe here: <input type="text" name="genderSelfDescribe">

4. Are you left or right-handed?

    ${radios("handedness", ["Left-handed", "Right-handed"])}

5. What is your academic year?

    ${radios("academicYear", ["Freshman", "Sophomore", "Junior", "Senior"])}

6. What is your birthdate (mm/dd/yyyy)?

    <input type="text" name="birthdate">

7. What was the highest level of math that you took in high school?

    ${radios("mathLevel", ["Algebra", "Geometry with an algebra prerequisite", "Pre-calculus or trigonometry", "Calculus", "Other (please specify)"])}

8. What is your **college** major / minor? (Indicate more than one if applicable.)

    <input type="text" name="majorMinor">

9. List your **past semester** colleges courses (designators and numbers) in mathematics?

    <textarea name="pastSemesterCourses" cols="80" rows="20"></textarea>

10. List your **current semester** colleges courses (designators and numbers) in mathematics?

    <textarea name="currentSemesterCourses" cols="80" rows="20"></textarea>
