import React from "react";
import { Flex, Text, Button, Title, Subtitle } from "@tremor/react";

import LoginImage from "@/assets/login.png";
import { useLogin } from "@/api/hooks";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import useStore from "@/store";
const loginSchema = z.object({
	email: z.string().min(1, "Email is required").email(),
	password: z
		.string()
		.min(1, "Email is required")
		.min(12, "Password must be more than 11 characters")
		.max(50),
});

type LoginSchema = z.infer<typeof loginSchema>;

function Login() {
	const setUser = useStore((state) => state.setUser);
	const navigate = useNavigate();
	const { mutateAsync, isLoading } = useLogin({
		onSuccess: (data) => {
			setUser(data);
			navigate("/dashboard");
		},
	});
	const { register, handleSubmit } = useForm<LoginSchema>({
		resolver: zodResolver(loginSchema),
	});
	return (
		<div className="grid grid-cols-2 min-h-screen container mx-auto px-6 items-center">
			<div className="grid grid-cols-2 min-h-screen fixed inset-0 -z-10">
				<div className="col-span-1 bg-white" />
				<div className="col-span-1 bg-[#e8f0ff]" />
			</div>
			<div className="max-w-sm justify-self-center">
				<Title>Welcome to RegTraka, Sign In to Continue</Title>
				<Subtitle>Please enter your details</Subtitle>
				<Flex
					alignItems="start"
					flexDirection="col"
					className="gap-2 mt-4 [&]>*:w-full "
				>
					<Flex alignItems="start" flexDirection="col">
						<Text>Email</Text>
						<input
							type="email"
							className="rounded-lg border-gray-200 border py-1 pl-2 w-full"
							{...register("email")}
						/>
					</Flex>
					<Flex alignItems="start" flexDirection={"col"}>
						<Text>Password</Text>
						<input
							type="password"
							className="rounded-lg border-gray-200 border py-1 pl-2 w-full"
							{...register("password")}
						/>
					</Flex>
					<Button
						loading={isLoading}
						className="mt-3"
						onClick={handleSubmit((d) =>
							mutateAsync(d).then((d) => console.log(d))
						)}
					>
						Sign In
					</Button>
				</Flex>
			</div>
			<div className="justify-self-center">
				<img src={LoginImage} className="max-w-sm" height="500" width="500" />
			</div>
		</div>
	);
}

export default Login;
