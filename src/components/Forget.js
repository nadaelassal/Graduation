/* eslint-disable jsx-a11y/alt-text */
import React from "react";
import "./forget.css";
import lock from "./lock.png";
import ArrowBackOutlinedIcon from "@mui/icons-material/ArrowBackOutlined";
import { Link } from "react-router-dom";
import "./Signin";
import { useState } from "react";
import FormForget from "./FormForget";

const Forget = () => {
  
  const [values, setValues] = useState({
    email: "",
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
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
  };

  const onChange = (e) => {
    setValues({ ...values, [e.target.name]: e.target.value });
  };

  return (
    <>
      <form onSubmit={handleSubmit} className="form">
        <Link to="/Signin" className="backbutton">
          <ArrowBackOutlinedIcon fontSize="large"  className="backbutton"/>
        </Link>
        <div>
          {" "}
          <img src={lock} className="lock" />
        </div>
        <br />
        <h1 className="forgetp">Forget </h1>
        <h2 className="passp">The Password</h2>
        <br />
        <p className="provide">Provide Your Account email </p>
        <h3 className="for">for which you need to reset your password</h3>
        <div className="forgetinput">
          {inputs.map((input) => (
            <FormForget
              key={input.id}
              {...input}
              value={values[input.name]}
              onChange={onChange}
            />
          ))}
        </div>

        <li>
          {" "}
          <Link to="/Forget2" className="next">
            Next
          </Link>
        </li>
      </form>
    </>
    
  ); 
};


export default Forget;
