/* eslint-disable jsx-a11y/alt-text */
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Pattern } from "@mui/icons-material";
import lock from "./lock.png";
import "./forget.css";
import ArrowBackOutlinedIcon from "@mui/icons-material/ArrowBackOutlined";
import { Link } from "react-router-dom";
import "./Signin";

function Forget() {
  const [email, setEmail] = useState("");
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const validateEmail = (value) => {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const newErrors = {};

    if (!validateEmail(email)) {
      newErrors.email = "Invalid email format";
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
    } else {
      // signup successful, navigate to home page
      navigate("/Forgetcode");
    }
  };

  return (
    <div>
      <div className="login-form3">
        <Link to="/Signin" className="backbutton">
          <ArrowBackOutlinedIcon fontSize="large" className="backbutton" />
        </Link>
        <div>
          <img src={lock} className="lock-image" />
        </div>
        <br />
        <h1 className="forgetp">Forget </h1>
        <h2 className="passp">The Password</h2>
        <br />
        <p className="provide">Provide Your Account email </p>
        <h3 className="for">for which you need to reset your password</h3>
        <form onSubmit={handleSubmit}>
          <div className="input-holder-f">
            <input
              className="input-holder-f"
              type="email"
              name="email"
              placeholder="Enter Your E-mail"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            {errors.email && <div className="error">{errors.email}</div>}
          </div>

          <div>
            <button type="submit" className="forget2-button">
              Next
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Forget;
