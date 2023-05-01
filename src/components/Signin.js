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
import { Link, Route, Routes } from "react-router-dom";
import Home from "./Home";

function Signin() {
  // React States
  const [errorMessages, setErrorMessages] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);

  // User Login info
  const database = [
    {
      username: "user1",
      password: "pass1",
    },
    {
      username: "user2",
      password: "pass2",
    },
  ];

  const errors = {
    uname: "invalid username",
    pass: "invalid password",
  };

  const handleSubmit = (event) => {
    //Prevent page reload
    event.preventDefault();

    var { uname, pass } = document.forms[0];

    // Find user login info
    const userData = database.find((user) => user.username === uname.value);

    // Compare user info
    if (userData) {
      if (userData.password !== pass.value) {
        // Invalid password
        setErrorMessages({ name: "pass", message: errors.pass });
      } else {
        setIsSubmitted(true);
      }
    } else {
      // Username not found
      setErrorMessages({ name: "uname", message: errors.uname });
    }
  };

  // Generate JSX code for error message
  const renderErrorMessage = (name) =>
    name === errorMessages.name && (
      <div className="error">{errorMessages.message}</div>
    );

  // JSX code for login form
  const renderForm = (
    <div>
      <form onSubmit={handleSubmit}>
        <div className="input-container-u">
          <label>Username </label>
          <input type="text" name="uname" required />
          {renderErrorMessage("uname")}
        </div>
        <div className="input-container-p">
          <label>Password </label>
          <input type="password" name="pass" required />
          {renderErrorMessage("pass")}
        </div>

        <div className="button-container">
          <input type="submit"  to="/Home"/>
        </div>
      </form>
    </div>
  );

  return (
    <div>
      <div className="login-form">
        {isSubmitted ? (
         <div>
         <Link to="/Home">
           
         </Link>{" "}
         </div>
        ) : (
          renderForm
        )}
      </div>
    </div>
  );
}

export default Signin;
