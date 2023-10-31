from administrator.serializers import IndividualInstructorSerializer, CourseSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework import permissions, response, status
from rest_framework.views import APIView
from Users.permissions import IsInstructor
from Users.models import Instructor, Courses, Student, Attendance, Year
from Users.serializers import UserSerializer
from .serializers import AllCourseStudentSerializer, AttendanceSerializer, CreateCourseSerializer, ClassSerializer
import os, pickle, cv2, face_recognition, time
import numpy as np
import threading
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter


list_of_student = []
# Global variable to control attendance taking process
attendance_process_active = False

# function to encode student image    
def encodeStudentImage(title):
    course = Courses.objects.get(title=title)
    students = Student.objects.filter(courses=course)
    file_path = os.getcwd()
    file_name = 'media/images'
    file_path = os.path.join(file_path, file_name)
    student_images_list = []
    student_matric_no = []
    for student in students:
        student_images_list.append(os.path.join(file_path, student.image))
        student_matric_no.append(os.path.splitext(student.image)[0])    
    encodings = []
    for img in student_images_list:
        img = cv2.imread(img)
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoder = face_recognition.face_encodings(image)[0]
        encodings.append(encoder)
    encodeListKnownWithMatricNo = [encodings, student_matric_no]
    file = open("EncodeFile.p", "wb")
    pickle.dump(encodeListKnownWithMatricNo, file)
    file.close()
        
        
# Function to start attendance process   
def start_attendance_process(self):
    global attendance_process_active
    global list_of_student
    src = 0 #add the camera src
    capture = cv2.VideoCapture(src, cv2.CAP_DSHOW)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    
    FPS = 1/30
    FPS_MS = int(FPS * 1000)
    # Load encoding file only once
    with open('EncodeFile.p', 'rb') as file:
        encodeListKnownWithIDs = pickle.load(file)
    file.close()    
    encodeListKnown, matric_no = encodeListKnownWithIDs
    while attendance_process_active:
        if capture.isOpened():
            success, img = capture.read()
            if success:
                image = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
                faceCurFrame = face_recognition.face_locations(image)
                encodeCurFrame = face_recognition.face_encodings(image, faceCurFrame)
                # Process matches here
                for encodeFace in encodeCurFrame:
                    matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance=0.4)
                    matches_array = np.array(matches)
                    indices = np.where(matches_array==True)[0]
                    for index in indices:
                        if matric_no[index] not in list_of_student:
                            list_of_student.append(matric_no[index])
                        else:
                            continue
                    
        # Sleep for a short duration to control frame rate
        time.sleep(self.FPS)
    # Release the video capture object when attendance process is stopped
    capture.release()
    cv2.destroyAllWindows()

# Function to mark the attendance
def markStudent(serializer, course_title, student_list):
    for student_no in student_list:
        student_obj = Student.objects.filter(matric_no=student_no)
        course_obj = Courses.objects.filter(title = course_title)
        is_present = True
        serializer.save(student=student_obj, course=course_obj, is_present=is_present)


# Get the current instructor information
class InstructorInfoView(RetrieveAPIView):
    permission_classes = [IsInstructor&permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        instructor = Instructor.objects.filter(user=user)
        result = {}
        for info in instructor:
            result['name'] = info.name
            result['email'] = info.user.email
            result['school'] = info.school.name
            result['gender'] = info.gender
        return response.Response(result, status=status.HTTP_200_OK)

# Get all classes in the instructor school
class ClassroomListAPIView(ListAPIView):
    serializer_class = ClassSerializer
    permission_classes = [IsInstructor&permissions.IsAuthenticated]
    queryset = Year.objects.all()
    
    def get(self, request, *args, **kwargs):
        instructor = Instructor.objects.get(user=self.request.user)
        school = instructor.school
        classrooms = self.queryset.filter(school=school)
        result = []
        for classroom in classrooms:
            output = {}
            output['id'] = classroom.pk
            output['name'] = classroom.name
            output['year'] = classroom.year
            result.append(output)
        return response.Response(result)
     
           
# Create a new course   
class CourseCreateAPIView(CreateAPIView):
    serializer_class = CreateCourseSerializer
    queryset = Courses.objects.all()
    permission_classes = [IsInstructor&permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        instructor = Instructor.objects.get(user=self.request.user)
        school = instructor.school
        return serializer.save(instructor=instructor, school=school)

# Get the instructor courses
class GetInstructorCoursesAPIView(ListAPIView):
    serializer_class = IndividualInstructorSerializer
    queryset = Instructor.objects.all()
    permission_classes = [IsInstructor&permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        instructor = self.queryset.filter(user=user)
        serializer = self.serializer_class(instructor, many=True).data
        result = {}
        result['name'] = serializer[0]['name']
        result['courses'] = serializer[0]['instructor_courses']
        return response.Response(result, status=status.HTTP_200_OK)


# Get the student offering the course        
class ViewCourseStudentsAPIView(RetrieveAPIView):
    serializer_class = AllCourseStudentSerializer
    queryset = Courses.objects.all()
    permission_classes = [IsInstructor&permissions.IsAuthenticated]
    lookup_field = "title"
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        instructor = Instructor.objects.get(user=user)
        course = self.queryset.filter(instructor=instructor)
        serializer = self.serializer_class(course, many=True).data
        result = {}
        result['title'] = serializer[0]['title']
        result['students'] = serializer[0]['student_courses']
        return response.Response(result, status=status.HTTP_200_OK)


# Start attendance API View
class StartAttendanceView(APIView):
    permission_classes = [IsInstructor&permissions.IsAuthenticated]
    serializer_class = None
    @extend_schema(
        parameters=[
            OpenApiParameter(name='title', description='Filter by course title', required=True, type=str)
        ],
    )
    def post(self, request):
        global attendance_process_active
        course_title = self.request.query_params.get('title')
        encodeStudentImage(course_title)
        if not attendance_process_active:
            # Start a new thread for the attendance process
            attendance_process_active = True
            attendance_thread = threading.Thread(target=start_attendance_process)
            attendance_thread.start()

            return response.Response({"message": "Attendance process started."}, status=status.HTTP_200_OK)
        else:
            return response.Response({"message": "Attendance process is already active."}, status=status.HTTP_400_BAD_REQUEST)

# Stop and save attendance API View
class StopAttendanceView(APIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsInstructor&permissions.IsAuthenticated]
    @extend_schema(
        parameters=[
            OpenApiParameter(name='title', description='Filter by course title', required=True, type=str)
        ],
    )
    def post(self, request):
        global attendance_process_active
        course_title = self.request.query_params.get('title')
        if attendance_process_active:
            # Stop the attendance process
            attendance_process_active = False
            markStudent(serializer=self.serializer_class, course_title=course_title, student_list=list_of_student)
            return response.Response({"message": "Attendance process stopped."}, status=status.HTTP_200_OK)
        else:
            return response.Response({"message": "No active attendance process to stop."}, status=status.HTTP_400_BAD_REQUEST)
          
# Get the course attendance view
class GetCourseAttendanceView(ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsInstructor&permissions.IsAuthenticated]
    queryset = Attendance.objects.all()
    
    @extend_schema(
        parameters = [
          OpenApiParameter(name='course', description='course', required=True, type=str),  
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
        description="Get a particular course atttendance"
    )
    def get(self, request, *args, **kwargs):
        course = self.request.query_params.get('course')
        course_obj = Courses.objects.filter(title=course) 
        course_attendance = self.queryset.filter(course=course_obj)
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
    permission_classes = [IsInstructor&permissions.IsAuthenticated]
    queryset = Attendance.objects.all()
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
        description= "Get the list of course attendance for a particular day"
    )
    def get(self, request, *args, **kwargs):
        course_title = self.request.query_params.get('course')  # Extract course title from URL
        date = self.request.query_params.get('date')
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
    permission_classes = [IsInstructor&permissions.IsAuthenticated]
    queryset = Attendance.objects.all()
    lookup_field = 'course'
    
    def get(self, request, course):
        course_obj = Courses.objects.filter(title=course)
        total_course_attendance = self.queryset.filter(course=course_obj).values('date').distinct().count()
        return response.Response({'total_attendance':total_course_attendance})
        