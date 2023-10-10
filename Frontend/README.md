# Regtraka Frontend

a user interface for the regtraka attendance system built by Abdulafeez.[[link to UI](https://www.figma.com/file/3JUSJ5UYTRXOJ0U7aFTS9q/RegTraka?node-id=0%3A1&mode=dev)]

## Running the app

- After cloning the repository, run the following command `pnpm i` to install the dependencies of the project.
- You then run the development server by using this command `pnpm run dev`.

> Note that this project uses `pnpm` instead of regular `npm`. You might need to install it using [scoop](https://scoop.sh/#/apps?q=pnpm&id=bdaceee1580ed1e27099a92e23e499d1f2409d41)

## App routes

```
├── /
├── /login
├── /register-student
├── /signup
├── /instructor
│   ├── dashboard
│   ├── students
│   │   └── :courseId
│   └── attendance
└── /admin
    ├── /dashboard
    ├── /students
    │    └── :courseId
    ├── /instructor
    └── /attendance
```

## Deployment

run `pnpm run build` to build to project are deploy to desired platform
