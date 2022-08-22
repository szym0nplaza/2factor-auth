import React, { useState } from "react";
import Cookies from "js-cookie";
import { Button, Alert } from "@mui/material";
import { useNavigate } from "react-router-dom";
import "./HomePage.css";

export default function HomePage() {
  const [name, setName] = useState(null);
  const email = Cookies.get("email");
  const navigate = useNavigate();

  const handleLogout = () => {
    Cookies.remove("email");
    return navigate("/");
  };

  return (
    <div className="home-page">
      {email === undefined ? (
        <Alert severity="warning">Please log in to see this page</Alert>
      ) : (
        <div className="success-area">
          <Alert severity="success">
            Welcome user with email <b>{email}</b>! You are logged in.
          </Alert>
          <Button
            style={{ width: "20%" }}
            variant="contained"
            className="home-button"
            onClick={handleLogout}
          >
            Logout
          </Button>
        </div>
      )}
    </div>
  );
}
