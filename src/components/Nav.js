/* eslint-disable jsx-a11y/alt-text */

import React from "react";
import "./css code/Nav.css";
import logo from "./logo.png";
import { Link , useNavigate} from "react-router-dom";

function Nav() {
  const navigate = useNavigate();
  return (
    <div className="svm">
      <nav className="item">
        <Link to="/">
          <img src={logo} className="logo" />
        </Link>
        <ul className="ul">
          <li>
            <Link to="/Guides">Guides</Link>
          </li>
          <li>
            <Link to="/Help">Help</Link>
          </li>
          <li>
          <button
          onClick={() => navigate("/SignUp")}
          className="signup-button-get"
        >
          Sign up
        </button>
          </li>
        </ul>
      </nav>
    </div>
  );
}
export default Nav;
