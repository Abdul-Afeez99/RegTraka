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
  deleteUser: () => void;
}

const createUserSlice: StateCreator<UserSlice> = (set) => ({
  setUser: (user) =>
    set(() => ({
      user: user,
    })),
  deleteUser: () =>
    set({
      user: undefined,
    }),
});
// thanks copilot :)
export default createUserSlice;
