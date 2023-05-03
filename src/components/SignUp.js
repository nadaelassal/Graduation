/* eslint-disable jsx-a11y/alt-text */
/*import { useState } from "react";
import FormInput from "./FormInput";
import "./css code/signup.css";
import { Link } from "react-router-dom";
import "./Home";
import sign from "./sign.jpg";

const SignUp = () => {
  const [values, setValues] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const inputs = [
    {
      id: 1,
      name: "username",
      type: "text",
      placeholder: "Enter your name",
      errorMessage:
        "Username should be 3-16 characters and shouldn't include any special character!",
      pattern: "^[A-Za-z0-9]{3,16}$",
      required: true,
    },
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
    {
      id: 4,
      name: "confirmPassword",
      type: "password",
      placeholder: "Confirm password",
      errorMessage: "Passwords don't match!",
      pattern: values.password,
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
        <img src={sign} className="image" />
      </div>

      <form onSubmit={handleSubmit} className="signupform">
        <p className="welcome">Welcome champ</p>
        <div className="inputs1">
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
          <Link to="/Signup2" className="button1">
            Sign up
          </Link>
        </li>
        <li>
          {" "}
          <Link to="/Signin" className="button2">
            Log in
          </Link>
        </li>
        <li>
          <Link to="https://www.Google.com" className="button3">
            Sign up with Google
          </Link>
        </li>
        <li>
          <Link to="https://www.Facebook.com" className="button4">
            Sign up with Facebook
          </Link>
        </li>
      </form>
    </div>
  );
};

export default SignUp;*/

import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./css code/signup.css"
import "./Home";
import sign from "./sign.jpg";


function SignUp() {
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
      // signup successful, navigate to home page
      navigate("/home");
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
            <input
              className="input-holder00"
              type="Nmae"
              name="Name"
              placeholder="Enter Your Name"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="input-holder11">
            <input
              className="input-holder11"
              type="email"
              name="email"
              placeholder="Enter Your E-mail"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            {errors.email && <div className="error">{errors.email}</div>}
          </div>
          <div className="input-holder22">
            <input
              className="input-holder22"
              type="password"
              name="password"
              placeholder="Enter Your Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            {errors.password && <div className="error">{errors.password}</div>}
          </div>

          <div>
            <button type="submit" className="signup-button22">
             Sign up
            </button>
          </div>
        </form>
        <div>
          <button onClick={() => navigate("/Signin")} className="signin-button22">
            Login
          </button>
        </div>
        <br/>
        <div>
          <Link to="https://www.google.com" className="google-button22">
            Sign in with Google
          </Link>
        </div>
        <br/>
        <div>
          <Link to="https://www.facebook.com" className="facebook-button22">
          Sign in with Facebook
          </Link>
        </div>
      </div>
    </div>
  );
}

export default SignUp;
