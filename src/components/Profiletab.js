/* eslint-disable jsx-a11y/alt-text */
import pro from "./pro.png";
import "./css code/profiletab.css";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";

function ProfileTab() {
  return (
    <div>
      <img src={pro} className="protab" />
      <h2 className="nameinput">Aliaa Mohammed</h2>
      <h1 className="update-p">Update Your Details</h1>
      <div className="input-holder100">
        <input
          className="input-holder100"
          type="hight"
          name="hight"
          placeholder="Enter Your Hight"
          value={Number}
          required
        />
      </div>

      <div className="input-holder200">
        <input
          className="input-holder200"
          type="Weight"
          name="Weight"
          placeholder="Enter Your Weight"
          value={Number}
          required
        />
      </div>

      <div className="input-holder300">
        <input
          className="input-holder300"
          type="Age"
          name="Age"
          placeholder="Enter Your Age"
          value={Number}
          required
        />
      </div>

      <button type="submit" className="button-container-confirm">
        Confirm
      </button>

      <h1 className="Tell-p">Tell Us If Something Doesn't Like You</h1>

      <div className="input-holder400">
        <input
          className="input-holder400"
          type="string"
          name="string"
          placeholder="Tell Us If Something Doesn't Like You"
        />
      </div>
      <button type="submit" className="button-container-send">
        Send
      </button>
    </div>
  );
}
export default ProfileTab;
