/* eslint-disable jsx-a11y/alt-text */

import React from "react";
import "./css code/nav2.css";
import logo from "./logo.png";
import { Link } from "react-router-dom";
import pro from './pro.png';

function Nav2() {
  return (
    <div className="svm2">
      <nav className="item2">
        <Link to="/">
          <img src={logo} className="logo2" />
        </Link>
        <ul className="ul2">
          <li className="li2">
            <Link to="/Guides">Guides</Link>
          </li>
          <li className="li2">
            <Link to="/Help">Help</Link>
          </li>
          <li className="li2">
            <img src={pro} className="pro"></img>
          </li>
        </ul>
      </nav>
    </div>
  );
}
export default Nav2;
