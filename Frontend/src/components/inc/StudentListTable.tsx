import {
	CheckBadgeIcon,
	CheckCircleIcon,
	XCircleIcon,
} from "@heroicons/react/24/solid";
import {
	Card,
	Table,
	TableHead,
	TableRow,
	TableHeaderCell,
	TableBody,
	TableCell,
	Text,
	Title,
	Badge,
} from "@tremor/react";

const data = [
	{
		name: "Viola Amherd",
		matricNo: "CCG/2022/001",
		sex: "Male",
		status: "present",
	},
	{
		name: "Simonetta Sommaruga",
		matricNo: "CCG/2022/005",
		sex: "Female",
		status: "present",
	},
	{
		name: "Alain Berset",
		matricNo: "CCG/2022/001",
		sex: "Male",
		status: "absent",
	},
	{
		name: "Ignazio Cassis",
		matricNo: "CCG/2022/201",
		sex: "Male",
		status: "present",
	},
	{
		name: "Ueli Maurer",
		matricNo: "CCG/2022/041",
		sex: "Male",
		status: "absent",
	},
	{
		name: "Guy Parmelin",
		matricNo: "CCG/2022/039",
		sex: "Female",
		status: "present",
	},
	{
		name: "Karin Keller-Sutter",
		matricNo: "CCG/2022/060",
		sex: "Female",
		status: "present",
	},
];

export default function StudentListTable({ course }: { course: string }) {
	return (
		<Card>
			<Title>List of {course} students</Title>
			<Table className="mt-5">
				<TableHead>
					<TableRow>
						<TableHeaderCell>S/N</TableHeaderCell>
						<TableHeaderCell>Name</TableHeaderCell>
						<TableHeaderCell>Matric No</TableHeaderCell>
						<TableHeaderCell>Sex</TableHeaderCell>
						<TableHeaderCell>Attendance</TableHeaderCell>
					</TableRow>
				</TableHead>
				<TableBody>
					{data.map((item, i) => {
						const present = item.status === "present";
						return (
							<TableRow key={item.name}>
								<TableCell>{i + 1}</TableCell>
								<TableCell>{item.name}</TableCell>
								<TableCell>
									<Text>{item.matricNo}</Text>
								</TableCell>
								<TableCell>
									<Text>{item.sex}</Text>
								</TableCell>
								<TableCell>
									<Badge
										color={present ? "emerald" : "red"}
										icon={present ? CheckCircleIcon : XCircleIcon}
									>
										{item.status}
									</Badge>
								</TableCell>
							</TableRow>
						);
					})}
				</TableBody>
			</Table>
		</Card>
	);
}
