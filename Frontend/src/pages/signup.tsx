import React from "react";
import { Flex, Button, Title, Subtitle } from "@tremor/react";
import SignUpImage from "@/assets/signup.png";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useSignup } from "@/api/hooks";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import ControlledInput from "@/components/base/Input";
const signUpSchema = z.object({
  name: z.string().min(1, "Name is required").max(50),
  email: z.string().min(1, "Email is required").email(),
  password: z
    .string()
    .min(1, "Email is required")
    .min(12, "Password must be more than 11 characters")
    .max(50),
});

type SignUpSchema = z.infer<typeof signUpSchema>;

function SignUp() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignUpSchema>({
    resolver: zodResolver(signUpSchema),
  });
  const { mutateAsync, isLoading } = useSignup();
  const navigate = useNavigate();
  return (
    <div className="grid grid-cols-2 min-h-screen container mx-auto px-6 items-center">
      <div className="grid grid-cols-2 min-h-screen fixed inset-0 -z-10">
        <div className="col-span-1 bg-white" />
        <div className="col-span-1 bg-[#e8f0ff]" />
      </div>
      <div className="max-w-sm justify-self-center">
        <Title>Welcome to RegTraka, Sign Up to Continue</Title>
        <Subtitle className="text-gray-500">kindly enter your details</Subtitle>
        <Flex
          alignItems="start"
          flexDirection="col"
          className="gap-2 mt-4 [&]>*:w-full "
        >
          <ControlledInput
            register={register}
            name="name"
            label="Name"
            placeholder="Enter your Name"
            errors={errors}
          />
          <ControlledInput
            register={register}
            name="email"
            label="Email"
            placeholder="Enter your Email"
            errors={errors}
            type="email"
          />

          <ControlledInput
            register={register}
            name="password"
            label="Password"
            placeholder="Enter your Password"
            errors={errors}
            type="password"
          />

          <Button
            className="mt-3"
            loading={isLoading}
            onClick={handleSubmit((data) => {
              mutateAsync({
                name: data.name,
                email: data.email,
                password: data.password,
              }).then(() => {
                toast.success("Account created successfully");
                navigate("/login");
              });
            })}
          >
            Sign Up
          </Button>
        </Flex>
      </div>
      <div className="justify-self-center">
        <img src={SignUpImage} className="max-w-sm" height="500" width="500" />
      </div>
    </div>
  );
}

export default SignUp;
