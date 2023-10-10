import React from "react";
import { Card, Col, Grid, Icon, Metric, Text, Title } from "@tremor/react";
import {
  AcademicCapIcon,
  ArrowLeftOnRectangleIcon,
  ArrowRightOnRectangleIcon,
  BookOpenIcon,
  DocumentTextIcon,
} from "@heroicons/react/24/solid";
import AttendanceChart from "@/components/inc/AttendanceChart";
import useStore from "@/store";
import {
  useAdminCourses,
  useAdminInstructors,
  useAdminTotalStudents,
} from "@/api/hooks";

function Dashboard() {
  const { name } = useStore((s) => s.user!);
  const { data: totalStudents } = useAdminTotalStudents({
    select(data) {
      return data.Total_Student;
    },
  });
  const { data: adminCourses } = useAdminCourses();
  const { data: adminInstructors } = useAdminInstructors();

  return (
    <section className="px-5 my-8">
      <div className="flex flex-col gap">
        <h1 className="text-xl font-bold">Hello, {name}!👋</h1>
        <p>We hope you're having a great day</p>
      </div>
      <Grid numItems={1} numItemsMd={2} numItemsLg={6} className="gap-4 mt-4">
        <Col numColSpan={1} numColSpanLg={2}>
          <Card className="flex">
            <Icon size="xl" icon={AcademicCapIcon} />
            <div className="flex flex-col gap-2">
              <Metric>{totalStudents ?? 0}</Metric>
              <Text>TOTAL STUDENTS</Text>
            </div>
          </Card>
        </Col>
        <Col numColSpan={1} numColSpanLg={2}>
          <Card className="flex" decoration="top" decorationColor="orange">
            <Icon size="xl" icon={DocumentTextIcon} />
            <div className="flex flex-col gap-2">
              <Metric>{adminInstructors?.length ?? 0}</Metric>
              <Text>Total Instructor</Text>
            </div>
          </Card>
        </Col>
        <Col numColSpan={1} numColSpanLg={2}>
          <Card className="flex">
            <Icon size="xl" icon={BookOpenIcon} />
            <div className="flex flex-col gap-2">
              <Metric>{adminCourses?.length ?? 0}</Metric>
              <Text>Total Courses</Text>
            </div>
          </Card>
        </Col>
        <Col numColSpan={1} numColSpanMd={2} numColSpanLg={6}>
          <AttendanceChart />
        </Col>

        <Col numColSpan={1} numColSpanMd={2} numColSpanLg={3}>
          <Card decoration="top" decorationColor="blue">
            <Title>MALE</Title>
            <span>
              <Metric>50</Metric>
              <Text>PRESENT TODAY</Text>
            </span>
          </Card>
        </Col>
        <Col numColSpan={1} numColSpanMd={2} numColSpanLg={3}>
          <Card decoration="top" decorationColor="pink">
            <Title>FEMALE</Title>
            <span>
              <Metric>50</Metric>
              <Text>PRESENT TODAY</Text>
            </span>
          </Card>
        </Col>
      </Grid>
    </section>
  );
}

export default Dashboard;
