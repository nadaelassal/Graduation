import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./css code/signup.css"
import "./Home";
import sign from "./sign.jpg";
import axios from 'axios';

function SignUp() {
  const [username, setUsername] = useState("");
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
      // signup successful, register user
      axios.post('/register', {
        username: username,
        email: email,
        password: password
      }).then((response) => {
   
        if (response.data['status']==true){
         
          navigate("/home");
        }
        else {

          setErrors({ password: response.data['message'] });
        }
      }).catch((error) => {
        console.log(error);
      });
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
              type="text"
              name="username"
              placeholder="Enter Your Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
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
