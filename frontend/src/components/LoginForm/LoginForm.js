import { React, useState } from "react";
import { TextField, Button } from "@mui/material";
import { postData } from "../../services/client";
import "./LoginForm.css";

export default function LoginForm() {
  const REGEX = /\w@\w.\D{1,}/;
  const [login, setLogin] = useState(null);
  const [isLoginValid, setIsLoginValid] = useState(true);
  const [password, setPassword] = useState(null);
  const validForm = async (e) => {
    if (!REGEX.test(login)) {
      setIsLoginValid(false);
      return;
    }

    const responseData = await postData(
      `http://localhost:8888/api/login/`,
      {
        email: login,
        password: password,
      }
    );
    console.log(responseData)
  };

  return (
    <div className="login-space">
      <label className="login-label">Login Form</label>
      <form className="login-form" onSubmit={validForm}>
        <TextField
          error={!isLoginValid}
          helperText={isLoginValid ? null : "Invalid login format!"}
          onChange={(e) => {
            setLogin(e.target.value);
          }}
          label="Login"
        />
        <TextField
          onChange={(e) => {
            setPassword(e.target.value);
          }}
          type="password"
          label="Password"
        />
        <Button onClick={validForm} variant="contained">
          Login
        </Button>
      </form>
    </div>
  );
}
