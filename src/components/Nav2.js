/* eslint-disable jsx-a11y/alt-text */

import React from "react";
import "./css code/Nav.css";
import logo from "./logo.png";
import { Link } from "react-router-dom";
import pro from './pro.png';

function Nav() {
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
            <img src={pro} className="pro"></img>
          </li>
        </ul>
      </nav>
    </div>
  );
}
export default Nav;
