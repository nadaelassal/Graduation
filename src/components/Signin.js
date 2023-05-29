/* eslint-disable jsx-a11y/alt-text */
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Home";
import "./css code/signin.css";
import { Pattern } from "@mui/icons-material";
import TextField from "@mui/material/TextField";
import log from "./log.jpg";
import "./SignUp";

function Signin() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const validateEmail = (value) => {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(value);
  };

  const validatePassword = (value) => {
    const passwordPattern =
      /^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,20}$/;
    return passwordPattern.test(value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const newErrors = {};

    if (!validateEmail(email)) {
      newErrors.email = "Invalid email format";
    }

    if (!validatePassword(password)) {
      newErrors.password =
        "Password should be 8-20 characters and include at least 1 letter, 1 number and 1 special character";
    }
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
    } else {
      // signup successful, navigate to home page
      navigate("/Home");
    }
  };

  return (
    <div>
      <div className="login-form">
        <div>
          <img src={log} className="img-signin" />
        </div>

        <form onSubmit={handleSubmit}>
          <div className="welcome-p">Welcome Back !</div>
          <div className="input-holder1">
            <TextField
              className="input-holder1"
              id="outlined-basic"
              label=" E-mail"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            ></TextField>
            {errors.email && <div className="error">{errors.email}</div>}
          </div>
          <div className="input-holder2">
            <TextField
              id="outlined-basic"
              className="input-holder2"
              label="Password"
              placeholder="Enter Your Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            {errors.password && <div className="error">{errors.password}</div>}
          </div>

          <li>
            <Link to="/Forget">
              <p className="forget-button"> Forget password</p>
            </Link>
          </li>
          <div>
            <button type="submit" className="button-container-login">
              Login
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Signin;
