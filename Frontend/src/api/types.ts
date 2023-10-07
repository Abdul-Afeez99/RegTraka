export type SignupResponse = {
  name: string;
  email: string;
};

export type LoginResponse = {
  access: string;
  email: string;
  message: string;
  name: string;
  refresh: string;
  role: "administrator" | "teacher" | "student";
  statusCode: string;
  success: string;
};
