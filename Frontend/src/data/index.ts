import {
  HomeIcon,
  PencilSquareIcon,
  AcademicCapIcon,
  BookOpenIcon,
  Cog6ToothIcon,
  DocumentTextIcon,
  ClockIcon,
} from "@heroicons/react/24/solid";

export const instructorSidbarLinks = [
  {
    name: "Dashboard",
    link: "/instructor/dashboard",
    icon: HomeIcon,
  },
  {
    name: "Attendance",
    link: "/instructor/attendance",
    icon: PencilSquareIcon,
  },
  {
    name: "Students",
    link: "/instructor/students",
    icon: AcademicCapIcon,
  },
];
export const adminSidbarLinks = [
  {
    name: "Dashboard",
    link: "/admin/dashboard",
    icon: HomeIcon,
  },
  {
    name: "Instructor",
    link: "/admin/instructor",
    icon: DocumentTextIcon,
  },
  {
    name: "Students",
    link: "/admin/students",
    icon: AcademicCapIcon,
  },
];

export const sampleCourses = [
  {
    name: "MTH 201",
    link: "/instructor/students/MTH201",
  },
  {
    name: "MTH 202",
    link: "/instructor/students/MTH202",
  },
  {
    name: "GNS 201",
    link: "/instructor/students/GNS201",
  },
];
