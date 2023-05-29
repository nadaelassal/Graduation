/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable jsx-a11y/alt-text */
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./css code/signup.css";
import "./Home";
import sign from "./sign.jpg";
import { TextField } from "@mui/material";



function SignUp() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState();
  const [cpassword, setcPassword] = useState();
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
  

  const handleSubmit = (event) => {
    event.preventDefault();
    const newErrors = {};
     
    if (cpassword !== password ) {
      newErrors.cpassword="password doesn't match"
    }
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
      navigate("/Signiformation");
    }
  };

  return (
    <div>
      <div className="login-form2">
        <div>
          <img src={sign} className="sign-image" />
        </div>

        <form onSubmit={handleSubmit}>
          <div className="welcome-p2">Welcome champ</div>
          <div className="input-holder00">
            <TextField
              className="input-holder00"
              label="Name"
              placeholder="Enter Your Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="input-holder11">
            <TextField
              className="input-holder11"
              label="Email"
              placeholder="Enter Your E-mail"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            {errors.email && <div className="error">{errors.email}</div>}
          </div>
          <div className="input-holder22">
            <TextField
              className="input-holder22"
              label="Password"
              placeholder="Enter Your Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            {errors.password && (
              <div className="error-pass">{errors.password}</div>
            )}
          </div>
          <div className="input-holder33">
            <TextField
              className="input-holder33"
              label="Confirm Password"
              placeholder="Confirm Password"
              value={cpassword}
              onChange={(e) => setcPassword(e.target.value)}
              required
            />
            {errors.cpassword && (
              <div className="error-conf">{errors.cpassword}</div>
            )}
          </div>
          <div>
            <button type="submit" className="signup-button22">
              Sign up
            </button>
          </div>
        </form>

        <br />

        <button
          onClick={() => window.open("https://www.google.com")}
          className="google-button22"
        >
          Sign up with google
        </button>

        <button
          onClick={() => window.open("https://www.facebook.com")}
          className="facebook-button22"
        >
          Sign up with facebook
        </button>
      </div>
    </div>
  );
}

export default SignUp;
