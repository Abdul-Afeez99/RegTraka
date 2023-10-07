import { Card, Title, AreaChart } from "@tremor/react";

const chartdata = [
	{
		date: "Jan 22",
		"Present students": 180,
		"Absent students": 20,
	},
	{
		date: "Feb 22",
		"Present students": 150,
		"Absent students": 50,
	},
	{
		date: "Mar 22",
		"Present students": 200,
		"Absent students": 0,
	},
	{
		date: "Apr 22",
		"Present students": 120,
		"Absent students": 80,
	},
	{
		date: "May 22",
		"Present students": 190,
		"Absent students": 10,
	},
	{
		date: "Jun 22",
		"Present students": 180,
		"Absent students": 20,
	},
];


export default function AttendanceChart() {
	return (
		<Card>
			<Title>Total Attendance report</Title>
			<AreaChart
				className="h-72 mt-4"
				data={chartdata}
				index="date"
				categories={["Present students", "Absent students"]}
				colors={["green", "red"]}
			/>
		</Card>
	);
}
