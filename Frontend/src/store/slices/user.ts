import type { StateCreator } from "..";

type User = {
  access: string;
  email: string;
  name: string;
  refresh: string;
  role: "administrator" | "teacher" | "student";
};
export interface UserSlice {
  user?: User;
  setUser: (user: User) => void;
}

const createUserSlice: StateCreator<UserSlice> = (set) => ({
  setUser: (user) =>
    set(() => ({
      user: user,
    })),
});
// thanks copilot :)
export default createUserSlice;
