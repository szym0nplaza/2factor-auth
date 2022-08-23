import { React, useState, useEffect } from "react";
import { TextField, Button, Alert, Collapse } from "@mui/material";
import { postData } from "../../services/client";
import { useNavigate } from "react-router-dom";

export default function AuthForm() {
  const [code, setCode] = useState(null);
  const [response, setResponse] = useState(null);
  const [alert, setAlert] = useState(false);
  const navigate = useNavigate();

  const verifyCode = async (e) => {
    e.preventDefault();
    const [responseData, status] = await postData(
      "http://0.0.0.0:8888/api/validate-otp/",
      { code: code }
    );
    setResponse(status);
  };

  useEffect(() => {
    setAlert(false);
    if (response === 400) setAlert(true);
    if (response === 200) {
      return navigate("/home");
    }
  }, [response]);

  return (
    <div className="login-space">
      <label className="login-label">Verification page</label>
      <form className="login-form" onSubmit={verifyCode}>
        <Collapse in={!alert}>
          <Alert severity="info">
            Please check your mailbox and provide given 5-digit verification
            code.
          </Alert>
        </Collapse>
        <Collapse in={alert}>
          <Alert severity="error">You provided incorrect code!</Alert>
        </Collapse>
        <TextField
          error={response === 400}
          onChange={(e) => {
            setCode(e.target.value);
          }}
          label="Verification Code"
          type="number"
          placeholder="XXXXX"
          onInput={(e) => {
            e.target.value = Math.max(0, parseInt(e.target.value))
              .toString()
              .slice(0, 5);
          }}
        />
        <Button type="submit" variant="contained">
          Confirm
        </Button>
      </form>
    </div>
  );
}
