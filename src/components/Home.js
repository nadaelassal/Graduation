/* eslint-disable react/jsx-no-undef */
/* eslint-disable jsx-a11y/alt-text */
import React from "react";
import "./css code/Home.css";
import model from "./model.png";
import { Link } from "react-router-dom";
import PlayCircleOutlineIcon from "@mui/icons-material/PlayCircleOutline";
import face from "./fb.png";
import insta from "./Insta.png";
import you from "./you.jpg";
import Nav2 from "./Nav2";
import MultiActionAreaCard from "./Card1";
import MultiActionAreaCard2 from "./Card2";
import MultiActionAreaCard3 from "./Card3";

function Home() {
  return (
    <div className="main">
      <Nav2 />
      <div className="main1">
        <h1 className="mov">
          Move
          <br />
          & Lose
          <br />
          Weight
        </h1>
        <p className="cont">
          join our gym website today and discover a world of fitness tips,
          <br />
          workout plans, and community support
          <br />
          to help you achieve your fitness goals.
        </p>

        <li className="li2">
          <Link to="/mypage" className="str-button">
            Get Started
          </Link>
          <Link to="/video" className="str-icon">
            <PlayCircleOutlineIcon fontSize="large" className="str-icon" />
          </Link>
        </li>

        <div>
          <img src={model} className="model2" />
        </div>
        <div className="phrase">
          <h1 className="sweat">Sweat</h1>
          <h2 className="challenge">3 challenges</h2>
        </div>

        <MultiActionAreaCard />
        <MultiActionAreaCard2 />
        <MultiActionAreaCard3 />
      </div>
      
      <div className="icons2">
        <Link to="https://www.Facebook.com">
          <img src={face} className="fb2" />
        </Link>
        <Link to="https://www.Youtube.com">
          <img src={you} className="youtube2" />
        </Link>
        <Link to="https://www.Instagram.com">
          <img src={insta} className="insta2" />
        </Link>
      </div>
    </div>
  );
}
export default Home;
