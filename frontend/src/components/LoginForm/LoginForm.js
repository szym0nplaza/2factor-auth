import { React, useState, useEffect } from "react";
import { TextField, Button, Alert, Collapse } from "@mui/material";
import { postData } from "../../services/client";
import { useNavigate } from "react-router-dom";
import "./LoginForm.css";

export default function LoginForm() {
  const REGEX = /\w@\w.\D{1,}/;
  const navigate = useNavigate();
  const [login, setLogin] = useState(null);
  const [isLoginValid, setIsLoginValid] = useState(true);
  const [isPasswordValid, setIsPasswordValid] = useState(true);
  const [password, setPassword] = useState(null);
  const [status, setStatus] = useState(null);
  const [response, setResponse] = useState(null);
  const [alert, setAlert] = useState(false);
  const validForm = async (e) => {
    e.preventDefault();
    if (!REGEX.test(login)) {
      setIsLoginValid(false);
      return;
    }else{
      setIsLoginValid(true);
    }

    if (!password){
      setIsPasswordValid(false);
      return;
    }else{
      setIsPasswordValid(true);
    }

    const [responseData, status] = await postData(
      `http://0.0.0.0:8888/api/login/`,
      {
        email: login,
        password: password,
      }
    );
    setStatus(status);
    setResponse(responseData);
  };

  useEffect(() => {
    setAlert(false);
    if (status === 400) setAlert(true);
    if (status === 200 && response.otp) {
      return navigate("/verification");
    } else if (status === 200 && !response.otp) {
      return navigate("/home");
    }
  }, [status]);

  return (
    <div className="login-space">
      <label className="login-label">Login Form</label>
      <form className="login-form" onSubmit={validForm}>
        <Collapse in={alert}>
          <Alert severity="error">You provided incorrect data!</Alert>
        </Collapse>
        <TextField
          error={!isLoginValid}
          helperText={isLoginValid ? null : "Invalid login format!"}
          onChange={(e) => {
            setLogin(e.target.value);
          }}
          label="Login"
        />
        <TextField
        error={!isPasswordValid}
        helperText={isPasswordValid ? null : "Fill in password field!"}
          onChange={(e) => {
            setPassword(e.target.value);
          }}
          type="password"
          label="Password"
        />
        <Button type="submit" variant="contained">
          Login
        </Button>
      </form>
    </div>
  );
}
