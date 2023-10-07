import React from "react";
import { Card, Col, Grid, Icon, Metric, Text, Title } from "@tremor/react";
import {
	AcademicCapIcon,
	ArrowLeftOnRectangleIcon,
	ArrowRightOnRectangleIcon,
} from "@heroicons/react/24/solid";
import AttendanceChart from "@/components/inc/AttendanceChart";

function Dashboard() {
	return (
		<section className="px-5 my-8">
			<div className="flex flex-col gap">
				<h1 className="text-xl font-bold">Hello Babatunde!👋</h1>
				<p>We hope you're having a great day</p>
			</div>
			<Grid numItems={1} numItemsMd={2} numItemsLg={6} className="gap-4 mt-4">
				<Col numColSpan={1} numColSpanLg={2}>
					<Card className="flex">
						<Icon size="xl" icon={AcademicCapIcon} />
						<div className="flex flex-col gap-2">
							<Metric>200</Metric>
							<Text>TOTAL STUDENTS</Text>
						</div>
					</Card>
				</Col>
				<Col numColSpan={1} numColSpanLg={2}>
					<Card className="flex" decoration="top" decorationColor="orange">
						<Icon size="xl" icon={ArrowRightOnRectangleIcon} />
						<div className="flex flex-col gap-2">
							<Metric>50</Metric>
							<Text>PRESENT TODAY</Text>
						</div>
					</Card>
				</Col>
				<Col numColSpan={1} numColSpanLg={2}>
					<Card className="flex">
						<Icon size="xl" icon={ArrowLeftOnRectangleIcon} />
						<div className="flex flex-col gap-2">
							<Metric>10</Metric>
							<Text>ABSENT TODAY</Text>
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
