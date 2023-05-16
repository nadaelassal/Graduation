/* eslint-disable jsx-a11y/alt-text */
import React from "react";
import "./css code/Content.css";
import model from "./model.png";
import { Link, useNavigate } from "react-router-dom";
import PlayCircleOutlineIcon from "@mui/icons-material/PlayCircleOutline";
import face from "./fb.png";
import insta from "./Insta.png";
import you from "./you.jpg";
import Nav from "./Nav";

function Content() {
  const navigate = useNavigate();
  return (
    <div className="main_content">
      <Nav/>
      <h1 className="move">
        Move
        <br />
        & Lose
        <br />
        Weight
      </h1>
      <p className="content">
        join our gym website today and discover a world of fitness tips,
        <br />
        workout plans, and community support
        <br />
        to help you achieve your fitness goals.
      </p>

      <li className="li">
        <button
          onClick={() => navigate("/Signin")}
          className="start-button-get"
        >
          Get Started
        </button>
        <Link to="/video" className="start-icon">
          <PlayCircleOutlineIcon fontSize="large" className="start-icon" />
        </Link>
      </li>

      <div>
        <img src={model} className="model" />
      </div>
      <div className="icons">
        <Link to="https://www.Facebook.com">
          <img src={face} className="fb" />
        </Link>
        <Link to="https://www.Youtube.com">
          <img src={you} className="youtube" />
        </Link>
        <Link to="https://www.Instagram.com">
          <img src={insta} className="insta" />
        </Link>
      </div>
    </div>
  );
}
export default Content;
