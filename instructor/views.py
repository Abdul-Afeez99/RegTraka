from administrator.serializers import IndividualInstructorSerializer, CourseSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework import permissions, response, status
from Users.permissions import IsInstructor
from Users.models import Instructor, Courses, Student
from Users.serializers import UserSerializer
from .serializers import AllCourseStudentSerializer, AttendanceSerializer
import os, pickle, cv2, face_recognition, time
import numpy as np
import threading


# Create your views here.
# def getInstructorObject(self,):
#     user_obj = self.request.user
#     instructor = Cus.objects.get(user=user_obj)
#     return instructor

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

class EncodeStudentImageAPIView(RetrieveAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsInstructor&permissions.IsAuthenticated]
    lookup_field = 'title'
    
    def get(self, request, title):
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
        
class ThreadedCamera(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        
        self.FPS = 1/30
        self.FPS_MS = int(self.FPS * 1000)
        
        # Load encoding file only once
        with open('EncodeFile.p', 'rb') as file:
            encodeListKnownWithMatricNo = pickle.load(file)
        self.encodeListKnown, self.matric_no = encodeListKnownWithMatricNo
        
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
    
    def update(self):
        while True:
            if self.capture.isOpened():
                self.success, self.img = self.capture.read()
                if self.success:
                    image = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
                    faceCurFrame = face_recognition.face_locations(image)
                    encodeCurFrame = face_recognition.face_encodings(image, faceCurFrame)
                    
                    for encodeFace in encodeCurFrame:
                        matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace, tolerance=0.4)
                        # Process matches here
                        print('matches', matches)
                        
            # Sleep for a short duration to control frame rate
            time.sleep(self.FPS)
            
    def show_frame(self):
        cv2.imshow('frame', self.img)
        cv2.waitKey(self.FPS_MS)
            
# class StartAttendanceAPIView(GenericAPIView):
#     serializer_class = AttendanceSerializer
#     permission_classes = [IsInstructor&permissions.IsAuthenticated]
    
#     def post(self, request, *args, **kwargs):
        