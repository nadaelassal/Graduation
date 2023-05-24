/* eslint-disable jsx-a11y/alt-text */
import pro from "./pro.png";
import "./css code/profiletab.css";
import { useNavigate } from "react-router-dom";

function ProfileTab() {
  const navigate = useNavigate();
  return (
    <div>
      <img src={pro} className="protab" />
      <h2 className="nameinput">Aliaa Mohammed</h2>
      <h1 className="update-p">Update Your Details :</h1>
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

      <button type="submit" className="button-container-confirm" onClick={() => navigate ('/Home')}>
        Confirm
      </button>
    </div>
  );
}
export default ProfileTab;
