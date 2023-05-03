/* eslint-disable jsx-a11y/alt-text */
/*import { useState } from "react";
import FormInput from "./FormInput";
import { Link } from "react-router-dom";
import "./Home";
import log from "./log.jpg";
import "./signin.css";

const SignUp = () => {
  const [values, setValues] = useState({
    email: "",
    password: "",
  });

  const inputs = [
    {
      id: 2,
      name: "email",
      type: "email",
      placeholder: "Enter your e-mail",
      errorMessage: "It should be a valid email address!",
      required: true,
    },
    {
      id: 3,
      name: "password",
      type: "password",
      placeholder: "Enter Password",
      errorMessage:
        "Password should be 8-20 characters and include at least 1 letter, 1 number and 1 special character!",
      pattern: `^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,20}$`,
      required: true,
    },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
  };

  const onChange = (e) => {
    setValues({ ...values, [e.target.name]: e.target.value });
  };

  return (
    <div className="app">
      <div>
        <img src={log} className="img" />
      </div>

      <form onSubmit={handleSubmit} className="signform">
        <p className="welcomeb">Welcome Back !</p>
        <div className="inputs222">
          {inputs.map((input) => (
            <FormInput
              key={input.id}
              {...input}
              value={values[input.name]}
              onChange={onChange}
            />
          ))}
        </div>

        <li>
          <Link to="/Forget">
            <p className="forgettt"> Forget password</p>
          </Link>
        </li>
        <br />
        <li>
          <Link to="/Home" className="buttonn">
            Log in
          </Link>
        </li>
        <li>
          {" "}
          <Link to="/Signup" className="buttonnn">
            Sign up
          </Link>
        </li>
      </form>
    </div>
  );
};

export default SignUp;*/

import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Home";
import "./css code/signin.css";
import { Pattern } from "@mui/icons-material";
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

  const handleSubmit = (event) => {
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
      // Login successful, navigate to home page
      navigate("/home");
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
            <input
              className="input-holder1"
              type="email"
              name="email"
              placeholder="Enter Your E-mail"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            {errors.email && <div className="error">{errors.email}</div>}
          </div>
          <div className="input-holder2">
            <input
              className="input-holder2"
              type="password"
              name="password"
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
        <div>
          <button onClick={() => navigate("/SignUp")} className="signup-button">
            Sign up
          </button>
        </div>
      </div>
    </div>
  );
}

export default Signin;
