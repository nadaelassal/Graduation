/* eslint-disable jsx-a11y/alt-text */
import React from "react";
import signup2 from "./signup2.jpg";
import "./css code/signup2.css";
import men from "./men.jpg";
import { Link } from "react-router-dom";

function SignUp2() {
  return (
    <>
      <div>
        <img src={signup2} className="image8" />
      </div>
      <h1 className="wel">Welcome MR Ali</h1>
      <br />
      <p className="plz">Please put picture of you</p>
      <img src={men} className="men" />
      <li>
        <Link to="/" className="b1">
          Upload picture
        </Link>
      </li>
      <li>
      <Link to="/Home" className="b2">
          Next
        </Link>
      </li>
    </>
  );
}
export default SignUp2;
