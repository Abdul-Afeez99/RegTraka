from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, GenericAPIView
from .serializers import (CourseSerializer, InstructorSerializer, ClassroomSerializer, StudentSerializer,
                          ListAllStudentInClassSerializer, IndividualInstructorSerializer, CreateClassroomSerializer)
from Users.models import Courses, Administrator, Instructor, Year, Student, Attendance, CustomUser
from rest_framework import permissions, response, status, serializers
from Users.permissions import IsAdministrator
from Users.serializers import UserSerializer
from Users.serializers import InstructorRegistrationSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from instructor.serializers import AttendanceSerializer

# Create your views here.

# get the administrator object
def getAdministratorObject(self,):
    user_obj = self.request.user
    school = Administrator.objects.get(user=user_obj)
    return school


# Get the current administrator information
class AdministratorInfoView(RetrieveAPIView):
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        administrator = Administrator.objects.filter(user=user)
        result = {}
        for info in administrator:
            result['name'] = info.name
            result['email'] = info.user.email
        return response.Response(result, status=status.HTTP_200_OK)

#create a new instructor
class InstructorRegistrationView(GenericAPIView):
    serializer_class = InstructorRegistrationSerializer
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
       
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return response.Response(
            user_data, status=status.HTTP_201_CREATED
        )   
    
# # Create a new course   
# class CourseCreateAPIView(CreateAPIView):
#     serializer_class = CreateCourseSerializer
#     queryset = Courses.objects.all()
#     permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
#     def perform_create(self, serializer):
#         school = getAdministratorObject(self)
#         return serializer.save(school=school)

# list all courses available in the school  
class CourseListAPIView(ListAPIView):
    serializer_class = CourseSerializer
    queryset = Courses.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    @extend_schema(
        examples=[
            OpenApiExample(
                "Example of courses in the school.",
                value={"title": 'Hydraulics', "credit": 4, 
                       "instructor": "AbdulAfeez", "class":"100level"},
                request_only=False,
                response_only=True,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        school = getAdministratorObject(self)
        courses = self.queryset.filter(school=school)
        result = []
        for course in courses:
            output = {
                'title': course.title,
                'credit': course.credit,
                'instructor': course.instructor.name,
                'class' : course.year.name
            }
            result.append(output)
        return response.Response(result, status=status.HTTP_200_OK)
    
#Get total number of courses in a school
class TotalCoursesInSchoolAPIView(ListAPIView):
    serializer_class = CourseSerializer
    queryset = Courses.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    @extend_schema(
        examples=[
            OpenApiExample(
                "Example of total number of courses in school.",
                value={"Total_Course": 10},
                request_only=False,
                response_only=True,
            ),
        ],
    )
    
    def get(self, request, *args, **kwargs):
        school = getAdministratorObject(self)
        total_courses = self.queryset.filter(school=school).count()
        result = {"Total_Course": total_courses}
        return response.Response(result)
    
# Modify an individual course 
class CourseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    queryset = Courses.objects.all()
    permission_classes = [IsAdministrator,permissions.IsAuthenticated]
    lookup_field = "title"
    
    def perform_create(self, serializer):
        school = getAdministratorObject(self)
        return serializer.save(school=school)
    
    def get(self, request, title):
        course = self.queryset.filter(school=getAdministratorObject(self), title=title)
        result = []
        for info in course:
            output = {}
            output['title'] = info.title
            output['class'] = info.year.name
            output['instructor'] = info.instructor.name
            output['credit'] = info.credit
            result.append(output)
        return response.Response(result)
    
    
            
# List all instructors in the school
class InsructorListAPIView(ListAPIView):
    serializer_class = InstructorSerializer
    queryset = Instructor.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    @extend_schema(
        examples=[
            OpenApiExample(
                "List all instructors in the school.",
                value={'id': 1, 'email': "example@email.com", 'name': "instructor name", 'gender': "MALE"},
                request_only=False,
                response_only=True,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        school = getAdministratorObject(self)
        instructors = self.queryset.filter(school=school)
        result = []
        for instructor in instructors:
            output = {}
            output['id'] = instructor.pk
            output['email'] = instructor.user.email
            output['name'] = instructor.name
            output['gender'] = instructor.gender
            result.append(output)
        return response.Response(result)
    
#Get total number of instructors in a school
class TotalInstructorsInSchoolAPIView(ListAPIView):
    serializer_class = InstructorSerializer
    queryset = Instructor.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    @extend_schema(
        examples=[
            OpenApiExample(
                "Example of total number of instructors in school.",
                value={"Total_Instructors": 30},
                request_only=False,
                response_only=True,
            ),
        ],
    )
    
    def get(self, request, *args, **kwargs):
        school = getAdministratorObject(self)
        total_instructors = self.queryset.filter(school=school).count()
        result = {"Total_Instructors": total_instructors}
        return response.Response(result)

# Modify individual Instructor
class InsructorModifyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = IndividualInstructorSerializer
    queryset = Instructor.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    lookup_field = "name"
    
    def get(self, request, name):
        school = getAdministratorObject(self)
        instructors = self.queryset.filter(school=school, name=name)
        result = []
        for instructor in instructors:
            output = {}
            output['name'] = instructor.name
            output['gender'] = instructor.gender
            result.append(output)
        return response.Response(result)
    
    
    
# Create a new classroom   
class ClassroomCreateAPIView(CreateAPIView):
    serializer_class = CreateClassroomSerializer
    queryset = Year.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        school = getAdministratorObject(self)
        return serializer.save(school=school)
    
# list all classrooms available in the school  
class ClassroomListAPIView(ListAPIView):
    serializer_class = ClassroomSerializer
    queryset = Year.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        school = getAdministratorObject(self)
        classrooms = self.queryset.filter(school=school)
        result = []
        for classroom in classrooms:
            output = {}
            output['id'] = classroom.pk
            output['name'] = classroom.name
            output['year'] = classroom.year
            result.append(output)
        return response.Response(result)

# List all the students in a class    
class StudentListAPIView(GenericAPIView):
    serializer_class = ListAllStudentInClassSerializer
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    @extend_schema(
        parameters = [
          OpenApiParameter(name='year', description='Filter by classroom', required=True, type=str),  
        ],
        examples=[
            OpenApiExample(
                "Example of total number of students in class.",
                value={"name": "student name", 'gender': "MALE", "matric_no": "2016543"},
                request_only=False,
                response_only=True,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        school = getAdministratorObject(self)
        year = self.request.query_params.get('year')
        year_obj = Year.objects.get(school=school, name=year)
        students = Student.objects.filter(school=school.pk, year=year_obj.pk)
        result = []
        for student in students:
            output = {}
            output['name'] = student.name
            output['gender'] = student.gender
            output['matric_no'] = student.matric_no
            result.append(output)
        if len(result) == 0:
            response.Response('no student registered for the course yet')
        else:
            return response.Response(result)
    
#Get total number of students in a school
class TotalStudentInSchoolAPIView(ListAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    @extend_schema(
        examples=[
            OpenApiExample(
                "Example of total number of students in school.",
                value={"Total_Student": 10},
                request_only=False,
                response_only=True,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        school = getAdministratorObject(self)
        total_students = self.queryset.filter(school=school).count()
        result = {"Total_Student": total_students}
        return response.Response(result)
    
# Get total male students in a school
class TotalStudentInfoInSchoolAPIView(GenericAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    @extend_schema(
        examples=[
            OpenApiExample(
                "Example of total number of male students in school.",
                value={"Total_male_student": 10,
                       "Total_female_student": 10},
                request_only=False,
                response_only=True,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        school = Administrator.objects.get(user=self.request.user)
        total_male_students = Student.objects.filter(school=school, gender='MALE').count()
        total_female_students = Student.objects.filter(school=school, gender='FEMALE').count()
        result = {"Total_male_student": total_male_students, 
                  "Total_female_student": total_female_students}
        return response.Response(result)
   
# Modify student information
class StudentAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    lookup_field = "matric_no"
    
    def perform_create(self, serializer):
        school = getAdministratorObject(self)
        return serializer.save(school=school)
    
    def get_queryset(self):
        school = getAdministratorObject(self)
        return list(self.queryset.filter(school=school).values())   
         
# Get the course attendance view
class GetCourseAttendanceView(ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    queryset = Attendance.objects.all()
    lookup_field = "course"
    
    @extend_schema(
        examples=[
            OpenApiExample(
                "Example of attendace",
                value={"date": '22/1/2023', "name": "AbdulAfeez", 
                       "matric_no": "20171469"},
                request_only=False,
                response_only=True,
            ),
        ],
        description= "Gets the list of a course attendance"
    )
    def get(self, request, course):
        course = Courses.objects.filter(title=course) 
        course_attendance = self.queryset.filter(course=course).order_by('-date')
        result = []
        for attendance in course_attendance:
            student_atendance = {}
            student_atendance['date'] = attendance.date
            student_atendance['name'] = attendance.student.name
            student_atendance['matric_no'] = attendance.student.matric_no
            result.append(student_atendance)
        return response.Response(result)
    
# View to get the course attendance using the date     
class GetCourseAttendanceByDateView(RetrieveAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    queryset = Attendance.objects.all()
    filterset_fields = ['course', 'date']
    @extend_schema(
        parameters=[
            OpenApiParameter(name='course', description='Filter by course title', required=True, type=str),
            OpenApiParameter(name='date', description='Filter by date attendance was taken', required=True, type=str)
        ],
        examples=[
            OpenApiExample(
                "Example of attendace",
                value={"date": '22/1/2023', "name": "AbdulAfeez", 
                       "matric_no": "20171469"},
                request_only=False,
                response_only=True,
            ),
        ],
        description="Get the course attendance for a particular day"
    )
    def get(self, request, *args, **kwargs):
        course_title = self.kwargs['course']  # Extract course title from URL
        date = self.kwargs['date']
        course = Courses.objects.filter(title=course_title).first()
        course_attendance = self.queryset.filter(course=course, date=date)
        result = []
        for attendance in course_attendance:
            student_atendance = {}
            student_atendance['date'] = attendance.date
            student_atendance['name'] = attendance.student.name
            student_atendance['matric_no'] = attendance.student.matric_no
            result.append(student_atendance)
        return response.Response(result)
    
#Get total attendance count    
class CountTotalAttendanceView(ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    queryset = Attendance.objects.all()
    @extend_schema(
        examples=[
            OpenApiExample(
                "Example of total attendace",
                value={"total_attendance": 23},
                request_only=False,
                response_only=True,
            ),
        ],
        description="Get the total attendance count"
    )
    def get(self, request):
        total_course_attendance = self.queryset.values('date').distinct().count()
        return response.Response({'total_attendance':total_course_attendance})