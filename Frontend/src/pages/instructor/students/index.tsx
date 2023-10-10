import useStore from "@/store";
import React from "react";
import { Navigate, Link } from "react-router-dom";
import { sampleCourses } from "@/data";
import { Button } from "@tremor/react";

function Students() {
	return (
		<section className="px-5 my-8">
			<h1 className="text-xl font-bold">View Students</h1>
			<p>Select course and see students studying course </p>
			<div className="flex flex-col gap-4">
				{sampleCourses.map((course) => (
					<Courses key={course} course={course.name} />
				))}
			</div>
		</section>
	);
}
function Courses({ course }: { course: string }) {
	const [prefix, num] = course.split(" ");
	return (
		<section className="px-4 py-6 rounded-md bg-primary/30 flex justify-between items-center">
			<h2>
				<span className="font-bold text-lg ">{prefix} </span>
				<span className="font-medium text-md">{num}</span>
			</h2>
			<Button>
				<Link to={`/instructor/students/${prefix + num}`}>View Details</Link>
			</Button>
		</section>
	);
}
export default Students;
