/* eslint-disable jsx-a11y/alt-text */
import { useState } from "react";
import FormInput from "./FormInput";
import "./signup.css";
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

export default SignUp;
