import { instructorSidbarLinks } from "@/data";
import { ChevronLeftIcon } from "@heroicons/react/24/solid";
import { Icon } from "@tremor/react";
import React from "react";
import { Outlet, Link, useLocation } from "react-router-dom";
import clsx from "clsx";
import Avatar from "@/assets/avatar.png";

function Root() {
	return (
		<div className="grid grid-cols-[auto_1fr] h-screen ">
			<Sidebar />
			<main className="overflow-y-scroll">
				<section className="bg-primary px-5 py-4 flex justify-between items-center">
					<h1 className="text-xl font-bold text-white">Dashboard</h1>
					<img
						src={Avatar}
						alt="avatar of user"
						className="w-8 h-8 rounded-full"
					/>
				</section>
				<Outlet />
			</main>
		</div>
	);
}

function Sidebar() {
	const [expanded, setExpanded] = React.useState(false);

	function toggleSidebar() {
		setExpanded((prev) => !prev);
	}
	return (
		<div
			className={clsx(
				"bg-primary px-4 relative transition-all ease-in-out duration-300 flex-col shadom-lg border-r-2 border-gray-700",
				expanded ? "w-48" : "w-20"
			)}
		>
			<Icon
				size="sm"
				icon={ChevronLeftIcon}
				variant="solid"
				color="sky"
				className="absolute top-4 -right-4 cursor-pointer"
				tooltip={expanded ? "Collapse" : "Expand"}
				onClick={toggleSidebar}
			/>
			<h1
				className={clsx(
					"font-bold text-3xl text-white mb-12 mt-4",
					!expanded && "text-center rounded-md bg-white/20 w-12 h-12 p-0 flex justify-center items-center"
				)}
			>
				{expanded ? "Regtraka" : "R"}
			</h1>
			<div className="flex flex-col gap-4 flex-1">
				{instructorSidbarLinks.map((link) => {
					return <NavLink key={link.name} {...{ ...link, expanded }} />;
				})}
			</div>
			<div className="mb-8"></div>
		</div>
	);
}

function NavLink({
	link,
	name,
	expanded,
	icon,
}: {
	link: string;
	name: string;
	expanded: boolean;
	icon: typeof ChevronLeftIcon;
}) {
	const location = useLocation();
	const active =
		location.pathname === link || location.pathname.startsWith(link);

	const Icon = icon;
	return (
		<Link
			to={link}
			className={clsx(
				"flex items-center gap-2 p-2  rounded-lg hover:bg-[#0A2A6C] ",
				active && "bg-[#0A2A6C]",
				!expanded && "justify-center"
			)}
			key={name}
		>
			<span className={clsx("text-white")}>
				{
					<Icon
						className={clsx(
							"w-6 h-6",
							"trasition-all ease-in-out duration-300 [& svg]:",
							active ? "text-[#FB843A]" : "text-gray-300"
						)}
					/>
				}
			</span>
			{expanded && (
				<span className={clsx(active ? "text-white" : "text-gray-300")}>
					{name}
				</span>
			)}
		</Link>
	);
}
export default Root;
