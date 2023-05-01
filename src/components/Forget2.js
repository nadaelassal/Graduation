/* eslint-disable jsx-a11y/alt-text */
import React from "react";
import "./forget2.css";
import open from "./open.png";
import ArrowBackOutlinedIcon from "@mui/icons-material/ArrowBackOutlined";
import { Link } from "react-router-dom";
import { useState } from "react";
import Thirdform from "./Thirdform";
import "./Forget";

function Forget2() {
  const [values, setValues] = useState({
    password: "",
  });

  const inputs = [
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
    <>
      <form onSubmit={handleSubmit} className="formforget2">
        <Link to="/Forget" className="backicon2">
          <ArrowBackOutlinedIcon fontSize="large" className="backicon2" />
        </Link>
        <div>
          {" "}
          <img src={open} className="open" />
        </div>
        <br />
        <h1 className="new">New </h1>
        <h2 className="passw"> Password</h2>
        <div className="forget2">
          {inputs.map((input) => (
            <Thirdform
              key={input.id}
              {...input}
              value={values[input.name]}
              onChange={onChange}
            />
          ))}
        </div>

        <li>
          {" "}
          <Link to="/Home" className="loginbutton">
            Log in
          </Link>
        </li>
      </form>
    </>
  );
}

export default Forget2;
